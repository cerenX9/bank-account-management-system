import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- VERİTABANI AYARLARI (Doğrudan Streamlit İçinde) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQL MODELİ ---
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    owner_name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

# Tabloları otomatik oluştur
Base.metadata.create_all(bind=engine)

# --- ARAYÜZ TASARIMI ---
st.set_page_config(page_title="Zirve Bank", page_icon="🏦", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏦 ZIRVE BANK MÜŞTERİ PANELİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Güvenli, Hızlı ve Modern Bankacılık Deneyimi (Cloud Version)</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
db = SessionLocal()

with col1:
    st.markdown("### 🛠️ Hesap İşlemleri")
    
    # 1. HESAP AÇMA
    with st.expander("✨ Yeni Hesap Aç", expanded=True):
        acc_num = st.text_input("Hesap Numarası (Örn: 1111)", key="reg_acc")
        owner = st.text_input("Müşteri Adı Soyadı", key="reg_name")
        initial_balance = st.number_input("İlk Yatırılacak Tutar (TL)", min_value=0.0, step=100.0)
        
        if st.button("Hesabı Oluştur", use_container_width=True):
            if acc_num and owner:
                # Eşsiz hesap kontrolü
                db_account = db.query(Account).filter(Account.account_number == acc_num).first()
                if db_account:
                    st.error("❌ Hata: Bu hesap numarası zaten kullanımda!")
                else:
                    new_account = Account(account_number=acc_num, owner_name=owner, balance=initial_balance)
                    db.add(new_account)
                    db.commit()
                    st.success(f"🎉 Tebrikler {owner}! Hesabınız başarıyla açıldı.")
            else:
                st.warning("Lütfen tüm alanları doldurun.")

    # 2. PARA YATIRMA
    with st.expander("💰 Hesaba Para Yatır"):
        dep_acc = st.text_input("Para Yatırılacak Hesap No", key="dep_acc")
        dep_amount = st.number_input("Yatırılacak Miktar (TL)", min_value=0.0, step=50.0, key="dep_amount")
        
        if st.button("Parayı Yatır", use_container_width=True):
            if dep_acc and dep_amount > 0:
                account = db.query(Account).filter(Account.account_number == dep_acc).first()
                if account:
                    account.balance += dep_amount
                    db.commit()
                    st.success(f"✅ {dep_amount} TL başarıyla yatırıldı! Yeni Bakiye: {account.balance} TL")
                else:
                    st.error("❌ Hesap bulunamadı!")

with col2:
    st.markdown("### 📊 Sorgulama ve Transfer")
    
    # 3. BAKİYE SORGULAMA
    with st.expander("🔍 Hesap Özetini Görüntüle", expanded=True):
        search_acc = st.text_input("Sorgulanacak Hesap No", key="search_acc")
        if st.button("Sorgula", use_container_width=True):
            if search_acc:
                account = db.query(Account).filter(Account.account_number == search_acc).first()
                if account:
                    st.metric(label=f"👤 {account.owner_name} - Bakiye", value=f"{account.balance} TL")
                    st.info(f"Hesap Numarası: {account.account_number}")
                else:
                    st.error("❌ Böyle bir hesap bulunamadı!")

    # 4. HAVALE / TRANSFER
    with st.expander("💸 Hesaba Havale Gönder"):
        sender = st.text_input("Gönderen Hesap No", key="send_acc")
        receiver = st.text_input("Alıcı Hesap No", key="rec_acc")
        transfer_amount = st.number_input("Transfer Tutarı (TL)", min_value=0.0, step=50.0, key="trans_amount")
        
        if st.button("Havale Yap", use_container_width=True):
            if sender and receiver and transfer_amount > 0:
                s_acc = db.query(Account).filter(Account.account_number == sender).first()
                r_acc = db.query(Account).filter(Account.account_number == receiver).first()
                
                if not s_acc or not r_acc:
                    st.error("❌ Gönderici veya Alıcı hesap bulunamadı!")
                elif s_acc.balance < transfer_amount:
                    st.error("❌ İşlem Reddedildi: Yetersiz bakiye!")
                else:
                    s_acc.balance -= transfer_amount
                    r_acc.balance += transfer_amount
                    db.commit()
                    st.success("🚀 Havale işlemi başarıyla tamamlandı!")
                    st.write(f"Kalan Bakiyeniz: {s_acc.balance} TL")

db.close()