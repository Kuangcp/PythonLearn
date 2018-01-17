import requests
from bs4 import BeautifulSoup
import redis
import sys, os
from time import sleep
import getopt
import threading
import time
from tkinter import *

'''
    针对该网址进行爬取 http://www.55156.com/tag/ 先得到标签,然后再去爬取 其实就是模仿点击事件
    sudo pip3 bs4 redis tkinter
'''
# run_flag = True

def getconn():
    return redis.Redis(host='localhost', port=6379, db=0)

# 从标签中获取指定属性的值
def getelement(line, element):
    log = open('debug.log','w+')
    
    elements = line.split(' ')
    for ele in elements:
        if ele.startswith(element):
            return ele.split('"')[1]
    log.write("------ "+line+"没有属性"+element+"\n")
    return 'none'
    
# 原有的思路是得到所有的URL,作为下一步的目标,得到当前页的所有图片然后筛选,然后突然发现这个直接从p中就可以自动一级级的跳转
# 只要指定入口URL即可,可以进一步优化,获取所有tag, 然后输入感兴趣的tag,然后跳到tag主页,得到第一个具体帖子的URL,就可以开始一级级的跳转了


# 判断是否已经访问过 , 加上判断类别,指定类别进行抓取(返回True就是过滤掉)
def already_read(href, conn):
    #print('判断的链接'+href)
    #tu_type = 'siwameinv'
    #print('判断:'+href)
    if type(href) == bytes:
        href = href.decode('utf-8')
    #if href.count(tu_type) == 0 :
        #return True
    return conn.sismember('readed_set',str(href))
    

def get_urlhead(url):
    #print('获取头', type(url))
    if type(url)==bytes:
        url = url.decode('utf-8')
    # 思路实现: 先切分,将最后那个html名字替换成空串 就好了
    result = url.split('/')
    htmls = result[-1]
    url = url.replace(htmls, '')
    return url


def read_content(url, soup, conn):
    # 抓取p标签,找得到center就进去,得到两个标签 的 链接, 如果是抓取失败,被拒绝就得不到该链接,就会一直卡在这
    # 应该优化下,回到首页,重新随机化的读取页面,反正已经访问的页面全部记录了
    p_list = soup.find_all('p')
    for temp in p_list:
        temp = str(temp)
        align = getelement(temp, 'align')
        #print("得到的中央组件属性结果",align)
        if not align == 'none':
            # 存在已经就有了HTTP的情况
            catch_url = getelement(temp, 'href')
            if not catch_url.startswith('http'):
                catch_url = get_urlhead(url)+catch_url
            
            
            # 保存链接先,如果访问过,还是要继续循环下去(相当于浪费了时间)
            conn.lpush('no_read', catch_url)
            conn.rpop('no_read')
            # TODO 跳回首页
            if already_read(catch_url, conn):
                break
            img_url = getelement(temp, 'src')
            conn.sadd('images',img_url)
            #print("URL:",catch_url, '  img:', img_url)
            #print('得到中央大图区域',temp)
            break


# 发起请求并进行解析,处理超时,定义Header
def readhtml(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language' : 'zh-CN,en-US;q=0.7,en;q=0.3'
                #'' : '',
                #'' : '',
               }
    print('-'*30)
    print('尝试读取 URL',url)
    # line('尝试读取 URL'+url.decode('utf-8'))
    listbox.insert(ANCHOR, '尝试读取 URL'+url.decode('utf-8')) 
    # 这个逻辑就是, 如果读取超时,就重新发起一次,如果还是失败,直接终止
    try:
        result = requests.get(url, timeout=4, headers=headers)
    except Exception:
        print("!!!!!!!! 超时等待5s后重试 ......", url)
        listbox.insert(ANCHOR, "!!!!!!!! 超时等待5s后重试 ......"+url.decode('utf-8'))
        try:    
            sleep(5)
            result = requests.get(url, timeout=5, headers=headers)
        except Exception:
            print("第二次重试失败 程序退出")
            listbox.insert(ANCHOR, "第二次重试失败 程序退出")
            sys.exit()
            # return 0
    
    print("  ->读取返回状态码",result)
    # line("  ->读取返回状态码"+str(result))
    listbox.insert(ANCHOR, "  ->读取返回状态码"+str(result)) 
    if str(result) == '<Response [200]>':
        pass
    elif str(result).startswith('<Response [4'):
        print("页面不存在,请检查输入") # 无法继续
        sys.exit(1)
    elif str(result).startswith('<Response [5'):
        print("服务器连接超时, 请等待....")
        sleep(10)
    result.encoding = "utf-8"
    soup = BeautifulSoup(result.text, 'lxml')
    return soup
  
# 处理解析结果
def deal_html(url, conn):
    soup = readhtml(url)
    #print(soup.prettify())
    conn.hset('HTML',url, soup.prettify())
    # 分离出里面的元素
    #save_image(soup, conn)
    #read_url(url, soup, conn)
    read_content(url, soup, conn)
    
