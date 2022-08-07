import random
import os
import signal
import sys
from blake3 import blake3 # https://pypi.org/project/blake3/


def tle_handler(*kwargs):
    raise Exception('Time limit exceeded.')


class AuthenticationServer:
    def __init__(self, password):
        self.password = password
        self.challenge = None

    def handshake(self, challenge):
        if len(challenge) != 16:
            raise Exception('Invalid challenge length.')
        
        self.challenge = os.urandom(16)

        # response = HASH(password || "HANDSHAKE_FROM_SERVER" || challenge)
        response = blake3(self.password + b"HANDSHAKE_FROM_SERVER" + challenge).digest()

        return response, self.challenge


    def verify_handshake(self, response):
        if self.challenge is None:
            raise Exception('Server did not generate a challenge. Use `generate_challenge` to generate a challenge first.')
        if response != blake3(self.password + b"HANDSHAKE_FROM_CLIENT" + self.challenge).digest():
            raise Exception('Invalid response.')

        return


class AuthenticationClient:
    def __init__(self, password):
        self.password = password
        self.challenge = None

    def generate_challenge(self):
        self.challenge = os.urandom(16)
        return self.challenge

    def verify_handshake(self, response, challenge):
        if self.challenge is None:
            raise Exception('Client did not generate a challenge. Use `generate_challenge` to generate a challenge first.')
        if response != blake3(self.password + b"HANDSHAKE_FROM_SERVER" + self.challenge).digest():
            raise Exception('Invalid response.')

        # response = HASH(password || "HANDSHAKE_FROM_CLIENT" || challenge)
        response = blake3(self.password + b"HANDSHAKE_FROM_CLIENT" + challenge).digest()
        
        return response


# I'll show you the protocol.
def test():
    password = bytes(random.sample(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6))

    client = AuthenticationClient(password)
    server = AuthenticationServer(password)

    # == The protocol ==

    # Steps 1+2+3: Client could verify that the server has the password, without leaking the password.
    # Steps 2+3+4: Server could verify that the client has the password, hence completing the authentication.

    # Step 1: Client generates a 16-byte challenge.
    challenge_client = client.generate_challenge()

    # Step 2: Client sends the challenge to the server.
    #         Server computes a response and generates a challenge.
    response_server, challenge_server = server.handshake(challenge_client)

    # Step 3: Server sends the response and the challenge to the client.
    #         Client verifies the response and solves the challenge.
    response_client = client.verify_handshake(response_server, challenge_server)

    server.verify_handshake(response_client)


# Now, it is your turn!
def main():
    flag = os.environ.get('FLAG', 'firebird{***REDACTED***}')

    # 6 letter password is not secure enough (there are only ~36 bit entropy).
    # Sarcastly, you cannot exhaust them during the CTF anyway. :)
    password = bytes(random.sample(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6))

    client = AuthenticationClient(password)
    server = AuthenticationServer(password)

    # == The protocol ==
    
    # Oh of course I am not patient.
    signal.alarm(10)
    signal.signal(signal.SIGALRM, tle_handler)

    # Steps 1+2+3: Client could verify that the server has the password, without leaking the password.
    # Steps 2+3+4: Server could verify that the client has the password, hence completing the authentication.

    try:
        # Step 1: Client generates a 16-byte challenge.
        challenge_client = bytes.fromhex(input('challenge_client = '))

        # Step 2: Client sends the challenge to the server.
        #         Server computes a response and generates a challenge.
        response_server, challenge_server = server.handshake(challenge_client)

        # Step 3: Server sends the response and the challenge to the client.
        #         Client verifies the response and solves the challenge.
        print(f'response_server = {response_server.hex()}')
        print(f'challenge_server = {challenge_server.hex()}')
        response_client = bytes.fromhex(input('response_client = '))

        # Step 4: Client sends the response to the server.
        #         Server verifies the response and finishes authenticating the user.
        server.verify_handshake(response_client)

        print(f'Congrats! {flag}')
    except Exception as err:
        print(f'\033[031mError: {err}\033[0m')


if __name__ == '__main__':
    test()
    main()