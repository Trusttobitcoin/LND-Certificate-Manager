import os
import subprocess
import shutil
from datetime import datetime
import time

def run_command(command, shell=False):
    """Run a command and return its output"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def backup_certs():
    """Backup existing certificates"""
    backup_dir = f"/root/.lnd/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        os.makedirs(backup_dir, exist_ok=True)
        if os.path.exists('/root/.lnd/tls.cert'):
            shutil.copy2('/root/.lnd/tls.cert', backup_dir)
        if os.path.exists('/root/.lnd/tls.key'):
            shutil.copy2('/root/.lnd/tls.key', backup_dir)
        return True, f"Certificates backed up to {backup_dir}"
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def main():
    print("Starting LND certificate renewal process...")
    
    # 1. Backup existing certificates
    print("\n1. Backing up existing certificates...")
    success, message = backup_certs()
    print(message)
    if not success:
        return
    
    # 2. Stop LND
    print("\n2. Stopping LND service...")
    success, message = run_command(['systemctl', 'stop', 'lnd'])
    if not success:
        print(f"Failed to stop LND: {message}")
        return
    print("LND service stopped")
    
    # 3. Remove old certificates
    print("\n3. Removing old certificates...")
    if os.path.exists('/root/.lnd/tls.cert'):
        os.remove('/root/.lnd/tls.cert')
    if os.path.exists('/root/.lnd/tls.key'):
        os.remove('/root/.lnd/tls.key')
    print("Old certificates removed")
    
    # 4. Start LND to generate new certificates
    print("\n4. Starting LND service to generate new certificates...")
    success, message = run_command(['systemctl', 'start', 'lnd'])
    if not success:
        print(f"Failed to start LND: {message}")
        return
    
    # 5. Wait for certificate generation
    print("Waiting for certificate generation...")
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        if os.path.exists('/root/.lnd/tls.cert') and os.path.exists('/root/.lnd/tls.key'):
            break
        time.sleep(1)
        attempt += 1
    
    if attempt >= max_attempts:
        print("Timeout waiting for certificate generation")
        return
    
    # 6. Verify new certificates
    print("\n5. Verifying new certificates...")
    success, cert_details = run_command(['openssl', 'x509', '-in', '/root/.lnd/tls.cert', '-noout', '-dates'])
    if success:
        print("New certificate details:")
        print(cert_details)
    
    # 7. Check LND status
    print("\n6. Checking LND status...")
    success, status = run_command(['systemctl', 'status', 'lnd'])
    if success:
        print("LND is running")
    else:
        print("Warning: LND might need attention")
    
    print("\nCertificate renewal process completed!")
    print("Note: You may need to unlock your wallet if it was previously locked.")
    print("To unlock: lncli unlock")

if __name__ == "__main__":
    main()
