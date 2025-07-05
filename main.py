from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os

# ローカル import（Azureで `.database` は失敗しやすいため、flat import推奨）
import models
import schemas
import crud
from database import SessionLocal, engine

app = FastAPI()

# CORS設定（本番では限定的に）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では ["https://your-frontend-url"] に絞る
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# テーブル作成（migrationsがない場合の初回起動用）
models.Base.metadata.create_all(bind=engine)

# DBセッション取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 商品取得API
@app.get("/product", response_model=schemas.ProductOut)
def get_product(code: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product

# 購入登録API
@app.post("/purchase")
def purchase(data: schemas.TransactionIn, db: Session = Depends(get_db)):
    try:
        print("=== purchase endpoint reached ===")
        print("datetime now:", datetime.now())

        total = 0
        transaction = models.Transaction(
            DATETIME=datetime.now(),
            EMP_CD=data.emp_cd or "9999999999",
            STORE_CD="30",
            POS_NO="90",
            TOTAL_AMT=0,
            TTL_AMT_EX_TAX=0
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        for idx, item in enumerate(data.products):
            detail = models.TransactionDetail(
                TRD_ID=transaction.TRD_ID,
                DTL_ID=idx + 1,
                PRD_ID=item.PRD_ID,
                PRD_CODE=item.CODE,
                PRD_NAME=item.NAME,
                PRD_PRICE=item.PRICE,
                TAX_CD="01"
            )
            db.add(detail)
            total += item.PRICE

        transaction.TOTAL_AMT = total
        transaction.TTL_AMT_EX_TAX = total
        db.commit()

        return {"success": True, "total_amount": total}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"購入処理に失敗しました: {str(e)}")
