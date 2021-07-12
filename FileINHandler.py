'''
Created on Jul 6, 2018

@author: Z231479
'''
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

        

class fileINHandler:
    
    def __init__(self,hostnameFile,siteCode):
        self.hostnameFile = hostnameFile # path to the file
        self.siteCode = siteCode
    
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
            fOUT = fileOUTHandler(self.siteCode)
            fOUT.grandWrite(grandMACDict)
            return grandMACDict
        except Exception as e:
            raise e