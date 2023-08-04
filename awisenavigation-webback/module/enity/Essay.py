import datetime
from module.enity.DB import *
class Essay(Base):
    __tablename__ = "Essay"
    id = Column(Integer, primary_key=True,autoincrement=True)
    bookid = Column(String(255), comment="书籍唯一标识")
    volume = Column(String(255), comment="卷名")
    volume_num = Column(Integer, comment="卷顺序")
    essay_num = Column(Integer, comment="章节顺序")
    title = Column(String(255), nullable=False, comment='章节名')
    content = Column(Text, nullable=True, comment='章节内容')
    loadtime = Column(DateTime, default=datetime.datetime.now, comment='装载时间')