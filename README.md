# netflix-ml-project

#  Netflix Film Öneri Sistemi (FastAPI + KMeans)

Bu proje, kullanıcıların film tercihlerini analiz ederek onlara kişiselleştirilmiş öneriler sunan bir **makine öğrenmesi tabanlı API** sistemidir.  
Projede **FastAPI**, **SQLite**, **SQLAlchemy** ve **scikit-learn** kullanılmıştır.

---

##  Özellikler

- Kullanıcı, film ve tercih (rating) ekleme işlemleri  
- Kullanıcı-film tercih matrisi oluşturma  
- **K-Means** algoritması ile kullanıcı segmentasyonu  
- Aynı kümeye düşen kullanıcıların tercihlerine göre **film önerileri**  
- RESTful API yapısı (GET/POST endpointleri)  

---

##  Kurulum

```bash
# Gerekli paketleri yükle
pip install -r requirements.txt

Dosya Açıklamaları

main.py	- FastAPI uygulaması ve tüm API uç noktaları
models.py -	SQLAlchemy veri tabanı modelleri
seed.py - Örnek kullanıcı, film ve tercih verisi yükleyici
requirements.txt - Gerekli Python kütüphaneleri

Film önerileri, kullanıcıların değerlendirmelerine göre oluşturulan kullanıcı-film matrisinden, K-Means Kümeleme algoritması ile hesaplanır. Aynı kümeye düşen kullanıcıların beğendiği filmler öneri olarak sunulur.
