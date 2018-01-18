import requests
from bs4 import BeautifulSoup
import redis
import sys, os
from time import sleep
import getopt


'''
    需要 pip3进行安装 bs4 redis lxml
'''
run_flag = True

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
    ''' 对url进行分析, 将对应内容保存'''
    # 抓取p标签,找得到center就进去,得到两个标签 的 链接, 如果是抓取失败,被拒绝就得不到该链接,就会一直卡在这
    # 应该优化下,回到首页,重新随机化的读取页面,反正已经访问的页面全部记录了

    # 看图页面, 抓取所有p标签,得到图片所在dom然后拿到图片的URL
    p_list = soup.find_all('p')
    print(p_list)
    for temp in p_list:
        temp = str(temp)
        align = getelement(temp, 'align')
        # print("得到的中央组件属性结果",align)
        if align != 'none':
            # 有的图片有了http的前缀, 有的没有,这里进行统一处理
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
            print("URL:",catch_url, '  img:', img_url, '图片区域的HTML代码', temp)
            break
        # print("fsdfsdfs")


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
    # 这个逻辑就是, 如果读取超时,就重新发起一次,如果还是失败,直接终止
    try:
        result = requests.get(url, timeout=4, headers=headers)
    except Exception:
        print("!!!!!!!! 超时等待5s后重试 ......", url)
        try:    
            sleep(5)
            result = requests.get(url, timeout=5, headers=headers)
        except Exception:
            print("第二次重试失败 程序退出")
            sys.exit(1)
    
    print("  ->读取返回状态码",result)
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
    ''' 对url进行解析, 将相关url放在redis中 '''
    soup = readhtml(url)
    #print(soup.prettify())
    read_content(url, soup, conn)

def save_img_url(conn):
    ''' 循环调用deal_html方法, 进行读取Redis中的url '''
    
    # 如果已经成功运行过,那么默认是接着上次继续爬取 如果是第一次就需要输入URL
    url = conn.lindex('no_read',0)
    if url == None:
        url = input("请输入起始URL, 只有一张大图片页面的url")
        conn.lpush('no_read', url)
    
    deal_html(url, conn)
    while run_flag:
        sleep(2)
        # 进入下一轮抓取,不采用递归调用
        # 不使用这种方式是因为,始终里面只有一个元素,如果弹出后面插入,就会被删掉,又新建,会有丢数据的隐患还不稳定
        #last = conn.rpoplpush('no_read', 'readed')
        last = conn.lindex('no_read',0)
        # TODO 优化成zset
        conn.lpush('readed', last) # 加入已爬取列表
        conn.sadd('readed_set', last) # 加入set
        
        print('    ->准备读取下一个URL',last)
        deal_html(last, conn)
        
def param_action(action, param):
    ''' 读取脚本参数调用对应函数'''
    # print(action, param)
    if action == "-h":
        print("-h    脚本参数说明")
        print("缺省   继续爬图")
        print("-d    下载图片")
    if action == "-d":
        print("下载")

def main():
    params = sys.argv
    if len(params) < 2:
        print("参数缺省")
    elif len(params) == 2:
        action = params[1]
        param_action(action, param=None)
        
main()