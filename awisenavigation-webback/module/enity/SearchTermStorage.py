import datetime
from module.enity.DB import *
class SearchTermStorage(Base):
    __tablename__ = "SearchTermStorage"
    id = Column(Integer, primary_key=True,autoincrement=True)
    ip = Column(String(50), nullable=False, comment='来源ip')
    search_word = Column(String(255), nullable=True, comment='关键词')
    search_engine = Column(String(255), nullable=False, comment='搜索引擎')
    loadtime = Column(DateTime, default=datetime.datetime.now, comment='更新时间')