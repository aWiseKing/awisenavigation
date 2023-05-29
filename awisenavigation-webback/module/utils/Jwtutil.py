import jwt
from datetime import datetime
from time import strptime,mktime,localtime,strftime

class JwtUtil():
    def __init__(self):
        self.jwt = jwt        
        self.key = "awiseking"
        self.effective_time = 1000 * 60
    # 生成token
    def createToken(self,uid,username,password):
        token_group = {
            'some': 'payload',
            'nbf':self.getTimestamp(),
            'exp':self.getTimestamp() * self.effective_time,
            "uid":uid,
            "username":username,
            "password":password
        }
        token = self.jwt.encode(token_group,self.key, algorithm="HS256")
        return token

    # 验证token
    def verifyToken(self,token):
        status = 0
        try:
            self.jwt.decode(token,self.key,algorithms=["HS256"])
        except:
            status = 1
        return status

    # 解密token
    def decryptToken(self,token):
        return self.jwt.decode(token,self.key,algorithms=["HS256"])
    
    # 验证时间
    def verifyTime(self,old_time):
        new_time = self.getTimestamp()
        timec = self.cal_time(old_time,new_time)/60
        if timec > 60:
            return 1
        else:
            return 0

    # 获取当前时间戳
    def getTimestamp(self):
        # 获取当前时间
        times=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 转为时间数组
        timeArray = strptime(times, "%Y-%m-%d %H:%M:%S")
        # 转为时间戳
        timeStamp = int(mktime(timeArray))
        return timeStamp
    
    # 计算时间戳之差
    def cal_time(self,stamp1,stamp2):
        t1 = localtime(stamp1)
        t2 = localtime(stamp2)
        t1= strftime("%Y-%m-%d %H:%M:%S",t1)
        t2 = strftime("%Y-%m-%d %H:%M:%S", t2)
        time1=datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
        timec = time2-time1
        return timec.total_seconds()