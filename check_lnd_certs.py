import os
import subprocess
import datetime
from pathlib import Path

def check_cert_details(cert_path):
    """Check certificate details using openssl"""
    try:
        cmd = f"openssl x509 -in {cert_path} -noout -dates"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error reading certificate: {str(e)}"

def check_lnd_directories():
    """Check common LND certificate locations and their contents"""
    possible_locations = [
        '/root/.lnd',
        '/home/bitcoin/.lnd',
        '/data/lnd',
        '/etc/lnd',
        os.path.expanduser('~/.lnd')
    ]
    
    print("Checking LND certificate locations...\n")
    
    found_certs = False
    for location in possible_locations:
        if os.path.exists(location):
            print(f"\n📁 Found LND directory: {location}")
            
            # Check tls.cert
            cert_path = os.path.join(location, 'tls.cert')
            if os.path.exists(cert_path):
                found_certs = True
                print(f"\n✅ Found tls.cert at: {cert_path}")
                print("Certificate details:")
                cert_details = check_cert_details(cert_path)
                print(cert_details)
                
                # Check permissions
                stat = os.stat(cert_path)
                print(f"File permissions: {oct(stat.st_mode)[-3:]}")
                print(f"Owner UID: {stat.st_uid}")
                
            else:
                print(f"❌ No tls.cert found in {location}")
            
            # Check tls.key
            key_path = os.path.join(location, 'tls.key')
            if os.path.exists(key_path):
                found_certs = True
                print(f"\n✅ Found tls.key at: {key_path}")
                # Check permissions
                stat = os.stat(key_path)
                print(f"File permissions: {oct(stat.st_mode)[-3:]}")
                print(f"Owner UID: {stat.st_uid}")
            else:
                print(f"❌ No tls.key found in {location}")
            
            # List other files in directory
            print("\nOther files in directory:")
            for item in os.listdir(location):
                if item not in ['tls.cert', 'tls.key']:
                    print(f"- {item}")
    
    if not found_certs:
        print("\n❌ No LND certificates found in any common locations!")
        
    # Check LND service status
    try:
        cmd = "systemctl is-active lnd"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        print(f"\nLND Service Status: {result.stdout.strip()}")
    except Exception as e:
        print(f"\nCouldn't check LND service status: {str(e)}")

if __name__ == "__main__":
    check_lnd_directories()
