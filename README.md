# 2. El Araç / Otomobil Ekspertiz ve Değerleme Sistemi

PySide6 (Qt for Python) kullanılarak geliştirilmiş masaüstü araç ekspertiz ve piyasa değerleme uygulaması.

## Karşılanan İsterler (B01 – B07)

- **B01 — Sanal ortam, PySide6 kurulumu, `QApplication` ve olay döngüsü:** `.venv` sanal ortamı, `requirements.txt`, `QApplication(sys.argv)` ve `sys.exit(app.exec())`.
- **B02 — `QMainWindow` sınıf yapısı:** `OtoEkspertizPenceresi(QMainWindow)`, `super().__init__()`, `self.initUI()` ve `self` kullanımı.
- **B03 — Sinyal ve slot bağlantıları:** `.clicked.connect()`, `.valueChanged.connect()`, `.currentIndexChanged.connect()`, `.toggled.connect()`, `.triggered.connect()` ile olay güdümlü anlık puan ve fiyat hesaplama.
- **B04 — Yerleşimler (Layouts):** `QHBoxLayout`, `QVBoxLayout`, iç içe yerleşimler, `QFormLayout` ve `addStretch()`.
- **B05 — `.ui` dosyası, `QUiLoader` ve `findChild`:** `ekspertiz_raporu.ui` dosyasının `QUiLoader` ile dinamik yüklenmesi ve `findChild()` ile bileşenlere (`QLabel`, `QProgressBar`, `QTextEdit`, `QPushButton`) erişim.
- **B06 — Form elemanları, veri okuma ve doğrulama:** Plaka formatı (Regex), boş alan, mükerrer plaka, boya/değişen parça sayısı (maksimum 13 parça) ve fiyat/km mantık doğrulaması.
- **B07 — Menü çubuğu, araç çubuğu, durum çubuğu, `QMessageBox` ve `QFileDialog`:** JSON olarak kaydetme/açma (`QFileDialog`), onay ve uyarı pencereleri (`QMessageBox`), `QMenuBar`, `QToolBar` ve `QStatusBar`.

## Kurulum ve Çalıştırma

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
