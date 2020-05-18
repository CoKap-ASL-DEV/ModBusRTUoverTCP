def idSeperate(id):
    lenID = len(str(id))
    idSeparateList = []
    idInt = id
    for i in range(lenID):    
        temp = idInt % 10
        idSeparateList.append(temp)
        idInt = idInt // 10
    print(idSeparateList) ##reverse order    
    return idSeparateList


def calcChkCode(sum):
    chkTmp = sum & 0xFF
    chk = chkTmp
    if(chkTmp==0x02):
        chk=0x04    
    if(chkTmp==0x03):
        chk=0x05
    return chk

startChr = 0x02
comCode = 0x52 #(R)
typeChr = 0x45 #(E)
###########ID Setting ############
iD100 = 0x30 #(0)  100자리
iD10 = 0x30 #(0)   10자리
iD1 = 0x31 #(1)    1자리
#################################
endChr = 0x03

#ids = idSeperate(1230)
# print(ids)
res = calcChkCode(startChr+comCode+typeChr+iD100+iD10+iD1+endChr)
print(hex(res))

