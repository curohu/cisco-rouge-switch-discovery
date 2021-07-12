'''
Created on Jul 6, 2018

@author: Z231479
'''
class Parse:
    
    def __init__(self,GMACD,sitecode):
        self.gmacd = GMACD
        self.sc = sitecode
    
    def parse(self):
        gthan2 = self.__greaterThanTwo()
        with open('analysis.csv','w') as file:
            for key, value in gthan2.items():
                print(str(key)+'\n\n')
                for inter in value:
                    for m in inter[1]:
                        m1=m.replace('.','')
                        oui = self.__prefixAnalysis(m1[:6])
                        file.write("{0},{1},{2},{3},{4}\n".format(key,inter[0],str(len(inter[1])),m,oui))
            file.close() 
        return gthan2
        
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
