import requests

"""
Quick tutorial to retrieve cookies despite redirections:
When making a /login request, be sure to disable redirections :)
Otherwise, you won’t receive the cookie.
"""

from sys import argv
if len(argv) != 2:
    print("usage: `python template_authentification_ou_pas.py <URL>`")
    exit()

URL = argv[1]

# Register
url = f'{URL}/register'
data = {"username": "demo", "password": "demo"}
_ = requests.post(url, data=data)

# Login
url = f'{URL}/login'
response = requests.post(url, data=data, allow_redirects=False)
auth = response.cookies["auth"]

print(auth)

