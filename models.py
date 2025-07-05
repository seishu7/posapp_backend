from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, ForeignKey
from .database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "商品マスタ"
    PRD_ID = Column(Integer, primary_key=True, autoincrement=False)
    CODE = Column(CHAR(13), unique=True, nullable=False)
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

class Transaction(Base):
    __tablename__ = "取引"
    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    DATETIME = Column(TIMESTAMP, nullable=False)
    EMP_CD = Column(CHAR(10), nullable=False)
    STORE_CD = Column(CHAR(5), nullable=False)
    POS_NO = Column(CHAR(3), nullable=False)
    TOTAL_AMT = Column(Integer, nullable=False)
    TTL_AMT_EX_TAX = Column(Integer, nullable=False)

class TransactionDetail(Base):
    __tablename__ = "取引明細"
    TRD_ID = Column(Integer, ForeignKey("取引.TRD_ID"), primary_key=True)
    DTL_ID = Column(Integer, primary_key=True)
    PRD_ID = Column(Integer, ForeignKey("商品マスタ.PRD_ID"))
    PRD_CODE = Column(CHAR(13))
    PRD_NAME = Column(String(50))
    PRD_PRICE = Column(Integer)
    TAX_CD = Column(CHAR(2))
