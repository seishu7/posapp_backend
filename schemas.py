from pydantic import BaseModel
from typing import List, Optional

class ProductOut(BaseModel):
    PRD_ID: int
    CODE: str
    NAME: str
    PRICE: int
    class Config:
        orm_mode = True

class TransactionProductIn(BaseModel):
    PRD_ID: int
    CODE: str
    NAME: str
    PRICE: int

class TransactionIn(BaseModel):
    emp_cd: Optional[str] = "9999999999"
    products: List[TransactionProductIn]
