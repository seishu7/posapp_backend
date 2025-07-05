from sqlalchemy.orm import Session
from . import models
from . import schemas
from datetime import datetime
print("✔ datetime successfully imported in crud.py")
print("✔ current time is", datetime.now())

def get_product_by_code(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.CODE == code).first()

def register_transaction(db: Session, emp_cd: str, products: list[schemas.TransactionProductIn]):
    # 1-1: 取引テーブルに仮登録
    txn = models.Transaction(
        DATETIME=datetime.now(),
        EMP_CD=emp_cd or "9999999999",
        STORE_CD="30",     # ← 固定
        POS_NO="90",       # ← 固定
        TOTAL_AMT=0,
        TTL_AMT_EX_TAX=0
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # 1-2 & 1-3: 明細登録 + 合計金額計算
    total = 0
    for idx, item in enumerate(products):
        detail = models.TransactionDetail(
            TRD_ID=txn.TRD_ID,
            DTL_ID=idx + 1,
            PRD_ID=item.PRD_ID,
            PRD_CODE=item.CODE,
            PRD_NAME=item.NAME,
            PRD_PRICE=item.PRICE,
            TAX_CD="01"  # 仮
        )
        db.add(detail)
        total += item.PRICE

    # 1-4: 合計金額更新
    txn.TOTAL_AMT = total
    txn.TTL_AMT_EX_TAX = total  # 税抜金額が別にあるなら調整
    db.commit()

    # 1-5: 合計金額返却
    return {"success": True, "total": total}


