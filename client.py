import socket 
import ssl

HOST, PORT = '127.0.0.1', 5000

def handle(conn):
    print 'Please Login:\n'
    conn.send('SYN'.encode())
    data = conn.recv(1024).decode()
    #print 'First Server Response: ' + data
    #Confirmed Connection and Synced
    complete = login(conn)
    if(complete == 1):
        data = query(conn)
    else:
        print "ERROR: Invalid Login"
    if(data == 'QUIT'):
        print 'Exiting Client'
        conn.close()
        return
    handle(conn)

def login(conn):
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    conn.send(username.encode())
    conn.send(password.encode())
    data = conn.recv(1024).decode()
    if(data == 'SUCCESS'):
        return 1
    else:
        return 0

def query(conn):
    data = conn.recv(1024).decode()
    #print "Server Response: " + data
    conn.send("SYN".encode())
    while data != 'END':
        input = raw_input("Enter a command (GET, POST, END) or QUIT to exit/terminate the client: ")
        conn.send(input)
        data = conn.recv(1024).decode()
        if data == 'END':
            return 'END'
        elif data == 'QUIT':
            return 'QUIT'
        elif data == 'GET':
            board_name = raw_input("Name of Message Board: ")
            conn.send(board_name.encode())
            buffer = conn.recv(4096).decode()
            print buffer
        elif data == 'POST':
            board_name = raw_input("Name of Board to Post to: ")
            message = raw_input("Message: ")
            conn.send(board_name.encode())
            conn.send(message.encode())
    return 'END'

def main():
    sock = socket.socket(socket.AF_INET)
    conn = ssl.wrap_socket(sock, ca_certs="domain.crt")
    try:
        conn.connect((HOST, PORT))
        handle(conn)
    finally:
        conn.close()
    
if __name__ == '__main__':
    main()
