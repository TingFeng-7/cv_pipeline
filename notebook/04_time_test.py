
from loguru import logger
import time
import os

ct = time.time()
local_time = time.localtime(ct)
data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

print(f'type:{type(data_head)} curr time : {data_head}')

print(f'execute file: {os.path.realpath(__file__)}')
a =os.path.split(os.path.realpath(__file__))
print(f'os.path.split(os.path.realpath(__file__)): {a}')
#可以分离出文件名