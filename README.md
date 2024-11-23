# LND Certificate Manager 🔐⚡

A lightweight utility for managing and monitoring LND (Lightning Network Daemon) TLS certificates. Keep your Lightning Node secure with automated certificate monitoring and renewal capabilities.

## 🚀 Features

- **Certificate Detection**: Automatically locates LND certificate files
- **Status Monitoring**: Detailed reporting of certificate validity and expiration
- **Auto Renewal**: Streamlined certificate renewal process
- **Safe Backups**: Automatic backup of existing certificates
- **Security Checks**: Verification of file permissions and ownership
- **Detailed Logging**: Comprehensive operation logging

## 📋 Prerequisites

- Python 3.6 or higher
- Running LND node
- Root access or appropriate permissions
- OpenSSL installed

## 🛠️ Installation

```bash
# Clone the repository
git https://github.com/Trusttobitcoin/LND-Certificate-Manager
cd lnd-cert-manager

# Make scripts executable
chmod +x *.py
```

## 📖 Usage

### Check Certificate Status

```bash
python3 check_lnd_certs.py
```

This will:
- Locate your LND certificates
- Display expiration dates
- Show file permissions
- Report LND service status

### Renew Certificates

```bash
python3 renew_lnd_certs.py
```

This will:
- Backup existing certificates
- Stop LND service
- Generate new certificates
- Restart LND service
- Verify renewal success

## 📁 File Structure

```
lnd-cert-manager/
├── README.md
├── check_lnd_certs.py    # Status checker
├── renew_lnd_certs.py    # Renewal utility
└── requirements.txt      # Dependencies
```

## 🔒 Security Best Practices

- Always backup certificates before renewal
- Maintain proper file permissions (600 for private keys)
- Keep LND node updated
- Regular certificate expiration monitoring
- Secure backup storage

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚡ Support

If you find this tool useful:
- Star the repository
- Report issues
- Submit feature requests
- Share with other node operators

## 🙏 Acknowledgments

- Lightning Network Community
- LND Development Team

---

Made with ❤️ for the Lightning Network Community

*Note: Always test certificate renewal in a safe environment first!*
