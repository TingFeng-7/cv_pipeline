with open('files0.txt', 'r') as file1:
    content1 = file1.readlines()

# 读取第二个txt文件内容
with open('files1.txt', 'r') as file2:
    content2 = file2.readlines()

# 移除换行符并转为集合
content1 = set([line.strip() for line in content1])
content2 = set([line.strip() for line in content2])

# 求差集
difference = content1 - content2
# 将差集写入新的txt文件
with open('difference.txt', 'w') as file_diff:
    for item in difference:
        file_diff.write(item + '\n')