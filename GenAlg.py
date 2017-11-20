import base64
import random

class Worm:
    Eld = 0
    Youth = 0
    Gen = ''
    P = str(Eld)+':'+str(Youth)+':'+Gen

    def updateP(self):
        self.P = str(self.Eld)+':'+str(self.Youth)+':^:'+str(self.Gen)
    
    def __init__(self,length):
        #length is length of the base64 string
        #2^24 - 1 bits is a length 4 base64 string
        if(length!=0):
            bits = (length//4 + length%4)*24
            z=random.getrandbits(bits)
            self.Gen = base64.b64encode(z.to_bytes((z.bit_length() + 7) // 8, 'big')).decode()
            self.updateP()
    #ok we make a new worm
    @classmethod
    def Breed(self,worm1,worm2):
       
        NewW = Worm(0)
        Pflag=0
        Farr = BaseToBin(worm1.Gen)
        Marr = BaseToBin(worm2.Gen)
        MaxL= max(len(Farr),len(Marr))
        NewGen=list()
        iters= iter(range(MaxL))
        for i in iters:
            if(i>=len(Farr)):
                Farr=Marr
            if(i>=len(Marr)):
                Marr=Farr
            if(i%6 == 0):
                s=random.randint(0,9)
                if(s==0):
                    Pflag=Pflag^1
               
            MainP = Farr
           
            if(Pflag==1):
                MainP=Marr  
            r=random.randint(0,1000)
            if(r==0):
                NewGen.append(str(int(MainP[i])^1))
            else:
                NewGen.append(MainP[i])
            if(i%24 == 0):
                z=random.randint(0,1000)
                if(z==0):
                    Bits=format(random.getrandbits(24),'024b')
                    for b in Bits:
                        NewGen.append(b)
                if(z==1 and i+24 < MaxL):
                    [iters.__next__() for x in range(24)]
        print(len(NewGen))
        NewW.Gen = BinToBase(NewGen)
        NewW.Eld = max(worm1.Eld,worm2.Eld)+1
        NewW.Youth = min(worm1.Youth,worm2.Youth)+1
        NewW.updateP()
        return NewW




def Btest(P):
    P=Worm.Breed(P,P)
    print(P.P)
    return P


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
    return base64.b64encode(NUM.to_bytes((NUM.bit_length()+7)//8,'big')).decode()
