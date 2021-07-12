'''
Created on Aug 18, 2017
Updated on July 6, 2018
'''
import Local_paramiko as paramiko
import platform
import socket
import time
import os
import threading

#    Abstract:
#        This is a easy wrapper around paramiko to run arbritrary SSH commands on a device
#        First initilize the class with the requires infromation, call the ssh.connect() function and run a command
#

class ssh:
    
    def __init__(self, ip, username, password, verbose='n'):
        self.ip = socket.gethostbyname(ip) #  if name=ipaddress format (ex 127.0.0.1) then it will just return the address format :)
        self.username = username
        self.password = password
        self.connection = None
        self.verbose = verbose # if this is 'y' it will print status, else it will not print anything
    
    def connect(self):
        if self.__checkIP(self.ip):
            if self.__checkCred(self.username, self.password): 
                if self.__createConnection():
                    return True
            else:
                raise Exception('CredentialError')
        else:
            raise Exception('IPError')


    def __checkCred(self, u, p):  #
            try:
                if self.verbose is 'y': print("\nTesting access to: ", str(self.ip));
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip, username=u, password=p, timeout=10)
                ssh.close()
                return True
            except:
                return False  # username or password are incorrect 

    def __checkIP(self,host,port=22,maxCount=1):
        
        maxCount = maxCount
        port = port
        host = host
        count = 0
        passed = 0
        failed = 0
        while count < maxCount:
            # Increment Counter
            count += 1
            success = False
            # New Socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 1sec Timeout
            s.settimeout(1)
            # Try to Connect
            try:
                s.connect((host, int(port)))
                s.shutdown(socket.SHUT_RD)
                success = True
            # Connection Timed Out
            except socket.timeout:
                failed += 1
            except OSError as e:
                print("OS Error:", e)
                raise e
            if success:
                passed += 1
            # Sleep for 1sec
            if count < maxCount:
                time.sleep(1)
            if passed != 0:
                return True
            else:
                return False

    def __createConnection(self):
        try:
            if self.verbose is 'y': print("\nTrying to connect...");
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            ssh.connect(self.ip, username=self.username, password=self.password, timeout=10)
            self.connection = ssh
            if self.verbose is 'y': print("Successfully connected to "+ str(self.ip)+"\n");
            return True
        except Exception as e: 
            raise e
          
    def runCommand(self, commands, readyToSendFlag="#"): # you get one shot at running these commands if the shell is closed you will need to open a new channel/session
        try:
            if self.connection != None:
                c = self.connection
                shell = c.invoke_shell()
                for cmd in commands:
                    shell.send(str(cmd + '\n'))
                    if self.verbose is 'y': print('Running: ', cmd);
                    while True:
                        output = str(shell.recv(9999))
                        if readyToSendFlag in output: # i am using "#" to notify the script that it is ready for more input; Change as needed
                            break
                        else:
                            time.sleep(.5)
                shell.close()
                return True
            elif self.__createConnection():
                self.runCommand(commands, readyToSendFlag=readyToSendFlag)
            else:
                raise Exception('SSHRunCmdException')
        except Exception as e:
            raise e
        
    def getStreams(self, command):
        try:
            if self.connection != None:
                c = self.connection
                if self.verbose is 'y': print('Expecting Output from: ', command);
                try:
                    stin, stout, sterr = c.exec_command(command) # returns 3 file-like streams stin, stout, sterr
                except:
                    self.close()
                return stin, stout, sterr
            elif self.__createConnection():
                return self.getStreams(command)  # returns 3 file-like streams stin, stout, sterr 
            else:
                raise Exception('SSHStreamException')
        except Exception as e:
            raise e

    def continuousShell(self, cmd, ty='cisco', readyToSendFlag="#",refresh=1.5): # refresh under 1 sec may cause issues with windows cmd
        try:
            if self.connection != None:
                c = self.connection
                shell = c.invoke_shell()
                if ty is 'cisco':
                    shell.send(str('term length 0\n'))
                #open tread
                t = threading.Thread(target=self.__continueShell_inputManager)
                t.daemon = False
                t.start()
                while t.is_alive():
                    if platform.system().lower() == "windows":
                        os.system('cls')
                    else: 
                        os.system('clear')
                    shell.send(str(cmd)+'\n')
                    print(str(shell.recv(9999).decode('utf-8')).replace("\"", '').replace("'", '').replace('[','').replace(']','').replace('\\n','\n').replace('\\r','\r')+'\n')
                    time.sleep(refresh)
            elif self.__createConnection():
                return self.continuousShell(cmd, ty=ty, readyToSendFlag=readyToSendFlag,refresh=refresh)
        except Exception as e:
            raise e

    def __continueShell_inputManager(self):
            input()

    def close(self):  # make sure to close the connection when done
        if self.connection != None:
            self.connection.close()
            self.connection = None
            return True
        else:
            return False
