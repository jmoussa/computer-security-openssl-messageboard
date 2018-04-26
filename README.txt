OpenSSL Message Board
Joseph Moussa - jam791



Need the following files to function (all included in tar file)
  domain.crt -- Certificate File (Necessary for SSL setup in client and server)
  domain.key -- Key File (Necessary for SSL setup in server)
  client.py  -- Python Client (login and interaction)
  server.py  -- Python Server (process and verify)
  password.txt -- Holds all login information
  /boards -- Holds all messageboard titles as files, files hold all messages tagged with users
    Food -- A sample message board

***SERVER MUST BE RUNNING BEFORE CLIENT***
Client will be asked to login/add an account, then will be given commands to input.
Must enter command, then press ENTER, then type argument


------------------------------------------------------------------------------------------------
USER MANUAL + IMPLEMENTATION DETAILS

-----------------------------------------
USER VERIFICATION
-----------------------------------------
Current implementation checks all usernames for a match, if one is matched, then it verifies the password stored with that username.
If the username matches but the password does not, then you are asked to try again (this method ensures no duplicate usernames).
If the username is not on file, then both the username and password are added.

-----------------------------------------
TO START
-----------------------------------------
Dependencies - make sure to pip install <package> (just in case)
  socket
  ssl
  thread
  os
  passlib

1. Start server
  python server.py

2. In a separate screen, start client
  python client.py

3. Follow on-screen instructions to login

4. After verfied you can now use GET, POST, END or QUIT as commands to interact with the server
  For the most part, you can follow the on screen instructions, but here's a breakdown:
  
  GET - Grabs all messages from the name of the message board entered after.
    *Will notify you if no message board exists
  POST - Posts to a message board. First supply the name of message board. 
    *If no message board exists, one is created, and message is added.
  END - Logs out a user (goes back to login screen)
  QUIT - Disconnects Client from server (Server still runs)

  *EXAMPLES for GET and POST syntax below


-----------------------------------------
GET Command Input Example
-----------------------------------------
$: GET
$: Food
- Server Grabs All Messages from Food message board -
"Message1 from Food" - User1
...


-----------------------------------------
POST Command Example
-----------------------------------------
$: POST
$: Food
$: I really loved this pot roast Diane
- Server posts 'I really loved this pot roast Diane' to Food message board -
...
