# 创建一个  database.py

声明和创建数据库
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db')
## /// 相对路径（相对于当前文件位置） //// 绝对路径
db_session = scoped_session(sessionmaker(autocommit=False,  autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
```

声明表字段

``` modes.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'user_org'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
```


创建数据库方法

终端 pyhton3 或者 python 进入cmd 编辑模式
# 引入 init_db 方法创建数据库
from database import init_db
# 引入数据库连接操作方法
from database import db_session
# 引入抽象模型
from models import User

# 初始化数据库 创建数据库
init_db()
# 声明数据 u
u = User('admin', 'admin@localhost')
# 添加数据
db_session.add(u)
# 提交数据
db_session.commit()
# 查询全部数据
User.query.all()
# 查询 name 为 admin 的第一个数据
User.query.filter(User.name == 'admin').first()