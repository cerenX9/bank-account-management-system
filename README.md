# 🏦 RESTful Banka Hesap Yönetimi API'si

Bu proje, Yazılım Mühendisliği standartlarına uygun olarak katmanlı mimari (Layered Architecture) prensipleriyle geliştirilmiş; veri bütünlüğü, ilişkisel veritabanı yönetimi ve güvenli iş mantığı (business logic) barındıran modern bir backend API sistemidir.

---

## 🛠️ Kullanılan Teknolojiler ve Standartlar

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Yüksek performanslı, asenkron ve otomatik Swagger dökümantasyonlu API geliştirme)
* **ORM (Veritabanı Köprüsü):** [SQLAlchemy](https://www.sqlalchemy.org/) (Python nesnelerini SQL tablolarına dönüştürmek için)
* **Veritabanı:** SQLite (Hafif ve gömülü ilişkisel veritabanı sistemi)
* **Veri Doğrulama:** Pydantic (Gelen HTTP isteklerinin veri tiplerini ve güvenliğini doğrulamak için)

---

## 💡 Kazanılan Yazılım Mühendisliği Yetkinlikleri

1. **Katmanlı Mimari Tasarımı:** Veritabanı modelleri (`models.py`), veritabanı konfigürasyonu (`database.py`) ve API yönlendirmeleri (`main.py`) birbirinden izole edilerek temiz kod (Clean Code) standartları uygulandı.
2. **İş Mantığı ve Hata Yönetimi:** Para transferlerinde yetersiz bakiye kontrolleri, benzersiz hesap numarası doğrulamaları ve HTTP durum kodları (201 Created, 400 Bad Request, 404 Not Found) sektörel standartlarda yönetildi.
3. **Otomatik API Dökümantasyonu:** FastAPI'nin entegre OpenAPI yapısı sayesinde interaktif test arayüzü kuruldu.

---

## 🚀 Projeyi Yerel Bilgisayarınızda Çalıştırın

### 1. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt