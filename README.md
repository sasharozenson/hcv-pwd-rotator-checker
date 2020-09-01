# What for?
 - This script is intended to check whether there are hosts that didn't rotate their password for more than 24h
 - Script will send mail only if there are at least one server
 
# Requirements
 - python3
 - python3 system packages
 - requests package
 - Hashi Corp Vault

# Configuration
 - mv config.py.template config.py
 - vim config.py insert valid vault token

# Usage
 - This script is running by crontab (Currently on it-bot)
 - python3 rptc.py

# To Be done
 - ignore list