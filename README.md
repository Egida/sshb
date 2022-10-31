# sshb
A Multithreaded SSH Bruteforce Tool written for IP Lists

Anti Honeypot is added to it!

## Usage:
```
pip3 install -r requirements.txt
zmap -p 22 -o iplist.txt
python3 main.py iplist.txt output.txt
Output.txt: 
ip ['username', 'passwort'] uname_output
```
