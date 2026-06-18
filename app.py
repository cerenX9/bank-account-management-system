import streamlit as st
import requests

# Sayfa Tasarımı Ayarları
st.set_page_config(page_title="Ceren Bank", page_icon="🏦", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏦 CEREN BANK MÜŞTERİ PANELİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Güvenli, Hızlı ve Modern Bankacılık Deneyimi</p>", unsafe_allow_html=True)
st.divider()

# Arka plandaki FastAPI sunucumuzun adresi
API_URL = "http://127.0.0.1:8000"

# Yan yana iki büyük sütun oluşturalım
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🛠️ Hesap İşlemleri")
    
    # 1. HESAP AÇMA BÖLÜMÜ
    with st.expander("✨ Yeni Hesap Aç", expanded=True):
        acc_num = st.text_input("Hesap Numarası (Örn: 1111)", key="reg_acc")
        owner = st.text_input("Müşteri Adı Soyadı", key="reg_name")
        initial_balance = st.number_input("İlk Yatırılacak Tutar (TL)", min_value=0.0, step=100.0)
        
        if st.button("Hesabı Oluştur", use_container_width=True):
            if acc_num and owner:
                payload = {"account_number": acc_num, "owner_name": owner, "initial_balance": initial_balance}
                response = requests.post(f"{API_URL}/accounts/", json=payload)
                if response.status_code == 201:
                    st.success(f"🎉 Tebrikler {owner}! Hesabınız başarıyla açıldı.")
                else:
                    st.error(f"❌ Hata: {response.json().get('detail')}")
            else:
                st.warning("Lütfen tüm alanları doldurun.")

    # 2. PARA YATIRMA BÖLÜMÜ
    with st.expander("💰 Hesaba Para Yatır"):
        dep_acc = st.text_input("Para Yatırılacak Hesap No", key="dep_acc")
        dep_amount = st.number_input("Yatırılacak Miktar (TL)", min_value=0.0, step=50.0, key="dep_amount")
        
        if st.button("Parayı Yatır", use_container_width=True):
            if dep_acc and dep_amount > 0:
                payload = {"amount": dep_amount}
                response = requests.post(f"{API_URL}/accounts/{dep_acc}/deposit", json=payload)
                if response.status_code == 200:
                    st.success(f"✅ {dep_amount} TL başarıyla yatırıldı! Yeni Bakiye: {response.json().get('new_balance')} TL")
                else:
                    st.error("❌ Hesap bulunamadı veya bir hata oluştu.")

with col2:
    st.markdown("### 📊 Sorgulama ve Transfer")
    
    # 3. BAKİYE SORGULAMA BÖLÜMÜ
    with st.expander("🔍 Hesap Özetini Görüntüle", expanded=True):
        search_acc = st.text_input("Sorgulanacak Hesap No", key="search_acc")
        if st.button("Sorgula", use_container_width=True):
            if search_acc:
                response = requests.get(f"{API_URL}/accounts/{search_acc}")
                if response.status_code == 200:
                    data = response.json()
                    st.metric(label=f"👤 {data['owner_name']} - Bakiye", value=f"{data['balance']} TL")
                    st.info(f"Hesap Numarası: {data['account_number']}")
                else:
                    st.error("❌ Böyle bir hesap bulunamadı!")

    # 4. HAVALE / TRANSFER BÖLÜMÜ
    with st.expander("💸 Hesaba Havale Gönder"):
        sender = st.text_input("Gönderen Hesap No", key="send_acc")
        receiver = st.text_input("Alıcı Hesap No", key="rec_acc")
        transfer_amount = st.number_input("Transfer Tutarı (TL)", min_value=0.0, step=50.0, key="trans_amount")
        
        if st.button("Havale Yap", use_container_width=True):
            if sender and receiver and transfer_amount > 0:
                payload = {"sender_account": sender, "receiver_account": receiver, "amount": transfer_amount}
                response = requests.post(f"{API_URL}/transfer/", json=payload)
                if response.status_code == 200:
                    st.success("🚀 Havale işlemi başarıyla tamamlandı!")
                    st.write(f"Kalan Bakiyeniz: {response.json().get('sender_new_balance')} TL")
                else:
                    st.error(f"❌ İşlem Reddedildi: {response.json().get('detail')}")