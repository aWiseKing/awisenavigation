from flask import Flask,request
from config import configs
from module.enity.DB import *
from module.enity.SearchTermStorage import *
from module.enity.bookInfo import *
from module.utils.GetBook import *
from flask_cors import CORS
from module.utils.Jwtutil import JwtUtil
from urllib.request import quote, unquote

app = Flask(__name__)

class RouterConfig:
    
    def __init__(self) -> None:
        CORS(app, supports_credentials=True)
        app.config.from_object(configs["default"])

    def run(self):
        self.search(app)
        self.book(app)
        app.run("0.0.0.0",8887)
    
    jwt_util = JwtUtil()

    """ 搜索框 """
    def search(self,app):

        # 搜索发起记录
        @app.route("/search", methods=["POST"])
        def searchRecord():
            xff = request.headers['X-Forwarded-For'] if "X-Forwarded-For" in request.headers.keys() else "null"
            ip=request.remote_addr if request.remote_addr != "127.0.0.1" else xff
            value = request.form.get("value")
            search_engine = request.form.get("search_engine")
            print(ip,value,search_engine)
            session = Session()
            search_term_storage = SearchTermStorage(ip=ip, search_word =value, search_engine=search_engine)
            session.add(search_term_storage)
            session.flush()
            # 提交状态
            session.commit()
            session.close_all()
            return "1"
    """ 小说 """
    def book(self,app):
        
        # 章节标题和正文
        @app.route("/essay",methods=["POST"])
        def essay():


            return "1"
    
        # 书籍信息
        @app.route("/book/info",methods=["POST"])
        def bookinfo():
            value = request.form.get("value")
            value = unquote(value,encoding="utf-8")
            session = Session()
            book_infos_obj = session.query(BookInfo.bookname,BookInfo.author,BookInfo.brief_info).\
                filter(or_(BookInfo.author.like(f"%{value}%"),BookInfo.bookname.like(f"%{value}%")))
            book_infos = []
            for book_info in book_infos_obj:
                book_infos.append({"title":book_info[0],"author":book_info[1],"brief_info":book_info[2]})

            return json.dumps(book_infos)