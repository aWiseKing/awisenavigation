import requests
import js2py
import ssl
import json
class GetEssay:
    """ 该类用于获取小说的章节，为各类站点获取小说章节的基类 """
    def __init__(self) -> None:
        self.jdata = {"title":None,"essay":None}
        self.title = None
        self.essay = None
    def request(self):
        ...
    
    def setJdata(self):
        self.jdata["title"] = self.title
        self.jdata["essay"] = self.essay
        

    def start(self):
        self.request()
        self.setJdata()

class GetSNDEssay(GetEssay):
    """ 获取少年梦阅读的小说章节 """
    def __init__(self):
        super().__init__()

    def request(self,book_chapter_id):
        """获取少年梦阅读的小说章节
        通过传入某章节的id获取当前章节的标题（title）和正文（essay）
        Keyword arguments:
        book_chapter_id -- 章节id
        Return: jdata -- 一个字典，包括标题（title）和正文（essay）
        """
        from module.utils.base64js import base64js
        ssl._create_default_https_context = ssl._create_unverified_context

        book_chapter_id = book_chapter_id

        url = f"https://www.shaoniandream.com/readchapter/{book_chapter_id}"

        payload = "-----011000010111000001101001--\r\n\r\n"
        headers = {
            "Cookie": "Hm_lvt_79e51ba08bd734f72224ccd0de30c8b0=; PHPSESSID=8nrf8g1phblpm34u4dveddnf70; saveMemberInfo={\"username\":\"17365575446\",\"password\":\"xiaoqian\"}",
            "content-type": "multipart/form-data; boundary=---011000010111000001101001"
        }

        response = requests.request("GET", url, data=payload, headers=headers,verify=False)

        data = response.text
        caonima = data.split("// 鼠标")[0].split("\",\"\",\"")[1].split("\"")[0]
        response.close()

        url = f"https://www.shaoniandream.com/booklibrary/membersinglechapter/chapter_id/{book_chapter_id}"

        payload = {
            "sign": "a3NvcnQoPPJHBhcmEpOw==",
            "caonima": caonima
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "sec-ch-ua-mobile": "?0",
            "Content-Length": "72",
            "sec-ch-ua-platform": "\"Windows\"",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.shaoniandream.com",
            "Pragma": "no-cache",
            "Referer": f"https://www.shaoniandream.com/readchapter/{book_chapter_id}",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "Cookie": "Hm_lvt_79e51ba08bd734f72224ccd0de30c8b0=; PHPSESSID=8nrf8g1phblpm34u4dveddnf70; saveMemberInfo={\"username\":\"17365575446\",\"password\":\"xiaoqian\"}",
            "content-type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers,verify=False)
        data = json.loads(response.text)
        if data["status"] == 2:
            self.title = data["msg"]

        if data["status"] == 1:
            base64js = base64js
            self.title = data["data"]["title"]
            self.essay = ""
            for line in data["data"]["show_content"]:
                content = line["content"]
                base64js = f"{base64js}\nrun('{content}')"
                mcontent = js2py.eval_js(base64js)
                self.essay += f"{mcontent}\n"
    
    def start(self,book_chapter_id):
        self.request(book_chapter_id)
        self.setJdata()
        return self.jdata
    
class GetBook:
    """ 获取书籍信息的基类 记录流程 搜索图书——>查找数据库——>自动切换引擎寻书——>存在则记录入数据库（书名，作者名，来源，简介，书籍id） """
    def __init__(self) -> None:
        self.books = []
        self.bdata = {"title":None,"book_id":None,"author":None,"brief_info":None,"source":None}
        self.title = None
        self.book_id = None
        self.author = None
        self.brief_info = None
        self.source = None
    def request(self):
        ...
    
    def setbdata(self):
        self.bdata["title"] = self.title
        self.bdata["book_id"] = self.book_id
        self.bdata["author"] = self.author
        self.bdata["source"] = self.source
        self.bdata["brief_info"] = self.brief_info
        self.books.append(self.bdata.copy())
        

    def start(self):
        self.request()
        self.setbdata()

class GetSNDBook(GetBook):
    """ 获取少年梦书籍信息 """
    def __init__(self) -> None:
        super().__init__()
        
        self.source = None
    
    def request(self,page = 1):
        from lxml import etree
        """ 获取少年梦的书籍的信息 """

        url = "http://www.shaoniandream.com/library"

        querystring = {"page":f"{page}"}

        payload = "-----011000010111000001101001--\r\n\r\n"
        headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.text
        
        data = etree.HTML(data)
        booklist= data.xpath("//div[@class='BookPicList']/ul/li/dl")
        print(booklist)
        for book_path in booklist:
            self.title = book_path.xpath("dd[@class='title']/a")[0].text
            self.book_id = book_path.xpath("dd[@class='title']/a")[0].text
            self.author = book_path.xpath("dd[@class='author']/a")[0].text
            self.brief_info = "少年梦"        


            