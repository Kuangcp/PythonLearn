from ReadURL import ReadURL
import re
from time import sleep
start = open('img/current', 'r').readline()
imgfile = open('img/imgfile'+start, 'a')

# 先执行该脚本,爬取网页得到图片URL, 然后运行 download.sh脚本进行下载
def readImg(index):
    readUrl.url = baseUrl+str(index)+'.html'
    soup = readUrl.readhtml()
    result = soup.find_all('div', class_='location')
    imgType = str(result).split('»')[-1].split('</div>')[0]
    print(imgType)
    
    title = soup.find('h1')
    title = str(title).split('>')[-3].split('<')[0]
    print(title)
    imgfile.write("##"+imgType+"|"+str(index)+"|"+title+"\n")
    content = soup.find_all('img')
    for line in content:
        img = readUrl.getelement(line, 'src')
        print(img)
        # readUrl.downFile(img)
        imgfile.write(img+"\n")

baseUrl = 'https://www.v4f3.com/AAtupian/AAAwz/'
readUrl = ReadURL(baseUrl)
# readImg(126386)
num = 40
end = int(start) - num
for i in range(int(start), end, -1):
    readImg(i)
    # sleep(2)
    # print(i)

current = open('img/current', 'w+')
current.write(str(end))
