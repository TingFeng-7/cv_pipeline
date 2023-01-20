
from loguru import logger
import time
ct = time.time()
local_time = time.localtime(ct)
data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
logger.info(type(data_head))
logger.info(data_head)

import os
print(os.path.realpath(__file__))
a =os.path.split(os.path.realpath(__file__))[1].split(".")[0]
print(a)