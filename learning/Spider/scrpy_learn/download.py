from urllib import request
import threading
from time import sleep, ctime
from html import parser


def downjpg(filepath, FileName="default.jpg"):
    try:
        web = request.urlopen(filepath)
        print("访问网络文件" + filepath + "n")
        jpg = web.read()
        DstDir = "/media/kcp/Myth/Linux/result"
        print("保存文件" + DstDir + FileName + "n")
        try:
            File = open(DstDir + FileName, "wb")
            File.write(jpg)
            File.close()
            return
        except IOError:
            print("errorn")
            return
    except Exception:
        print("errorn")
        return


def downjpgmutithread(filepathlist):
    print("共有%d个文件需要下载" % len(filepathlist))
    for file in filepathlist:
        print(file)
    print("开始多线程下载")
    task_threads = []  # 存储线程
    count = 1
    for file in filepathlist:
        t = threading.Thread(target=downjpg, args=(file, "%d.jpg" % count))
        count = count + 1
        task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()  # 等待所有线程结束
    print("线程结束")


class parserLinks(parser.HTMLParser):
    filelist = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    print(value)
                    self.filelist.append(value)
                    # print( self.get_starttag_text() )

    def getfilelist(self):
        return self.filelist


def main(WebUrl):
    # globals flist
    if __name__ == "__main__":
        lparser = parserLinks()
        web = request.urlopen(WebUrl)
        # context= web.read()
        for context in web.readlines():
            _str = "%s" % context
            try:
                lparser.feed(_str)
            except parser.HTMLParseError:
                # print( "parser error")
                pass
        web.close()
        imagelist = lparser.getfilelist()
        # downjpgmutithread(imagelist)
        downjpg("/media/kcp/Myth/Linux/result", 'a.jpg')
        # downjpgmutithread( flist)



WebUrl = "http://t2.55156.com/uploads/allimg/170712/22-1FG21445450-L.jpg"
main(WebUrl)
