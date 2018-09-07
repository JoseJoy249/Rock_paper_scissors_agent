import random

kon={'RR':'1','RP':'2','RS':'3','PR':'4','PP':'5','PS':'6','SR':'7','SP':'8','SS':'9'}
d0s={'1':0,'2':0,'3':0,'4':1,'5':1,'6':1,'7':2,'8':2,'9':2}
d1s={'1':0,'2':1,'3':2,'4':0,'5':1,'6':2,'7':0,'8':1,'9':2}
k2i={'R':0,'P':1,'S':2}
i2k={0:'R',1:'P',2:'S'}

def mdl(N):
    N%=3
    if N<0:
       N+=3
    return N

if not input:
   DNA=""
   mRNA=""
   tRNA=""
   flag=[False]*7
   hist=[[0]*3]*4
   eval=[0]*3
   subs=[0]*30
   prin=[[0]*30]*3
   meta=[0]*3
   output=random.choice("RPS")
else:
   for i in range(3):
       j=prin[i].index(max(prin[i]))
       if ((j<3 and flag[0]) or (j>=3 and j<6 and flag[1]) or
           (j>=6 and j<9 and flag[2]) or (j>=9 and j<12 and flag[3]) or
           (j>=12 and j<18 and flag[4]) or (j>=18 and j<24 and flag[5]) or (j>=24 and flag[6])):
          k=mdl(subs[j]-k2i[input])
          if k==2:
             meta[i]-=1
          else:
             meta[i]+=k
   for j in range(30):
       if ((j<3 and flag[0]) or (j>=3 and j<6 and flag[1]) or
           (j>=6 and j<9 and flag[2]) or (j>=9 and j<12 and flag[3]) or
           (j>=12 and j<18 and flag[4]) or (j>=18 and j<24 and flag[5]) or (j>=24 and flag[6])):
          prin[1][j]*=0.9
          k=mdl(subs[j]-k2i[input])
          if k==1:
             for i in range(3):
                 prin[i][j]+=1
          elif k==2:
             for i in range(3):
                 if i<2:
                    prin[i][j]-=1
                 elif prin[i][j]<3:
                    prin[i][j]-=1.5
                 else:
                    prin[i][j]*=0.5
          elif prin[2][j]<3:
             prin[2][j]-=0.25
          else:
             prin[2][j]=0.75*prin[2][j]+0.5
   DNA+=kon[input+output]
   mRNA+=output
   tRNA+=input
   for i in range(4):
       for j in range(3):
           hist[i][j]=0
   i=min(25,len(DNA))
   j=-1
   w=0
   while i>1 and j<0:
         i-=1
         RNA=DNA[-i:]
         j=DNA.find(RNA,0,-1)
   flag[4]=(j>=0)
   while j>=0:
         k=i+j
         w+=1
         hist[0][d0s[DNA[k]]]+=1
         hist[1][d1s[DNA[k]]]+=1
         hist[2][d0s[DNA[k]]]+=w
         hist[3][d1s[DNA[k]]]+=w
         j=DNA.find(RNA,j+1,-1)
   if flag[4]:
      j=d0s[DNA[k]]+1
      k=d1s[DNA[k]]-1
      for i in range(3):
          subs[i+12]=mdl(j-i)
          subs[i+15]=mdl(k-i)
   for i in range(4):
       flag[i]=(hist[i][0]!=hist[i][1] or hist[i][1]!=hist[i][2])
       if flag[i]:
          for j in range(3):
              eval[j]=hist[i][mdl(j-1)]-hist[i][mdl(j+1)]
          k=eval.index(max(eval))
          for j in range(3):
              subs[3*i+j]=mdl(k-j+i%2)
   i=min(25,len(DNA))
   j=-1
   while i>1 and j<0:
         i-=1
         RNA=tRNA[-i:]
         j=tRNA.rfind(RNA,0,-1)
   flag[5]=(j>=0)
   if flag[5]:
      k=k2i[mRNA[i+j]]-1
      j=k2i[tRNA[i+j]]+1
      for i in range(3):
          subs[i+18]=mdl(j-i)
          subs[i+21]=mdl(k-i)
   i=min(25,len(DNA))
   j=-1
   while i>1 and j<0:
         i-=1
         RNA=mRNA[-i:]
         j=mRNA.rfind(RNA,0,-1)
   flag[6]=(j>=0)
   if flag[6]:
      k=k2i[mRNA[i+j]]-1
      j=k2i[tRNA[i+j]]+1
      for i in range(3):
          subs[i+24]=mdl(j-i)
          subs[i+27]=mdl(k-i)
   i=meta.index(max(meta))
   j=prin[i].index(max(prin[i]))
   if ((j<3 and flag[0]) or (j>=3 and j<6 and flag[1]) or
       (j>=6 and j<9 and flag[2]) or (j>=9 and j<12 and flag[3]) or
       (j>=12 and j<18 and flag[4]) or (j>=18 and j<24 and flag[5]) or (j>=24 and flag[6])):
      output=i2k[subs[j]]
   else:
      output=random.choice("RPS")
