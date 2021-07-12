'''
Created on Jul 5, 2018
modified on April 26, 2019

@author: Z231479
'''


import time
import os
import datetime
import sys
from ssh import ssh


class main:
    
    def __init__(self,username,password,siteCode,hostnamefilepath):
        self.username = username
        self.password = password
        self.hostnameFile = hostnamefilepath # path to the file
        self.siteCode = siteCode
        self.GMACD_Path = '/{0}_Grand_Data_{1}.csv'.format(self.siteCode,str(datetime.datetime.today()).replace(':',''))
        self.directory = "./{0}_data".format(self.siteCode)
        


    def main(self):
        Username = self.username
        Password = self.password
        locationPrefix = self.siteCode
        hostnameFile = self.hostnameFile
        
        print('\nSTART\n')
        fileIN = fileINHandler(hostnameFile,locationPrefix,self.directory,self.GMACD_Path)
        hosts = fileIN.readHostFile()
        for h in hosts:
            print('\nAccessing: {0}...'.format(h))
            s = ssh(h, Username, Password)
            fileOut = fileOUTHandler(locationPrefix,self.directory,self.GMACD_Path)
            try:
                if s.connect():
                    _, stout, _ = s.getStreams('show mac address-table\n')
                    time.sleep(1)
                    rawOutput = stout.readlines()
                    print('Parsing Data...')
                    p = Parse(rawOutput)
                    formatedOutput = p.parse()
                    print('Writing Data...')
                    fileOut.write(h, formatedOutput)
                    s.close()
            except Exception as e:
                sys.stderr.write('Error with {0}, encountered Exception: {1}'.format(h,str(e)))
    
        # TODO add analysis
        print('\nGenerating MAC List...\n')
        
        GMACD = fileIN.readMACData()
        
        return self.directory,self.GMACD_Path

class fileINHandler:
    
    def __init__(self,hostnameFile,siteCode,directory,GMACD_Path):
        self.hostnameFile = hostnameFile # path to the file
        self.siteCode = siteCode
        self.directory = directory
        self.GMACD_Path = GMACD_Path
    
    def readHostFile(self):
        hostnames = []
        with open(self.hostnameFile, 'r') as file:
            for l in file.readlines():
                if l is not '':
                    hostnames.append(l.replace('\n',''))
            file.close()
        return hostnames
    
    def readMACData(self):
        grandMACDict = dict() # this is a very large dict consisting of the files of all other devices in a large datafile
        # format [KEY:Hostname, Value:[Key: interfaceName, Value:[MACAddresses]]]
        try:
            dataFiles = []
            for f in os.listdir("./{0}_data".format(self.siteCode)):
                if 'grand' not in f:
                    dataFiles.append(str(f))
            for f in dataFiles:
                if f.split('_')[0] not in grandMACDict.keys(): 
                    grandMACDict[str(f.split('_')[0])] = dict()
                    deviceDict = dict()
                    with open(str("./{0}_data/".format(self.siteCode))+str(f), 'r') as file:
                        for l in file.readlines():
                            key, value = l.replace("'",'').replace('\n','').split(',')
                            if key in deviceDict.keys():
                                tempList = deviceDict[key]
                                tempList.append(value)
                                deviceDict[key] = tempList
                            else:
                                tempList = []
                                tempList.append(value)
                                deviceDict[key] = tempList
                        file.close()
                    grandMACDict[str(f.split('_')[0])] = deviceDict  
            fOUT = fileOUTHandler(self.siteCode,self.directory,self.GMACD_Path)
            fOUT.grandWrite(grandMACDict)
            return grandMACDict
        except Exception as e:
            raise e
        
class fileOUTHandler:
    
    def __init__(self,siteCode,directory,GMACD_Path):
        self.siteCode = siteCode
        self.GMACD_Path = GMACD_Path
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def write(self,hostname,dataDict):
        with open(str(self.directory)+'/{0}_Data_{1}.csv'.format(hostname,str(datetime.datetime.today()).replace(':','')),'a') as file:
            for key, value in dataDict.items():
                for v in value:
                    file.write("'{0}','{1}'\n".format(str(key),str(v)))
            file.close()
        return True
    
    def grandWrite(self,grandDict):
        with open(str(self.directory)+self.GMACD_Path,'a') as file:
            for hostname, data in grandDict.items():
                for interface, MACs in data.items():
                    for m in MACs:
                        file.write("'{0}','{1}','{2}'\n".format(hostname,interface,m))
            file.close()

class Parse:
    
    def __init__(self,stout):
        self.stout = stout
    
    def parse(self):
        interfaceDict = dict()
        for l in self.stout[5:-1]:
            j = l.replace('\r','').replace('\n','').split('    ')
            if 'CPU' in j[3].replace(' ',''):
                pass
            elif j[3].replace(' ','') in interfaceDict.keys():
                tempList = interfaceDict[j[3].replace(' ','')]
                tempList.append(j[1])
                interfaceDict[j[3].replace(' ','')] = tempList
            else:
                tempList = []
                tempList.append(j[1])
                interfaceDict[j[3].replace(' ','')] = tempList
        return interfaceDict

if __name__ == '__main__':
    main()


















