'''
Created on Sep 17, 2018

@author: Z231479
'''

import socket
import time

class tcpping:
    
    def __init__(self,host,port=22,maxCount=3,detail=False):
        
        self.maxCount = maxCount
        self.port = port
        self.host = host
        self.count = 0
        self.detail = detail
        
        self.ping()
    
    def ping(self):
        
        passed = 0
        failed = 0
        
        while self.count < self.maxCount:
            # Increment Counter
            self.count += 1
        
            success = False
        
            # New Socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            # 1sec Timeout
            s.settimeout(1)

            # Try to Connect
            try:
                s.connect((self.host, int(self.port)))
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
            if self.count < self.maxCount:
                time.sleep(1)
                
            if self.detail:
                return {passed,failed}
            else:
                if passed != 0:
                    return True
                else:
                    return False






