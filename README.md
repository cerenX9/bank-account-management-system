# 🏦 Ceren Bank: Katmanlı Mimarili Full-Stack Banka Yönetim Sistemi

Bu proje; veri güvenliği, ilişkisel veritabanı yönetimi ve iş mantığı (business logic) kurallarını barındıran modern bir **Backend API** sistemi ile son kullanıcının etkileşime girebildiği şık bir **Frontend (Ön Yüz)** web arayüzünün birleşiminden oluşan **Full-Stack** bir yazılım mühendisliği çalışmasıdır.

--------------------------------------------------------------------------------------------------------
# 🚀🚀🚀🚀LİNK İLE UYGULAMAYA GİRİŞ YAP 🚀🚀🚀🚀

https://bank-account-management-system-7yhbz2ddbkgy9ze8rdkfv8.streamlit.app/

--------------------------------------------------------------------------------------------------------

## 🏗️ Sistem Mimarisi ve Çalışma Mantığı

Proje, kurumsal şirketlerin kullandığı **Mikroservis / Ayrık Mimari** prensiplerine uygun olarak iki bağımsız katmanın birbiriyle HTTP protokolü üzerinden (REST API) konuşması esasına dayanır:

1. **Arka Plan Katmanı (Backend - FastAPI):** İşin mutfağıdır. Veritabanı bağlantılarını, SQL tablolarını yönetir ve hesaplar arası havale/bakiye kontrolleri gibi kritik algoritmaları işletir. (`Port: 8000`)
2. **Ön Yüz Katmanı (Frontend - Streamlit):** Müşterinin gördüğü vitrindir. Kullanıcıdan aldığı verileri güvenli bir şekilde arka plana iletir ve gelen yanıtları temiz, kurumsal bir tasarımla ekrana basar. (`Port: 8501`)

---

## 🛠️ Kullanılan Teknolojiler

* **Core Language:** Python 3
* **API Framework:** FastAPI (Asenkron, yüksek performanslı web servis mimarisi)
* **Web UI Frontend:** Streamlit (Veri odaklı ve modern kullanıcı arayüzü)
* **ORM (Veritabanı Köprüsü):** SQLAlchemy (Python nesnelerini güvenli SQL sorgularına dönüştürmek için)
* **Veritabanı:** SQLite (İlişkisel, gömülü veritabanı sistemi)
* **Veri Doğrulama:** Pydantic (HTTP isteklerindeki veri tiplerini ve güvenliğini doğrulamak için)

---

## 💡 Kazanılan Yazılım Mühendisliği Yetkinlikleri

* **Full-Stack Entegrasyonu:** İki farklı yerel sunucuyu (FastAPI ve Streamlit) `requests` kütüphanesi kullanarak birbirine entegre etme ve veri senkronizasyonu sağlama yetkinliği.
* **Temiz Kod ve Katmanlı Tasarım (Clean Code):** Veritabanı ayarlarının (`database.py`), SQL modellerinin (`models.py`), API rotalarının (`main.py`) ve arayüz kodlarının (`app.py`) birbirinden tamamen izole edilerek sürdürülebilir mimari kurulması.
* **Kritik İş Mantığı (Business Logic) & Hata Yönetimi:** Para transferlerinde yetersiz bakiye engellemesi, benzersiz hesap numarası kontrolleri ve bunlara uygun HTTP durum kodlarının (201 Created, 400 Bad Request, 404 Not Found) sektörel standartlarda yönetilmesi.

---

## 🚀 Projeyi Bilgisayarınızda Çalıştırın

Bu projeyi yerelde çalıştırmak için iki ayrı katmanı (sunucuyu) aynı anda ayağa kaldırmamız gerekir.

### Adım 1: Bağımlılıkları Yükleyin
Öncelikle projenin kök dizininde bir terminal açarak gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt


### Adım 2: Müşteri Panelini (Frontend) Başlatın
VS Code üzerinden **yeni bir terminal sekmesi (+)** açın (ilk terminali kapatmayın) ve şu komutu yazarak web sitesini ayağa kaldırın:
```bash
python -m streamlit run app.py
