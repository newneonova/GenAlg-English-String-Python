import base64


#OK genetic is base64 string

Bytes = base64.b64decode(D)
Z=''
for b in Bytes:
    Z=Z+format(b,'08b')
O=list()
for i in range(len(Z)):
    O.append(str(int(Z[i])))
R=''.join(O)
NUM= int(R,2)
OUT=base64.b64encode(NUM.to_bytes((NUM.bit_length()+7)//8,'big'))


#takes a base64 string a returns a list of strings integers 0,1 
def BaseToBin(BaseString):
    Bytes = base64.b64decode(BaseString)
    Z=''
    for b in Bytes:
        Z=Z+format(b,'08b')
    O=list()
    for i in range(len(Z)):
        O.append(str(int(Z[i])))
    return O

def BinToBase(Bin):
    R=''.join(Bin)
    NUM= int(R,2)
    return base64.b64encode(NUM.to_bytes((NUM.bit_length()+7)//8,'big'))
