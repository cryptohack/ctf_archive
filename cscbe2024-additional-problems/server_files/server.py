import Crypto.Util.number # Ensure all our RNGs are safe!!
import random # This is only used for the noise and not for the key, so it's fine
import binascii
import os

FLAG = os.getenv('FLAG')

def dghv_encrypt(p, N, m):
    """
    Encrypt a value to later decrypt with `dghv_decrypt`
    """
    assert 2**7 <= N < 2**8 # Normally this is 2, but by using a bigger `N` we can encode ASCII bytes instead of bits! That's much more efficient. All `N` in this range should be secure, so let's make it an assertion

    q = random.getrandbits(1024)
    rmax = 2**128 / N / 4
    r = random.randint(0, rmax) # In v2.0, we will let `r` be negative as well as positive => double the randomness!
    return p*q + N*r + m

def dghv_decrypt(p, N, c):
    """
    Since c = pq + Nr + m, we can find m as (c mod p) mod N!
    """
    return (c % p) % N

def dghv_add(c1, c2):
    """
    The sum of ciphertexts decodes to the sum of plaintexts!!!
    """
    return c1 + c2 # We will add bootstrapping to make this fully homomorphic in v2.0

def dghv_multiply(c1, c2):
    raise NotImplementedError # We will add multiplication in v2.0

def serialize(s):
    res = binascii.hexlify(s).decode()
    return ' '.join([res[i:i+2] for i in range(0, len(res), 2)])

def deserialize(s):
    return binascii.unhexlify(s)


def Game(client_socket):
    GameStatus = True

    output(client_socket, "Welcome! We're glad you're trying out our free and secure encryption service.\n\nYou're currently on v1.0. This is only the beginning -- v2.0 will bring extra features and security fixes and v3.0 will add AI, probably.\n")
    while True:
        p = Crypto.Util.number.getPrime(128) # VERY IMPORTANT!!! THIS MUST BE COPRIME WITH ALL N!!! So let's just make it prime to be sure :-)

        output(client_socket, "We've generated a private key, it's like super secure!")
        output(client_socket, "We've even encrypted our secret flag with it:")
        output(client_socket, "\n".join(map(lambda c: "  " + str(dghv_encrypt(p, 2**7, ord(c))), FLAG)))
        output(client_socket, "")
        output(client_socket, "Now you get to encrypt and decrypt stuff. You can try out the killer feature: if you encrypt two strings, add them, and decrypt them, you get the sum of the strings! Have fun!!")
        output(client_socket, "")

        first_iter = True
        while True:
            if first_iter:
                first_iter = False
                action = "new"
            else:
                while True:
                    output(client_socket, "What do you want to do?\n   (1) Start a new encryption\n   (2) Encrypt and add to the current encrypted value\n   (3) Decrypt the current encrypted value\n     > ", newline=False)
                    choice = client_socket.recv(1024).decode().strip()
                    if choice == '1':
                        action = "new"
                        break
                    elif choice == '2':
                        action = "add"
                        break
                    elif choice == '3':
                        action = "decrypt"
                        break
                    else:
                        output(client_socket, "Invalid option :(")

            if action == "new":
                while True:
                    output(client_socket, "Choose N: ", newline=False)
                    try:
                        N = client_socket.recv(1024).decode().strip()
                        N = int(N)
                        assert 2**7 <= N < 2**8
                        break
                    except Exception as e: output(client_socket, f"Invalid option :( Error: {e}")
            if action == "new" or action == "add":
                while True:
                    output(client_socket, "Message to encode (converted to hexadecimal): ", newline=False)
                    try:
                        m = deserialize(client_socket.recv(1024).decode().strip().replace(' ', ''))
                        lnew = len(m)
                        if any([char >= N for char in m]):
                            output(client_socket, f"Invalid input: message bytes cannot be larger than N!")
                            continue

                        if action == "add": 
                            assert lnew == l
                        else:
                            l = lnew
                            c = [0 for _ in range(l)]
                        break
                    except Exception as e: output(client_socket, f"Invalid option :( Error: {e}")
                c = [dghv_add(c[i], dghv_encrypt(p, N, m[i])) for i in range(l)]
            elif action == "decrypt":
                output(client_socket, "Decrypted message: " + serialize(bytes([dghv_decrypt(p, N, c[i]) for i in range(l)])))
            else:
                pass
    client_socket.close()

def output(client_socket, s, newline=True):
    client_socket
    client_socket.sendall(bytes(s + ("\n" if newline else ""), "utf-8"))

# --- TECHNICAL STUFF FOR THE SERVER ---
from http import client
import netifaces as ni
import argparse
from threading import Thread
from time import sleep
import sys
import socket

class ClientThread(Thread):
    def __init__(self, client_socket, ip, port):
        """[summary]

        Args:
            client_socket ([socket]): [holds the client socket]
        """
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = ip
        self.client_port = port

    def run(self):
            try:
                Game(self.client_socket)
            except BrokenPipeError:
                self.closeConn()
                return

    def closeConn(self):
        self.client_socket.close()
        print(f"{Colors.FAIL}[-] Client {self.client_ip}:{self.client_port} disconnected {Colors.ENDC}")


class Server():
    def __init__(self, address, port):
        """[summary]

        Args:
            address ([str]): [server's ip]
            port ([int]): [server's port]
        """
        self.initConn(address, port)

    @classmethod
    def initConn(self, address, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except Exception:
            print("Could not bind address to port, use a different port or try again later")
            sys.exit()
        if args.verbose:
            print(f"{Colors.BOLD}Listening on {address} {port} ...{Colors.ENDC}")
        while True:
            try:
                (client_socket, (ip, port)) = server_socket.accept()
                print(f"{Colors.OKGREEN}[+] Connection established from {ip} at port {port} {Colors.ENDC}")
                client_thread = ClientThread(client_socket, ip, port)
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}We are shutting down the server {Colors.ENDC}")
                sleep(1)
                break
            except Exception as e:
                print(f"{Colors.FAIL}Error occured {e} {Colors.ENDC}")
                break


def verifyInter(ip):
    interfaces = ni.interfaces()
    for i in interfaces:
        # Checking if there's an ip assigned to the interface
        if len(ni.ifaddresses(i)) > 1:
            if ip == ni.ifaddresses(i)[2][0]['addr']:
                return True
    return False

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Server settings args
    parser.add_argument('-p', '--port', metavar='', type=int, help='specify server\'s port', default=1337)
    parser.add_argument('-a', '--address', metavar='', type=str, help='specify server\'s address', default="0.0.0.0")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quit', action='store_true', help='quiet mode - default')
    group.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    AllowedAddre = ['localhost', '0.0.0.0']
    if(verifyInter(args.address) or (args.address in AllowedAddre)):
        try:
            server = Server(args.address, args.port)
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()
    print(f"{Colors.FAIL}Error occured. Try using a valid address or check network interfaces. {Colors.ENDC}")
