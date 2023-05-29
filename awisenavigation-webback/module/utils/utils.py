from datetime import datetime
from time import strptime,mktime,localtime,strftime

# 将数据处理为统一格式
def responeUtil(data,code:int=200,msg:str="请求成功"):
    respone = {
        "code":code,
        "msg":msg,
        "data":data,
        "timestamp":getTimestamp()
    }
    return respone

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