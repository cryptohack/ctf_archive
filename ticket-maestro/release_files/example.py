from pwn import *
import json 

def redeemTicket(rem, ticket_proof):
    payload = {"Redeem":{"proof":ticket_proof}}
    print(json.dumps(payload))
    rem.sendline(json.dumps(payload).encode())

    resp = rem.readline().decode()
    return resp

def getBalance(rem):
    rem.sendline(b'"Balance"')
    resp = rem.readline().decode()
    return resp

def buyFlag(rem):
    rem.sendline(b'"BuyFlag"')
    resp = rem.readline().decode()
    return resp

def buyTicket(rem):
    rem.sendline(b'"BuyTicket"')
    resp = rem.readline().decode()
    return resp

def getProvingKey(rem):
    rem.sendline(b'"ProvingKey"')
    resp = rem.readline().decode()
    return resp

def getVerifyingKey(rem):
    rem.sendline(b'"VerifyingKey"')
    resp = rem.readline().decode()
    return resp

def getDigest(rem):
    rem.sendline(b'"Digest"')
    resp = rem.readline().decode()#
    return resp

with remote("127.0.0.1", 1337) as rem:
    welcome = rem.readline()
    print(welcome)

    balance = getBalance(rem)
    print(f'balance = {balance}')
    
    digest = getDigest(rem)
    print(f'digest = {digest}')

    ticket = buyTicket(rem)
    print(f'ticket = {ticket}')

    balance = getBalance(rem)
    print(f'balance = {balance}')

    ticket_proof = json.loads(ticket)["Ticket"]["proof"]
    redeemed = redeemTicket(rem, ticket_proof)
    print("redeemed ticket = {redeemed}")

    redeemed = redeemTicket(rem, ticket_proof)
    print("redeemed ticket again = {redeemed}")

    balance = getBalance(rem)
    print(f'balance = {balance}')

    # vk = getVerifyingKey(rem)
    # pk = getProvingKey(rem)

    flag_response = buyFlag(rem)
    
    print(flag_response)
