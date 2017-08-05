# coding:utf-8
import codecs

# 读取readme文件
read = open('README.md')
links = []
for line in read:
    if line.startswith('- ['):
        #        print(line)
        links.append(line[2:])

for link in links:
    # print(link)
    print("- " + link.split("]")[0] + "](./data/" + link.split("/")[-1].rstrip())
