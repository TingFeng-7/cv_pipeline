## 
s=input().strip()
k=int(input())
print(f'input : {s}')
print(f'input : {k}')
A=[]
for i in range(len(s)-k):
    A.append(s[i:i+k])
if k==1:
    A=sorted(A,key=lambda x:(x[0]))
elif k==2:
    A=sorted(A,key=lambda x:(x[0],x[1]))
elif k==3:
    A=sorted(A,key=lambda x:(x[0],x[1],x[2]))
elif k==4:
    A=sorted(A,key=lambda x:(x[0],x[1],x[2],x[3]))
else:
    A=sorted(A,key=lambda x:(x[0],x[1],x[2],x[3],x[4]))
print(A[0])
## 1.测试组数不固定，每组三行数据
while True:
    n, m = map(int, input().split())
    a = [int(c) for c in input().split()]
    b = [int(d) for d in input().split()]
    c = list(set(a + b))
    c.sort()
    for i in range(len(c)):
        print(c[i], end=' ')
 ## 2.测试组数不定，输入数据中有指定行数的多行输入（赛码网找老乡题最完美答案）
#  while True:
#     N, M = map(int, input().split())
#     a = []
#     b = set()
#     for _ in range(M):
#         a = list(map(int, input().split()))
#         if a[2] == 1:
#             b.add(a[0])
#             b.add(a[1])
#     if 1 in b:
#         print(len(b) - 1)
#     else:
#         print(0)
## 3.一组数据，有指定行数的多行输入，必须先将多行输入整合到一起的情况