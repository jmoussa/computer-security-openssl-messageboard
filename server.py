import socket 
import ssl
import thread
import os
from passlib.hash import sha256_crypt

HOST, PORT = '127.0.0.1', 5000

def handle(conn):
    conn.send('First ACK'.encode())
    data = conn.recv(1024).decode()
    print 'First Client Message (SYN): ' + data
    #Confirmed connection and Synced
    username = conn.recv(1024).decode()
    password = conn.recv(1024).decode()
    isVerified = verify_add(username, password)
    if(isVerified==1):
        conn.send('SUCCESS')
        data = query(conn, username)
    else:
        conn.send('INVALID LOGIN')
   
    if data == "QUIT":
        return
    else:
        handle(conn)

def verify_add(username, password):
    hash = sha256_crypt.encrypt(password)
    print 'Password Hashed'
    fo = open("passwords.txt", "r")
    line = fo.readline()    
    count = 1
    while line:
        if count%2 != 0:
            usercheck = line.strip('\n')
            if usercheck == username:
                stored_hash = fo.readline().strip('\n')
                if sha256_crypt.verify(password, stored_hash):
                    usercheck = fo.readline()
                    count += 1
                    print 'Verified!\nWelcome ' + username
                    return 1
                else:
                    print 'Wrong Password. Try Again'
                    return 0
            else:
                #Didn't find matching username
                line = fo.readline()
                count += 1
        else:
            #Didn't land on the Username (landed on password line)
            line = fo.readline()
            count += 1
    fo.close
    fo = open("passwords.txt", "a") 
    fo.write(username + '\n' + hash + '\n')
    print 'User ' + username + ' Added'
    fo.close()
    return 1

def query(conn, username):
    conn.send('Server ACK QUERY'.encode())
    data = conn.recv(1024).decode()
    while data != 'END':
        print 'Accepting input'
        data = conn.recv(1024).decode()
        print data
        if(data == 'END'):
            print 'Logging Out'
            conn.send('END'.encode())
            return
        elif data == 'GET':
            #RETRIEVE FROM NEXT ARGUMENT
            print 'Fetching from messageboard'
            conn.send('GET'.encode())
            board_name = conn.recv(1024).decode()
            try:
                fd = open('./boards/'+board_name, 'r')
            except:
                conn.send(board_name + " does not exist".encode())
                continue
            content = ""
            for line in fd.readlines():
                content += line + '\n'
            conn.send(content.encode())
            #if there send read buffer
            #if not there then send back 'not there'
        elif data == 'POST':
            #POST TO MESSAGE BOARD
            print 'Posting to messageboard'
            conn.send('POST'.encode())
            board_name = conn.recv(1024).decode()
            message = conn.recv(4096).decode()
            #Search for board_name.txt
            fd = open('./boards/'+board_name, 'a+')
            fd.write(message + ' - ' + username + '\n')
            fd.close()
        elif data == 'QUIT':
            conn.send('QUIT'.encode())
            print 'Client Disconnecting'
            return 'QUIT'
        else:
            conn.send('ACK'.encode()) 
    conn.send('END')

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        conn = None
        ssock, addr = sock.accept()
        try:
            conn = ssl.wrap_socket(ssock, server_side=True, certfile="domain.crt", keyfile="domain.key")
            print 'server is running on port 5000'
            thread.start_new_thread(handle, (conn,)) #spin up a new client handler thread
        except ssl.SSLError as e:
            print(e)

if __name__ == '__main__':
    main()
