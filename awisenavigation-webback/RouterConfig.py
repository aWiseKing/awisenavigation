from flask import Flask,request
from config import configs
from module.enity.DB import *
from module.enity.SearchTermStorage import *
from flask_cors import CORS

app = Flask(__name__)

class RouterConfig:
    
    def __init__(self) -> None:
        CORS(app, supports_credentials=True)
        app.config.from_object(configs["default"])

    def run(self):
        app.run("0.0.0.0",8887)
    
    @app.route("/search", methods=["POST"])
    def index():
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