# coding:utf-8
import codecs

# with open('README.md','r+',encoding='utf-8') as file_object:
#	contents = file_object.read()
#	print(contents)
read = open('README.md')
links = []
for line in read:
    if line.startswith('- ['):
        #        print(line)
        links.append(line[2:])

for link in links:
    print(link)

tests = ["24.md", "93.md"]
for link in links:
    name = link.split("/")[-1]
    print(name[:-2])
    #    with open("PythonMythLearn/"+name,'a') as temp:
    temp = open("data/" + name[:-2], 'a')
    current_index = links.index(link)
    temp.write("[目录](https://github.com/Kuangcp/GhostPushLight)|" + links[current_index - 1] + "|" + links[
        current_index + 1] + "\n")
    temp.close()
read.close()
# for