# 得到标签    
def get_tags(conn,home):
    tags_url = 'http://www.55156.com/tag/'
    soup = readhtml(tags_url)
    div_list = soup.find_all('div')
    list = []
    for div in div_list:
        div = str(div)
        div_class = getelement(div, 'class')
        #print('class:',div_class)
        if div_class == 'tags_list':
            #print(div)
            div = BeautifulSoup(div, 'lxml')
            list += div.find_all('a')
            
    conn.delete('tags')
    conn.delete('tag_list')
    for a in list:
        #print(a)
        a = str(a)
        # 还要处理只有图片没有标题的 情况,,,例如小图标
        href = getelement(a, 'href')
        title = getelement(a, 'title')
        if href=='none' or title=='none':
            continue
        conn.hset('tags',  title,home+href)
        conn.lpush('tag_list', home+href)
    print('读取标签成功')

# def get_more_img(conn, run_flag):
#     # 确定类别
#     siwameinv = 'http://www.55156.com/a/siwameinv/'
    
#     # 也就是说,如果已经运行过,那么默认是按着上次未完成的,继续爬取
#     # 如果是第一次就需要输入URL
#     url = conn.lindex('no_read',0)
#     if url == None:
#         url = input("请输入起始URL")
    
#     deal_html(url, conn)
#     # TODO 退出条件？？？
    
#     while run_flag:
#         sleep(2)
#         # 进入下一轮抓取,不采用递归调用
#         # 不使用这种方式是因为,始终里面只有一个元素,如果弹出后面插入,就会被删掉,又新建,会有丢数据的隐患还不稳定
#         #last = conn.rpoplpush('no_read', 'readed')
#         last = conn.lindex('no_read',0)
#         conn.lpush('readed', last) # 加入已爬取列表
#         conn.sadd('readed_set', last)
        
#         print('    ->准备读取下一个URL',last)
#         deal_html(last, conn)
        
# 输入类别,然后得到方向 URL 是想每次输入不同的类别,就能有针对性的抓取,然后再下载
def catch_tags(conn):
    tags = conn.hkeys('tags')
    tags.sort()
    temp = ''
    count = 0
    for tag in tags:
        count += 1
        temp += tag.decode('utf-8')+' | '
        if count%9==0:
            print(temp)
            temp = ''
    choose = input("请输入你要的类别: ")
    target = 'none'
    for tag in tags:
        tag = tag.decode('utf-8')
        if tag.count(choose) == 1:
            target = tag
            break
    if target == 'none':
        print('>>>>> 没有找到对应的类别')
        catch_tags(conn)
    
    tag_url = conn.hget('tags', target )
    print(target, ' : ', str(tag_url))
    #deal_html(tag_url, conn)
    return tag_url.decode('utf-8')

# def main():
#     conn = getconn()
#     # 读取参数 t 是读取标签 默认是继续上次的抓取
#     opts, args = getopt.getopt(sys.argv[1:], 'td')
#     for op,value in opts:
#         if op == "-d":
#             catch_tags(conn)
#             sys.exit(0)
#         if op == "-t":
#             #print('获取分类')
#             get_tags(conn, home)
#             sys.exit(0)
    
#     # 缺省
#     get_more_img(conn)
home = 'http://www.55156.com'




# main()
# tkf.button('开始', main)




class Application(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.thread_stop = False  
    
    def run(self):
         self.main_get()

    def main_get(self):
        conn = getconn()
        self.get_more_img(conn)

    def stop(self):  
        print('按下结束')
        self.thread_stop = True  

    def get_more_img(self,conn):
        siwameinv = 'http://www.55156.com/a/siwameinv/'
        url = conn.lindex('no_read',0)
        if url == None:
            url = input("请输入起始URL")
        
        deal_html(url, conn)
        while not self.thread_stop:
            sleep(2)
            last = conn.lindex('no_read',0)
            conn.lpush('readed', last) # 加入已爬取列表
            conn.sadd('readed_set', last)
            print('    ->准备读取下一个URL',last)
            # line('    ->准备读取下一个URL'+last.decode('utf-8'))
            # listbox.insert(ACTIVE, '    ->准备读取下一个URL'+last.decode('utf-8'))
            
            deal_html(last, conn)
        print('退出下载循环')
        line('退出下载循环')

a = Application(12)


def frame():
    root.mainloop()

def line(text):
    Label(root, text=text).pack()

def button(text, func):
    Button(root, text=text, command=func).pack(side=TOP)

def get_screen_size(window):  
    return window.winfo_screenwidth(),window.winfo_screenheight()  
  
def get_window_size(window):  
    return window.winfo_reqwidth(),window.winfo_reqheight()  
  
def center_window(root, width, height):  
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
    print(size)  
    root.geometry(size) 

root = Tk()
# 滑动条
scrollbar = Scrollbar(root)  
scrollbar.pack(side=RIGHT, fill=Y)  
listbox = Listbox(root, yscrollcommand=scrollbar.set)   
listbox.pack(side=BOTTOM, fill=BOTH)  
scrollbar.config(command=listbox.yview) 

root.title('爬取URL')  
center_window(root, 400, 240) 
root.maxsize(600, 400)  
root.minsize(300, 240)
button('开始', a.start)
button('重试', a.main_get)
button('结束', a.stop)
frame()