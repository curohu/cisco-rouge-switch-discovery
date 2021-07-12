'''
Created on Jul 6, 2018

@author: Z231479
'''


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
