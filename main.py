from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# Veritabanı tablolarını otomatik oluşturuyoruz
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="🔒 Güvenli Bankacılık REST API Sistemi")

# --- Veri Doğrulama Şablonları (Pydantic Schemas) ---
class AccountCreate(BaseModel):
    account_number: str
    owner_name: str
    initial_balance: float = 0.0

class TransactionRequest(BaseModel):
    amount: float

class TransferRequest(BaseModel):
    sender_account: str
    receiver_account: str
    amount: float

# --- API Rotaları (Endpoints) ---

@app.post("/accounts/", status_code=status.HTTP_201_CREATED)
def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    # Hesap numarası eşsiz olmalı kontrolü
    db_account = db.query(models.Account).filter(models.Account.account_number == account_data.account_number).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Bu hesap numarası zaten kullanımda!")
    
    new_account = models.Account(
        account_number=account_data.account_number,
        owner_name=account_data.owner_name,
        balance=account_data.initial_balance
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"message": "Hesap başarıyla açıldı", "account": new_account}

@app.get("/accounts/{account_number}")
def get_account_balance(account_number: str, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Hesap bulunamadı!")
    return account

@app.post("/accounts/{account_number}/deposit")
def deposit_money(account_number: str, data: TransactionRequest, db: Session = Depends(get_db)):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Yatırılacak miktar 0'dan büyük olmalıdır.")
    
    account = db.query(models.Account).filter(models.Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Hesap bulunamadı!")
    
    account.balance += data.amount
    db.commit()
    return {"message": f"{data.amount} TL başarıyla yatırıldı.", "new_balance": account.balance}

@app.post("/transfer/")
def transfer_money(req: TransferRequest, db: Session = Depends(get_db)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer miktarı 0'dan büyük olmalıdır.")
    
    # Gönderen ve Alıcı hesapları veritabanından bul
    sender = db.query(models.Account).filter(models.Account.account_number == req.sender_account).first()
    receiver = db.query(models.Account).filter(models.Account.account_number == req.receiver_account).first()
    
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Gönderici veya Alıcı hesap bulunamadı!")
    
    # Bakiye kontrolü (Business Logic)
    if sender.balance < req.amount:
        raise HTTPException(status_code=400, detail="Yetersiz bakiye! Transfer gerçekleştirilemedi.")
    
    # Parayı düş ve diğerine ekle (Atomik İşlem simülasyonu)
    sender.balance -= req.amount
    receiver.balance += req.amount
    
    db.commit()
    return {
        "message": "Havale işlemi başarıyla tamamlandı.",
        "transferred_amount": req.amount,
        "sender_new_balance": sender.balance
    }