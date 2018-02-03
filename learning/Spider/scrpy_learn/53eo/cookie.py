import urllib.request, urllib.parse, urllib.error
import http.cookiejar

LOGIN_URL = 'https://www.v4f3.com/AAtupian/AAAwz/126386.html'
	

values = {'__cfduid': 'd9c560f2fc3a5e24ab2fb60e949705da81517589551', 'fist_user': '1'} 
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
    page = response.read().decode()
    # print(page)
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
print(cookie)
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

get_url = 'http://www.mtupian.com/yazhou/20170908/705/21324.jpg'  # 利用cookie请求訪问还有一个网址
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)
content = get_response.read()
print(content)
with open('8.jpg', "wb") as code:
    code.write(content)