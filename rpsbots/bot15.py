import random

kon={'RR':'1','RP':'2','RS':'3','PR':'4','PP':'5','PS':'6','SR':'7','SP':'8','SS':'9'}
k2i={'R':0,'P':1,'S':2}
i2k={0:'R',1:'P',2:'S'}

def mdl(N):
    N%=3
    if N<0:
       N+=3
    return N

if not input:
   DNA=[""]*3
   flag=[False]*5
   hist=[[0]*3]*2
   eval=[0]*3
   subs=[0]*24
   prin=[[0]*24]*3
   meta=[0]*3
   output=random.choice("RPS")
else:
   for i in range(3):
       j=prin[i].index(max(prin[i]))
       if ((j<3 and flag[0]) or (3<=j<6 and flag[1]) or
           (6<=j<12 and flag[2]) or (12<=j<18 and flag[3]) or (j>=18 and flag[4])):
          q=mdl(subs[j]-k2i[input])
          if q==2:
             q=-1
          meta[i]=0.9*meta[i]+1.1*q-0.1
   for j in range(24):
       if ((j<3 and flag[0]) or (3<=j<6 and flag[1]) or
           (6<=j<12 and flag[2]) or (12<=j<18 and flag[3]) or (j>=18 and flag[4])):
          q=mdl(subs[j]-k2i[input])
          if q==2:
             q=-1
          prin[1][j]*=0.9
          prin[2][j]*=0.5
          for i in range(3):
              prin[i][j]+=q
   DNA[0]+=input
   DNA[1]+=output
   DNA[2]+=kon[input+output]
   output=random.choice("RPS")
   for i in range(2):
       for j in range(3):
           hist[i][j]=0
   i=min(26,len(DNA[2]))
   j=-1
   while i>1 and j<0:
         i-=1
         RNA=DNA[2][-i:]
         j=DNA[2].find(RNA,0,-1)
   flag[2]=(j>=0)
   while j>=0:
         q=i+j
         for k in range(2):
             hist[k][k2i[DNA[k][q]]]+=1
         j=DNA[2].find(RNA,j+1,-1)
   for i in range(2):
       flag[i]=(hist[i][0]!=hist[i][1] or hist[i][1]!=hist[i][2])
       if flag[i]:
          for j in range(3):
              eval[j]=hist[i][mdl(j-1)]-hist[i][mdl(j+1)]
          k=eval.index(max(eval))
          for j in range(3):
              subs[3*i+j]=mdl(k-j+i)
   if flag[2]:
      for i in range(2):
          for j in range(3):
              subs[3*i+j+6]=mdl(k2i[DNA[i][q]]-j+i+1)
   for k in range(2):
       i=min(26,len(DNA[2]))
       j=-1
       while i>1 and j<0:
             i-=1
             RNA=DNA[k][-i:]
             j=DNA[k].rfind(RNA,0,-1)
       flag[k+3]=(j>=0)
       if flag[k+3]:
          q=i+j
          for i in range(2):
              for j in range(3):
                  subs[6*k+3*i+j+12]=mdl(k2i[DNA[i][q]]-j+i+1)
   i=meta.index(max(meta))
   if meta[i]>=0:
      j=prin[i].index(max(prin[i]))
      if ((j<3 and flag[0]) or (3<=j<6 and flag[1]) or
          (6<=j<12 and flag[2]) or (12<=j<18 and flag[3]) or (j>=18 and flag[4])):
         output=i2k[subs[j]]