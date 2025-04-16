
# HecatePost 🔮

**HecatePost** adalah alat otomatis untuk menjadwalkan dan memposting gambar dan video ke Halaman Facebook menggunakan API resmi Graph API. Cocok untuk kreator, dropshipper, shitposter, hingga agensi sosial media.

---

## 🚀 Fitur Utama
- 🔁 Rotasi multi-page otomatis (`PAGE_ID_1`, `PAGE_ID_2`, dst.)
- 🖼️ Posting gambar otomatis + caption + hashtag
- 🎥 Posting video Facebook Reels otomatis
- 🔐 Setup APP ID & token hanya sekali
- 💾 Anti duplikat posting per halaman
- 🧠 Konfigurasi lewat file `.env`

---

## ⚙️ Cara Pakai

### 1. Clone repo ini
```bash
git clone https://github.com/Hecate1337-py/HecatePost.git
cd HecatePost
```

### 2. Install dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan
```bash
python hecate_post_manager.py
```

---

## 📁 Struktur Folder

```bash
images/           # Folder berisi gambar
vid/shorts/       # Folder berisi video
link.txt          # Caption setiap baris untuk gambar
.env              # Token dan konfigurasi halaman
```

---

## 🔐 Lisensi

Proyek ini menggunakan lisensi **MIT** — silakan gunakan, modifikasi, dan distribusikan dengan bebas. Lihat file [LICENSE](./LICENSE) untuk detailnya.

---

## 💡 Credits

Made with ❤️ by [@Hecate1337](https://github.com/Hecate1337-py)
