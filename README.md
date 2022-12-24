# sshb/telnetb
A Multithreaded SSH Bruteforce Tool written mainly for botnets, educational purpose

## Usage:
```
pip3 install -r requirements.txt
python3 sshb/telnetb.py 1.0.0.0/8 credentials.txt timeout threads(max 1000)

python3 sshb/telnetb.py 155.0.0.0/8 credentials.txt 5 500

only supports valid ranges:
0.0.0.0/0
1.0.0.0/8
1.1.0.0/16
1.1.1.0/24

valid_ssh/telnet.txt: 
ip:port username:password
```
