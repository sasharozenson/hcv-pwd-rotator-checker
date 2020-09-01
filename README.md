# What for?
 - This script is intended to check whether there are hosts that didn't rotate their password for more than 24h
 - Script will send mail only if there are at least one server
 - Supports only kv2 
 
# Requirements
 - python3
 - python3 system packages
 - requests package
 - Hashi Corp Vault

# Configuration
 * mv config.py.template config.py
 * vim config.py
 * chmod +x rprc.py

# Usage
 - This script intended to run in crontab
 - python3 rprc.py

# To Be done
 - ignore list
