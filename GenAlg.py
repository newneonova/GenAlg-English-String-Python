import base64
import random
import sys
color = sys.stdout.shell


DicFile = 'words.txt'
def loadDict():
    return set(line.strip() for line in open(DicFile))
EnglishDic = loadDict()
MaxLen = max(map(len, EnglishDic))


class Worm:
    Eld = 0
    Youth = 0
    Gen = ''
    P = str(Eld)+':'+str(Youth)+':'+Gen
    score = 0
    Words = list()
    Inds = list()

    def updateP(self):
        self.P = str(self.Eld)+':'+str(self.Youth)+':^:'+str(self.Gen)
        self.fitTest()

    def PRINT(self):
        Z=color.write(str(int(self.score))+':'+str(self.Eld)+":"+str(self.Youth)+":::",'stdout')
        if(len(self.Words)>0):
            self.Inds,self.Words = zip(*sorted(zip(self.Inds,self.Words)))
            Z=color.write(self.Gen[:self.Inds[0]],'stdout')
            stop = self.Inds[0];
            for j in range(len(self.Words)):
                if(self.Inds[j]+len(self.Words[j]) > stop):
                    Z=color.write(self.Gen[stop:(stop+len(self.Words[j]))] ,'KEYWORD')
                    stop = stop+len(self.Words[j])
                    if(j+1 not in range(len(self.Words))):
                       Z=color.write(self.Gen[stop:] ,'stdout')
                    else:
                       Z=color.write(self.Gen[stop:self.Inds[j+1]] ,'stdout')
                       stop = self.Inds[j+1]
            Z=color.write('_____'+','.join(self.Words),'stdout')
            Z=color.write('\n','stdout')
        else:
            Z=color.write(self.Gen ,'stdout')
            Z=color.write('\n','stdout')
            

    #scored based on unique words
    def fitTest(self):
        GenString = self.Gen
        self.Words = list()
        self.Inds = list()
        score = 0
        for i in range(len(GenString)):
            chunk = GenString[i:i+MaxLen+1]
            for j in range(4,len(chunk)+1):
                word = chunk[:j]
                if word in EnglishDic:
                    self.Words.append(word)
                    self.Inds.append(i)
        for word in set(self.Words):
            score=score+(pow(10,len(word))/len(GenString))
        self.score=score
        

    @classmethod
    def load(WormString):
        NewW = Worm(0)
        NewW.Gen = WormString.split(':^:')[1]
        NewW.Eld = WormString.split(':^:')[0].split(':')[0]
        NewW.Youth = WormString.split(':^:')[0].split(':')[1]
        NewW.updateP()
        return NewW
    
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
            
            ##if originating character is the same
            #mutation rate goes up to 1 in 100
            #index is floor(i/6)
            Ind = int(i/6)
            mutmult=1
            if(Ind<len(Farr) and Ind < len(Marr)):
                if(Farr[Ind]==Marr[Ind]):
                    mutmult=10
            r=random.randint(0,1000/mutmult)
            if(r==0):
                NewGen.append(str(int(MainP[i])^1))
            else:
                NewGen.append(MainP[i])
            if(i%24 == 0):
                z=random.randint(0,1000/mutmult)
                if(z==0):
                    Bits=format(random.getrandbits(24),'024b')
                    for b in Bits:
                        NewGen.append(b)
                if(z==1 and i+24 < MaxL):
                    [iters.__next__() for x in range(24)]
        NewW.Gen = BinToBase(NewGen)
        NewW.Eld = max(worm1.Eld,worm2.Eld)+1
        NewW.Youth = min(worm1.Youth,worm2.Youth)+1
        NewW.updateP()
        return NewW



        

#basic test, generate 100 worms,
def LongTest(WormGen):
    if(len(WormGen)==0):
        for x in range(100):
            WormGen.append(Worm(10))
    #do 100 generations
    C=0;
    while True:
        C=C+1
        WormGen.sort(key = lambda x: x.score, reverse = True)
        if(C%100 == 0):
            print('__________________________________')
            for W in WormGen:
                if(W.score!=0):
                    W.PRINT()
       
        #WormGen[0].PRINT()
        NextGen = list()
        QuotaLeft=len(WormGen)
        for i in range(0,len(WormGen),2):
            if(QuotaLeft<=0):
                break
            if(i==0):
                for G in range(int(len(WormGen)*.1)):
                    QuotaLeft=QuotaLeft-1
                    NextGen.append(Worm.Breed(WormGen[0],WormGen[1]))
                #do many breeding
            elif i>(len(WormGen)-len(WormGen)*.2):
                if(len(WormGen[i].Gen)+len(WormGen[i+1].Gen)<WormGen[i].score+WormGen[i+1].score):
                    NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                else:
                    NextGen.append(Worm(10))
                NextGen.append(Worm(10))
                QuotaLeft=QuotaLeft-2
            else:
                #breed 2
                if(len(WormGen[i].Gen)+len(WormGen[i+1].Gen)<WormGen[i].score+WormGen[i+1].score):
                     NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                     NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                else:
                     NextGen.append(Worm(10))
                     NextGen.append(Worm(10))
                QuotaLeft=QuotaLeft-2
        WormGen = list()
        WormGen = NextGen

    return WormGen

def Atest(WormGen):
    if(len(WormGen)==0):
        for x in range(100):
            WormGen.append(Worm(10))
    #do 100 generations
    for x in range(100):
        WormGen.sort(key = lambda x: x.score, reverse = True)
        WormGen[0].PRINT()
        NextGen = list()
        QuotaLeft=len(WormGen)
        for i in range(0,len(WormGen),2):
            if(QuotaLeft<=0):
                break
            if(i==0):
                for G in range(int(len(WormGen)*.1)):
                    QuotaLeft=QuotaLeft-1
                    NextGen.append(Worm.Breed(WormGen[0],WormGen[1]))
                #do many breeding
            elif i>(len(WormGen)-len(WormGen)*.2):
                if(len(WormGen[i].Gen)+len(WormGen[i+1].Gen)<WormGen[i].score+WormGen[i+1].score):
                    NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                else:
                    NextGen.append(Worm(10))
                NextGen.append(Worm(10))
                QuotaLeft=QuotaLeft-2
            else:
                #breed 2
                if(len(WormGen[i].Gen)+len(WormGen[i+1].Gen)<WormGen[i].score+WormGen[i+1].score):
                     NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                     NextGen.append(Worm.Breed(WormGen[i],WormGen[i+1]))
                else:
                     NextGen.append(Worm(10))
                     NextGen.append(Worm(10))
                QuotaLeft=QuotaLeft-2
        WormGen = list()
        WormGen = NextGen
    WormGen.sort(key = lambda x: x.score, reverse = True)
    print('__________________________________')
    for W in WormGen:
        W.PRINT()
    return WormGen

           

def Btest(P):
    P=Worm.Breed(P,P)
    print(str(P.score) +' ::: '+P.P )
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
