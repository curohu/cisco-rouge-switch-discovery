'''
Created on April 26, 2019

@author: Z231479

Overview: wrapper for older code to discover, index and then analyse MAC addresses from sites 
'''

import analysis
import finder
import getpass
import time

class main:
    
    def main(self):
        
        username = ''
        password = ''
        siteCode = ''
        hostnameFilePath = './hostnames.txt'
        
        username = input("Enter SSH Username: ")
        password = getpass.getpass("Enter SSH Password: ")
        siteCode = input("Enter three character Site Code: ")
        hostnamepathcheck = input("Enter hostname file path. Make sure that there are hostnames in the file otherwise the program will throw an error (press enter for default, ./hostnames.txt): ")
        if hostnamepathcheck is not "":
            hostnameFilePath = hostnamepathcheck
        print("\nThis will take while, please let the program run until it says \"END\"\n")
        time.sleep(2)
        # run finder
        f = finder.main(username,password,siteCode,hostnameFilePath)
        folderPath,GMACD_Path = f.main()
        formanted_GMACD_Path = folderPath+GMACD_Path
        # run analysis
        a = analysis.main(formanted_GMACD_Path,siteCode)
        analysis_path = a.main()
        print("\n\nFile output is in: '{0}'. It is a list of all MAC addresses and OUI Vendors on ports with more than 2 MAC addresses.".format(analysis_path))
        time.sleep(2)
        print("\n\nEND")
        input("Press \'Enter\' to exit")

if __name__ == '__main__':
    m = main()
    m.main()
