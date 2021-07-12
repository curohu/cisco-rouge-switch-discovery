'''
Created on Jul 5, 2018
modified on April 26, 2019

@author: Z231479
'''



import subprocess
import platform
import time
import socket
import random
import os
import datetime
import sys

class main:
    
    def __init__(self,path,sitecode):
        self.path = path
        self.sitecode = sitecode
        
    def main(self):
        path = self.path
        sitecode = self.sitecode
        fIN = fileINHandler(path)
        GMACD = fIN.readGrandMACData()
        p = Parse(GMACD,sitecode)
        path,_ = p.parse()
        return path
    
class fileINHandler:
    
    def __init__(self,path):
        self.path = path

    def readGrandMACData(self):
        grandMACDict = dict() # this is a very large dict consisting of the files of all other devices in a large datafile
        # format [KEY:Hostname, Value:[Key: interfaceName, Value:[MACAddresses]]]
        try:
            with open(self.path,'r') as file:
                for line in file.readlines():
                    line = line.replace("'","").replace('\n','').split(',')
                    if line[0] not in grandMACDict.keys():
                        tempdict = dict()
                        tempdict[line[1]] = []
                        tempdict[line[1]].append(line[2])
                        grandMACDict[line[0]] = tempdict
                    else:
                        if line[1] not in grandMACDict[line[0]].keys():
                            tempdict = grandMACDict[line[0]]
                            tempdict[line[1]] = []
                            tempdict[line[1]].append(line[2])
                            grandMACDict[line[0]] = tempdict
                        else:
                            tempDict = grandMACDict[line[0]]
                            tempDict[line[1]].append(line[2])
                            grandMACDict[line[0]] = tempDict
                            
                file.close()
            return grandMACDict
        except Exception as e:
            raise e

        
class fileOUTHandler:
    
    def __init__(self,siteCode):
        self.siteCode = siteCode
        self.directory = "./{0}_data".format(self.siteCode)
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
        with open(str(self.directory)+'/{0}_Grand_Data_{1}.csv'.format(self.siteCode,str(datetime.datetime.today()).replace(':','')),'a') as file:
            for hostname, data in grandDict.items():
                for interface, MACs in data.items():
                    for m in MACs:
                        file.write("'{0}','{1}','{2}'\n".format(hostname,interface,m))
            file.close()

class Parse:
    
    def __init__(self,GMACD,sitecode):
        self.gmacd = GMACD
        self.sc = sitecode
        self.analysis_path = '{0}_analysis_{1}.csv'.format(self.sc,str(datetime.datetime.today()).replace(':',''))
        with open(self.analysis_path,'w') as file:
            file.write("Hostname,Port,Number_of_MAC_Addresses_on_Port,MAC_Address,Best_Guess_Vendor_for_MAC_Prefix\n")
            file.close() 
        
    
    def parse(self):
        gthan2 = self.__greaterThanTwo()
        with open(self.analysis_path,'a') as file:
            for key, value in gthan2.items():
                print("Analysing: "+str(key))
                for inter in value:
                    for m in inter[1]:
                        m1=m.replace('.','')
                        oui = self.__prefixAnalysis(m1[:6])
                        file.write("{0},{1},{2},{3},{4}\n".format(key,inter[0],str(len(inter[1])),m,oui))
            file.close() 
        return self.analysis_path,gthan2
        
    def __greaterThanTwo(self):
        output = dict()
        for device, data in self.gmacd.items():
            for interface, macs in data.items():
                if len(macs) >= 2 and len(macs) <= 10:
                    if device not in output.keys():
                        templist = []
                        templist.append([interface,macs])
                        output[device] = templist
                    else:
                        templist = output[device]
                        templist.append([interface,macs])
                        output[device] = templist
        return output
    
    def __prefixAnalysis(self,mac):
        output = 'no'
        with open('fixedOUI.txt','r',encoding='utf8') as file:
            for l in file.readlines():
                if mac.lower() in l.lower():
                    output = l.replace('\n','').split(',')[1]
            file.close()
        return output

if __name__ == '__main__':
    main()
























