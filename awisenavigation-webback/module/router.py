from flask import request,make_response
from random import randint
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from time import strptime,mktime,localtime,strftime
from module.utils.Jwtutil import JwtUtil
from module.utils.utils import *
from module.enity.Account import session,Account
from module.enity.User import User
from module.utils.PWencryptionutil import PWEncryptionUtil
from random import randint
from sqlalchemy.exc import IntegrityError

jwt_util = JwtUtil()
PW_encryption_util = PWEncryptionUtil()

""" 用户认证 """
def loginVerify(app):

    # 路由：用户登录
    @app.route('/api/login', methods=["GET","POST"])
    def login():
        msg = "登录成功"
        code = 200
        data = ""
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            accounts = session.query(Account,User).join(User,User.id == Account.uid).filter(Account.username == username,User.isdel == 0)
            accounts = session.query(Account,User).join(User,User.id == Account.uid).filter(Account.username == username,User.isdel == 0)
            if judgeAccountExists(accounts.all()): # 验证账户是否存在
                account = accounts.one().Account
                db_password = PW_encryption_util.decrypt(account.password,account.nonce,account.tag)
                password_verify = PW_encryption_util.verifyPlainText(password,db_password)
            else:
                code=901
                msg="账户或密码错误"
                return responeUtil(data=data,code=code,msg=msg)

            if password_verify: # 验证密码是否正确
                uid = account.uid
                token = jwt_util.createToken(uid,username, db_password)
                data = token
            else :
                code=901
                msg="账户或密码错误"
            
            return responeUtil(data=data,code=code,msg=msg)
    
    # 路由：token认证
    @app.route("/api/verify/token", methods=["GET","POST"])
    def tokenVerify():
        msg = "认证成功"
        code = 200
        data = ""
        if request.method == "POST":
            token = request.form.get("token")
            user_data = jwt_util.decryptToken(token) if jwt_util.verifyToken(token) == 0 else 0
            if user_data == 0:
                msg = "用户信息过期，请重新登录"
                code = 901
            else :
                username = user_data["username"]
                password = user_data["password"]
                loginVerify(msg,code,data,username,password)
                

        return responeUtil(data=data,code=code,msg=msg)

    # 判断是否存在该用户
    def judgeAccountExists(accounts) -> bool:
        if len(accounts) <1:
            return False
        else:
            return True

    # 账户验证
    def loginVerify(msg,code,data,username,password) -> None:
        accounts = session.query(Account,User).join(User,User.id == Account.uid).filter(Account.username == username,User.isdel == 0)
        if judgeAccountExists(accounts.all()): # 验证账户是否存在
            account = accounts.one().Account
            db_password = PW_encryption_util.decrypt(account.password,account.nonce,account.tag)
            password_verify = PW_encryption_util.verifyPlainText(password,db_password)
        else:
            code=901
            msg="账户或密码错误"
            return responeUtil(data=data,code=code,msg=msg)

        if password_verify: # 验证密码是否正确
            uid = account.uid
            token = jwt_util.createToken(uid,username, db_password)

        else :
            code=901
            msg="账户或密码错误"
        
""" 用户注册 """
def registerUser(app):

    #路由：用户注册
    @app.route('/api/register', methods=["GET","POST"])
    def register():
        msg = "注册成功"
        code = 200
        data = ""
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            nickname = (request.form.get("nickname") if len(request.form.get("nickname")) > 0 else str(randint(10000,99999)))
            email = request.form.get("email")
            ciphertext_b64,nonce_b64,tag_b64 = PW_encryption_util.encrypt(password)
            # 加入事物
            try:
                user = User(nickname=nickname, email=email)
                session.add(user)
                session.flush()
                uid = user.id
                account = Account(uid=uid,username=username,password=ciphertext_b64,nonce=nonce_b64,tag=tag_b64)
                session.add(account)
                session.flush()
                # 提交状态
                session.commit()
            except IntegrityError:
                msg = "账户已经存在"
                code = 901
                session.rollback()
            # 返回状态
            return responeUtil(data=data,code=code,msg=msg)

