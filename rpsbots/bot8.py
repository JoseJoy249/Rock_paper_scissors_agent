import random

RNA={'RR':'1','RP':'2','RS':'3','PR':'4','PP':'5','PS':'6','SR':'7','SP':'8','SS':'9'}
mix={'RR':'R','RP':'R','RS':'S','PR':'R','PP':'P','PS':'P','SR':'S','SP':'P','SS':'S'}
rot={'R':'P','P':'S','S':'R'}

if not input:
   DNA=[""]*3
   prin=[random.choice("RPS")]*36
   meta=[random.choice("RPS")]*6
   skor1=[[0]*36,[0]*36,[0]*36,[0]*36,[0]*36,[0]*36]
   skor2=[0]*6
else:
   for j in range(36):
       for i in range(4):
           skor1[i][j]*=0.8
       for i in range(4,6):
           skor1[i][j]*=0.5
       for i in range(0,6,2):
           skor1[i][j]-=(input==rot[rot[prin[j]]])
           skor1[i+1][j]-=(output==rot[rot[prin[j]]])
       for i in range(2,6,2):
           skor1[i][j]+=(input==prin[j])
           skor1[i+1][j]+=(output==prin[j])
       skor1[0][j]+=1.3*(input==prin[j])-0.3*(input==rot[prin[j]])
       skor1[1][j]+=1.3*(output==prin[j])-0.3*(output==rot[prin[j]])
   for i in range(6):
       skor2[i]=0.9*skor2[i]+(input==meta[i])-(input==rot[rot[meta[i]]])
   DNA[0]+=input
   DNA[1]+=output
   DNA[2]+=RNA[input+output]
   for i in range(3):
       j=min(11,len(DNA[2]))
       k=-1
       while j>1 and k<0:
             j-=1
             k=DNA[i].rfind(DNA[i][-j:],0,-1)
       prin[4*i]=DNA[0][j+k]
       prin[4*i+1]=rot[DNA[1][j+k]]
       k=DNA[i].rfind(DNA[i][-j:],0,j+k-1)
       k=k*(k>-1)-j*(k<0)
       prin[4*i+2]=mix[prin[4*i]+DNA[0][j+k]]
       prin[4*i+3]=mix[prin[4*i+1]+rot[DNA[1][j+k]]]
   for i in range(12,36):
       prin[i]=rot[prin[i-12]]
   for i in range(0,6,2):
       meta[i]=prin[skor1[i].index(max(skor1[i]))]
       meta[i+1]=rot[prin[skor1[i+1].index(max(skor1[i+1]))]]
if max(skor2)<1:
   output=random.choice("RPS")
else:
   output=rot[meta[skor2.index(max(skor2))]]
