import datetime
from module.enity.DB import *
class BookInfo(Base):
    __tablename__ = "book_info"
    bookid = Column(String(255), primary_key=True,comment="书籍唯一标识")
    bookname = Column(String(255), nullable=False, comment='书名')
    author = Column(String(255), nullable=True, comment='作者')
    brief_info = Column(String(255), nullable=False, comment='简介')
    source = Column(String(255), nullable=True, comment="书籍来源")
    loadtime = Column(DateTime, default=datetime.datetime.now, comment='装载时间')