""" 验证码 """
def verifyCode(app):
    num = {}

    # 路由：发送验证码图片
    @app.route("/api/verifycode", methods=["GET"])
    def verifyImg():
        cleanNum()
        if request.method == "GET":
            uuid = request.args.get("uuid")
            code_str = randString()
            num[uuid] = {"str":code_str,"time":getTimestamp()}
            img=createVerifyCodeImg(code_str)
            out = BytesIO()
            img.save(out, 'png')
            out.seek(0)
            resp = make_response(out.read())
            resp.content_type = 'image/png'
            return resp
    
    # 路由：校验验证码
    @app.route("/api/code/verify", methods=["GET"])
    def verifyCode():
        msg = "验证码有误"
        code = 901
        data = ""
        cleanNum()
        if request.method == "GET":
            try:
                uuid = request.args.get("uuid")
                code = request.args.get("code").lower()
                if uuid not in num.keys():
                    code = 901
                code_str = num[uuid]["str"].lower()
                if code_str == code:
                    msg = "验证成功"
                    code = 200
                    num.pop(uuid)
                else:
                    code = 901
            except KeyError:
                    code = 901
        return responeUtil(data=data,code=code,msg=msg)
    
    # 生成随机字符
    def randString(str_len=6):
        str_len = str_len
        code_str = ""
        for i in range(0, str_len):
            str_type = randint(0,2)
            if str_type == 0:
                code_str = code_str+chr(randint(65,90))
            elif str_type == 1:
                code_str = code_str+chr(randint(97,122))
            elif str_type == 2:
                code_str = code_str+str(randint(0,9))
        return code_str

    # 随机颜色RGB
    def get_random_color():
        return randint(120, 200), randint(120, 200), randint(120, 200)
    
    # 生成验证码图片
    def createVerifyCodeImg(code_str):
        width = 140
        height = 60
        img = Image.new("RGB",(width, height), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./state/font/grid.ttf', size=36)
        gr_font = ImageFont.truetype('./state/font/hymmnos.ttf', size=36)
        gr_ho = randString()

        # 绘制文字
        for i in range(0,len(code_str)):
            c = code_str[i]
            rand_len = randint(-2, 2)
            
            draw.text((width * 0.15 * (i) + rand_len, height * 0.2 + rand_len), c, font=font, fill=get_random_color())

        # 绘制干扰文字
        for i in range(0,len(gr_ho)):
            c = code_str[i]
            rand_len = randint(-5, 5)
            x1 = randint(0, width)
            y1 = randint(0, height)
            draw.text((x1, y1), c, font=gr_font, fill=get_random_color())

        # 加入干扰线
        for i in range(3):
            x1 = randint(0, width)
            y1 = randint(0, height)
            x2 = randint(0, width)
            y2 = randint(0, height)
            draw.line((x1, y1, x2, y2), fill=get_random_color())

        # 加入干扰点
        for i in range(16):
            draw.point((randint(0, width), randint(0, height)), fill=get_random_color())
        return img
    
    # 获取当前时间戳
    def getTimestamp():
        # 获取当前时间
        times=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 转为时间数组
        timeArray = strptime(times, "%Y-%m-%d %H:%M:%S")
        # 转为时间戳
        timeStamp = int(mktime(timeArray))
        return timeStamp

    # 计算时间戳之差
    def cal_time(stamp1,stamp2):
        t1 = localtime(stamp1)
        t2 = localtime(stamp2)
        t1= strftime("%Y-%m-%d %H:%M:%S",t1)
        t2 = strftime("%Y-%m-%d %H:%M:%S", t2)
        time1=datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
        timec = time2-time1
        return timec.total_seconds()

    # 清理内存
    def cleanNum():
        new_timestamp = getTimestamp()
        tmp_lst = []
        for i in num.keys():
            value = num[i]
            if cal_time(value["time"],new_timestamp)/60 >= 10:
                tmp_lst.append(i)
        for i in tmp_lst:
            num.pop(i)

""" Home页面 """
def homePage(app):

    # 路由：发送用户个人信息
    @app.route('/route_name')
    def userData():
        pass