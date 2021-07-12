'''
Created on Jul 5, 2018

@author: Z231479
'''


oui=dict()
with open('oui.txt','r',encoding='utf8') as file:
    for l in file.readlines():
        l = l.replace('\n','')
        if '(base 16)' in l:
            oui[l.split(' ')[0]] = l[22:]
    file.close()
with open('fixedOUI.txt','w',encoding='utf8') as file:
    for key, value in oui.items():
        file.write("{0},{1}\n".format(key,value.replace(',','')))
    file.close()