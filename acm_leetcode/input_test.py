# ## 
# s=input().strip()
# k=int(input())
# print(f'input : {s}')
# print(f'input : {k}')
# A=[]
# for i in range(len(s)-k):
#     A.append(s[i:i+k])
# if k==1:
#     A=sorted(A,key=lambda x:(x[0]))
# elif k==2:
#     A=sorted(A,key=lambda x:(x[0],x[1]))
# elif k==3:
#     A=sorted(A,key=lambda x:(x[0],x[1],x[2]))
# elif k==4:
#     A=sorted(A,key=lambda x:(x[0],x[1],x[2],x[3]))
# else:
#     A=sorted(A,key=lambda x:(x[0],x[1],x[2],x[3],x[4]))
# print(A[0])

# ## 1.测试组数不固定，每组三行数据
# input = int(input())
# output = input
# print(str(output))

 ## 2.单行多个输入，单行多个输出，空格分割 (多行输入，每一行是一个测试样例)
# inputs = list(map(int, input().split(" ")))
# nums, operations = inputs[0], inputs[1]
# # print(str(nums), str(operations))
# power = list(map(int, input().split(" ")))
# while operations!=0:
#     inputs = list(map(int, input().split(" ")))
#     name, k = inputs[0], inputs[1]
#     # print(power[:k])
#     tmp = power[:k]
#     if name==1:
#         tmp.sort()
#         power[:k] = tmp
#         # print(f'name:{name}:从小到大 {power}')
#     elif name==2:
#         tmp.sort(reverse=True) #act #cheack
#         power[:k] = tmp
#         # print(f'name:{name}:从大到小 {power}') 
#     operations-=1

# s=""
# for i in range(nums):
#     s+=str(power[i])
#     if i != nums-1:
#         s+=" "
# print(s)

# print('end')
# print(f'power: {power}')

## 3.多个测试案例，每个测试案例多行
# while 1:
#     nm = list(map(int,input().split(" ")))
#     N = nm[0]
#     M = nm[1]
#     print(str(N)+' '+str(M))
#     for i in range(M):
#         abc = list(map(int, input().split(" ")))
#         a, b, c = abc[0], abc[1], abc[2]
#         print(str(a)+'_'+str(b)+'_'+str(c))

inputs = list(map(int, input().split(" ")))
L, R = inputs[0], inputs[1]
digits=0
if R<10:
    print(str(R))
else:
    tmp = R
    while tmp:
        tmp = tmp//10
        digits+=1
    digits-=1
    print(f'{(pow(10,digits)-1)}* 9 *{digits}')    
    print(str((pow(10,digits)-1)*9*(digits-1)))