from ReadURL import ReadURL

readUrl = ReadURL('http://53eo.com/htm/2018/1/22/p02/397336.html')
soup = readUrl.readhtml()
img_list = soup.find_all('img')
for img in img_list:
    print(img)
    url = readUrl.getelement(img, 'scr')
    readUrl.downFile(url)
    print()