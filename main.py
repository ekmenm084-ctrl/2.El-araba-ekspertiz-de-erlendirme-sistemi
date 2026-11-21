import json
import os
import re
import sys
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class OtoEkspertizPenceresi(QMainWindow):
    """
    B02 — QMainWindow'dan miras alan sınıf yapısı, super().__init__(), initUI() ve self kullanımı.
    """

    def __init__(self):
        super().__init__()
        # Ekspertiz kayıtlarını tutacağımız liste
        self.arac_listesi = []
        self.rapor_penceresi = None
        self.initUI()
        self.menuVeAracCubuguOlustur()
        self.sinyalSlotBagla()

    def initUI(self):
        self.setWindowTitle("2. El Araç Ekspertiz ve Değerleme Sistemi")
        self.resize(1180, 740)

        # Ana merkezi widget ve ana yatay yerleşim (B04 — QHBoxLayout)
        merkez_widget = QWidget()
        self.setCentralWidget(merkez_widget)
        ana_yatay_layout = QHBoxLayout(merkez_widget)

        # =====================================================================
        # SOL PANEL: Araç Bilgileri ve Ekspertiz Formu (B04 — QVBoxLayout + QFormLayout)
        # =====================================================================
        sol_dikey_layout = QVBoxLayout()

        form_grup = QGroupBox("Araç Kimlik ve Ekspertiz Formu")
        form_layout = QFormLayout()

        # B06 — Form Elemanları
        # 1. Plaka (QLineEdit)
        self.txt_plaka = QLineEdit()
        self.txt_plaka.setPlaceholderText("Örn: 34 ABC 123")
        form_layout.addRow("Araç Plakası (*):", self.txt_plaka)

        # 2. Marka / Model (QLineEdit)
        self.txt_marka_model = QLineEdit()
        self.txt_marka_model.setPlaceholderText("Örn: Volkswagen Golf 1.5 TSI")
        form_layout.addRow("Marka ve Model (*):", self.txt_marka_model)

        # 3. Model Yılı (QSpinBox)
        self.spn_yil = QSpinBox()
        self.spn_yil.setRange(1990, 2026)
        self.spn_yil.setValue(2021)
        form_layout.addRow("Model Yılı:", self.spn_yil)

        # 4. Kilometre (QSpinBox)
        self.spn_km = QSpinBox()
        self.spn_km.setRange(0, 1_000_000)
        self.spn_km.setSingleStep(5000)
        self.spn_km.setValue(65000)
        self.spn_km.setSuffix(" km")
        form_layout.addRow("Kilometre:", self.spn_km)

        # 5. Yakıt Tipi (QComboBox)
        self.cmb_yakit = QComboBox()
        self.cmb_yakit.addItems(["Benzin", "Dizel", "Hibrit", "Elektrik", "LPG & Benzin"])
        form_layout.addRow("Yakıt Tipi:", self.cmb_yakit)

        # 6. Vites Tipi (QRadioButton + QHBoxLayout iç içe yerleşim)
        vites_layout = QHBoxLayout()
        self.rad_otomatik = QRadioButton("Otomatik")
        self.rad_manuel = QRadioButton("Manuel")
        self.rad_otomatik.setChecked(True)
        vites_layout.addWidget(self.rad_otomatik)
        vites_layout.addWidget(self.rad_manuel)
        vites_layout.addStretch()  # B04 — addStretch() kullanımı
        form_layout.addRow("Şanzıman / Vites:", vites_layout)

        # 7. Boyalı ve Değişen Parça Sayısı (QHBoxLayout içinde 2 QSpinBox)
        parca_layout = QHBoxLayout()
        self.spn_boyali = QSpinBox()
        self.spn_boyali.setRange(0, 13)
        self.spn_boyali.setSuffix(" parça")
        self.spn_degisen = QSpinBox()
        self.spn_degisen.setRange(0, 13)
        self.spn_degisen.setSuffix(" parça")
        parca_layout.addWidget(QLabel("Boyalı:"))
        parca_layout.addWidget(self.spn_boyali)
        parca_layout.addWidget(QLabel("Değişen:"))
        parca_layout.addWidget(self.spn_degisen)
        form_layout.addRow("Kaporta Durumu:", parca_layout)

        # 8. Ekspertiz Ek Durumlar (QCheckBox'lar)
        durum_layout = QVBoxLayout()
        self.chk_agir_hasar = QCheckBox("Ağır Hasar / Pert Kayıtlı (Tramer)")
        self.chk_motor_iyi = QCheckBox("Motor & Mekanik Performansı İyi (%85+)")
        self.chk_motor_iyi.setChecked(True)
        self.chk_garanti = QCheckBox("Yetkili Servis Bakımlı / Garantili")
        durum_layout.addWidget(self.chk_agir_hasar)
        durum_layout.addWidget(self.chk_motor_iyi)
        durum_layout.addWidget(self.chk_garanti)
        form_layout.addRow("Ekspertiz Kontrolleri:", durum_layout)

        # 9. Hatasız Emsal Baz Piyasa Fiyatı (QDoubleSpinBox)
        self.dspn_baz_fiyat = QDoubleSpinBox()
        self.dspn_baz_fiyat.setRange(0.0, 50_000_000.0)
        self.dspn_baz_fiyat.setSingleStep(25_000.0)
        self.dspn_baz_fiyat.setDecimals(2)
        self.dspn_baz_fiyat.setValue(1_250_000.0)
        self.dspn_baz_fiyat.setSuffix(" TL")
        form_layout.addRow("Emsal Baz Fiyat (*):", self.dspn_baz_fiyat)

        # 10. Ekspertiz Uzman Notu (QTextEdit)
        self.txt_not = QTextEdit()
        self.txt_not.setPlaceholderText("Motor, şasi, direksiyon kutusu veya lastik durumu hakkında notlar...")
        self.txt_not.setMaximumHeight(75)
        form_layout.addRow("Uzman Notu:", self.txt_not)

        # Anlık Ön Hesaplama Etiketi
        self.lbl_on_izleme = QLabel("Ekspertiz Puanı: 100/100 | Tahmini Değer: 1.250.000,00 TL")
        self.lbl_on_izleme.setStyleSheet(
            "font-weight: bold; color: #1b5e20; background-color: #e8f5e9; padding: 8px; border-radius: 4px;"
        )
        form_layout.addRow("Anlık Değerleme:", self.lbl_on_izleme)

        form_grup.setLayout(form_layout)
        sol_dikey_layout.addWidget(form_grup)

        # İşlem Butonları (QHBoxLayout + addStretch)
        buton_layout = QHBoxLayout()
        self.btn_ekle = QPushButton("Aracı Kaydet ve Değerle")
        self.btn_ekle.setStyleSheet("font-weight: bold; padding: 6px 12px;")
        self.btn_temizle = QPushButton("Formu Temizle")
        self.btn_rapor_ui = QPushButton("Ekspertiz Sertifikası (.ui)")
        self.btn_sil = QPushButton("Seçili Kaydı Sil")

        buton_layout.addWidget(self.btn_ekle)
        buton_layout.addWidget(self.btn_temizle)
        buton_layout.addWidget(self.btn_rapor_ui)
        buton_layout.addStretch()  # B04 — addStretch() ile Sil butonunu sağa yasla
        buton_layout.addWidget(self.btn_sil)

        sol_dikey_layout.addLayout(buton_layout)
        sol_dikey_layout.addStretch()  # B04 — Formun altındaki boşluğu esnet

        # =====================================================================
        # SAĞ PANEL: Kayıtlı Araçlar Tablosu ve Özet Bilgi (B04 — QVBoxLayout)
        # =====================================================================
        sag_dikey_layout = QVBoxLayout()

        tablo_grup = QGroupBox("Ekspertizi Tamamlanan Araç Listesi")
        tablo_layout = QVBoxLayout()

        self.tbl_araclar = QTableWidget(0, 7)
        self.tbl_araclar.setHorizontalHeaderLabels([
            "Plaka",
            "Marka / Model",
            "Yıl & KM",
            "Yakıt / Vites",
            "Boya / Değişen",
            "Ekspertiz Puanı",
            "Tahmini Değer (TL)",
        ])
        self.tbl_araclar.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tbl_araclar.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tbl_araclar.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        tablo_layout.addWidget(self.tbl_araclar)

        # Tablo altı özet satırı (QHBoxLayout + addStretch)
        ozet_layout = QHBoxLayout()
        self.lbl_toplam_arac = QLabel("Toplam Kayıtlı Araç: 0")
        self.lbl_ortalama_puan = QLabel("Ortalama Ekspertiz Puanı: -")
        ozet_layout.addWidget(self.lbl_toplam_arac)
        ozet_layout.addStretch()
        ozet_layout.addWidget(self.lbl_ortalama_puan)

        tablo_layout.addLayout(ozet_layout)
        tablo_grup.setLayout(tablo_layout)
        sag_dikey_layout.addWidget(tablo_grup)

        # Ana yatay yerleşime Sol ve Sağ panelleri ekle (Oran: 2'ye 3)
        ana_yatay_layout.addLayout(sol_dikey_layout, 2)
        ana_yatay_layout.addLayout(sag_dikey_layout, 3)

        # B07 — Durum Çubuğu (QStatusBar)
        self.durum_cubugu = QStatusBar()
        self.setStatusBar(self.durum_cubugu)
        self.durum_cubugu.showMessage("Sistem hazır. Yeni araç ekspertiz bilgilerini girebilirsiniz.")

        # İlk anlık hesaplamayı çalıştır
        self.anlikDegerlemeGuncelle()

    def menuVeAracCubuguOlustur(self):
        """
        B07 — Menü çubuğu (QMenuBar), Araç çubuğu (QToolBar) ve QAction tanımlamaları.
        """
        menu_cubugu = self.menuBar()

        # 1. Dosya Menüsü
        dosya_menu = menu_cubugu.addMenu("&Dosya")

        self.act_ac = QAction("Kayıtları Dosyadan Aç (.json)...", self)
        self.act_ac.setShortcut("Ctrl+O")
        self.act_ac.setStatusTip("Daha önce kaydedilmiş ekspertiz kayıtlarını JSON dosyasından yükler.")

        self.act_kaydet = QAction("Kayıtları Dosyaya Kaydet (.json)...", self)
        self.act_kaydet.setShortcut("Ctrl+S")
        self.act_kaydet.setStatusTip("Mevcut araç ekspertiz listesini JSON dosyası olarak kaydeder.")

        self.act_ornek_yukle = QAction("Örnek Araç Verisi Yükle", self)
        self.act_ornek_yukle.setStatusTip("Test amacıyla tabloya 3 adet örnek ekspertiz kaydı ekler.")

        self.act_cikis = QAction("Çıkış", self)
        self.act_cikis.setShortcut("Ctrl+Q")
        self.act_cikis.setStatusTip("Uygulamadan güvenli çıkış yapar.")

        dosya_menu.addAction(self.act_ac)
        dosya_menu.addAction(self.act_kaydet)
        dosya_menu.addSeparator()
        dosya_menu.addAction(self.act_ornek_yukle)
        dosya_menu.addSeparator()
        dosya_menu.addAction(self.act_cikis)

        # 2. Ekspertiz Menüsü
        ekspertiz_menu = menu_cubugu.addMenu("&Ekspertiz İşlemleri")

        self.act_ekle = QAction("Aracı Kaydet ve Değerle", self)
        self.act_ekle.setShortcut("Ctrl+Return")

        self.act_rapor_ui = QAction("Detaylı Ekspertiz Sertifikası Aç (.ui)", self)
        self.act_rapor_ui.setShortcut("Ctrl+R")
        self.act_rapor_ui.setStatusTip("QUiLoader ve findChild kullanarak ekspertiz_raporu.ui penceresini açar.")

        self.act_tumunu_temizle = QAction("Tüm Listeyi Sıfırla", self)
        self.act_tumunu_temizle.setStatusTip("Tablodaki tüm araç kayıtlarını onay alarak temizler.")

        ekspertiz_menu.addAction(self.act_ekle)
        ekspertiz_menu.addAction(self.act_rapor_ui)
        ekspertiz_menu.addSeparator()
        ekspertiz_menu.addAction(self.act_tumunu_temizle)

        # 3. Yardım Menüsü
        yardim_menu = menu_cubugu.addMenu("&Yardım")
        self.act_hakkinda = QAction("Hakkında", self)
        self.act_hakkinda.setShortcut("F1")
        yardim_menu.addAction(self.act_hakkinda)

        # B07 — Araç Çubuğu (QToolBar)
        arac_cubugu = QToolBar("Ana Araç Çubuğu")
        arac_cubugu.setMovable(False)
        self.addToolBar(arac_cubugu)

        arac_cubugu.addAction(self.act_ac)
        arac_cubugu.addAction(self.act_kaydet)
        arac_cubugu.addSeparator()
        arac_cubugu.addAction(self.act_ornek_yukle)
        arac_cubugu.addAction(self.act_rapor_ui)
        arac_cubugu.addSeparator()
        arac_cubugu.addAction(self.act_tumunu_temizle)
        arac_cubugu.addAction(self.act_hakkinda)

    def sinyalSlotBagla(self):
        """
        B03 — Sinyal ve slot bağlantıları, olay güdümlü akış.
        """
        # Buton tıklama sinyalleri
        self.btn_ekle.clicked.connect(self.aracKaydet)
        self.btn_temizle.clicked.connect(self.formuTemizle)
        self.btn_sil.clicked.connect(self.seciliAraciSil)
        self.btn_rapor_ui.clicked.connect(self.ekspertizRaporuAcUI)

        # Menü ve Araç Çubuğu QAction sinyalleri (B03 & B07)
        self.act_ac.triggered.connect(self.dosyadanAc)
        self.act_kaydet.triggered.connect(self.dosyayaKaydet)
        self.act_ornek_yukle.triggered.connect(self.ornekVeriYukle)
        self.act_cikis.triggered.connect(self.uygulamadanCik)
        self.act_ekle.triggered.connect(self.aracKaydet)
        self.act_rapor_ui.triggered.connect(self.ekspertizRaporuAcUI)
        self.act_tumunu_temizle.triggered.connect(self.tumListeyiSifirla)
        self.act_hakkinda.triggered.connect(self.hakkindaGoster)

        # Form elemanları değiştikçe anlık ekspertiz puanını ve tahmini fiyatı güncelleyen sinyaller
        self.spn_yil.valueChanged.connect(self.anlikDegerlemeGuncelle)
        self.spn_km.valueChanged.connect(self.anlikDegerlemeGuncelle)
        self.spn_boyali.valueChanged.connect(self.anlikDegerlemeGuncelle)
        self.spn_degisen.valueChanged.connect(self.anlikDegerlemeGuncelle)
        self.dspn_baz_fiyat.valueChanged.connect(self.anlikDegerlemeGuncelle)
        self.cmb_yakit.currentIndexChanged.connect(self.anlikDegerlemeGuncelle)
        self.rad_otomatik.toggled.connect(self.anlikDegerlemeGuncelle)
        self.chk_agir_hasar.toggled.connect(self.anlikDegerlemeGuncelle)
        self.chk_motor_iyi.toggled.connect(self.anlikDegerlemeGuncelle)
        self.chk_garanti.toggled.connect(self.anlikDegerlemeGuncelle)

        # Tablodan bir satıra tıklandığında formu doldur
        self.tbl_araclar.itemSelectionChanged.connect(self.tablodanSecimYapildi)

    def ekspertizHesapla(self):
        """
        Formdaki değerlere göre 100 üzerinden Ekspertiz Puanı ve Tahmini Piyasa Değeri hesaplar.
        """
        puan = 100
        baz_fiyat = self.dspn_baz_fiyat.value()
        carpan = 1.0

        boyali = self.spn_boyali.value()
        degisen = self.spn_degisen.value()
        km = self.spn_km.value()

        # Her boyalı parça -2 puan ve %1.5 değer kaybı
        puan -= boyali * 2
        carpan -= boyali * 0.015

        # Her değişen parça -5 puan ve %3.5 değer kaybı
        puan -= degisen * 5
        carpan -= degisen * 0.035

        # Ağır hasar / pert kaydı varsa -25 puan ve %25 değer kaybı
        if self.chk_agir_hasar.isChecked():
            puan -= 25
            carpan -= 0.25

        # Motor performansı iyi değilse -15 puan ve %10 değer kaybı
        if not self.chk_motor_iyi.isChecked():
            puan -= 15
            carpan -= 0.10

        # Yetkili servis garantili ise +5 puan ve %4 değer artışı
        if self.chk_garanti.isChecked():
            puan += 5
            carpan += 0.04

        # Otomatik vites +2% değer avantajı
        if self.rad_otomatik.isChecked():
            carpan += 0.02

        # Yüksek KM etkisi (200.000 km üstü)
        if km > 200_000:
            puan -= 10
            carpan -= 0.08
        elif km > 100_000:
            puan -= 4
            carpan -= 0.03

        puan = max(10, min(100, puan))
        carpan = max(0.30, carpan)
        tahmini_deger = baz_fiyat * carpan

        return puan, tahmini_deger

    def anlikDegerlemeGuncelle(self):
        """
        B03 — Olay güdümlü akış: Kullanıcı değerleri değiştirdikçe anlık önizleme etiketini günceller.
        """
        puan, tahmini_deger = self.ekspertizHesapla()
        fiyat_str = f"{tahmini_deger:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.lbl_on_izleme.setText(f"Ekspertiz Puanı: {puan}/100 | Tahmini Değer: {fiyat_str} TL")

    def veriDogrula(self):
        """
        B06 — Form elemanlarından veri okuma ve doğrulama (Validation).
        Hata varsa (False, hata_mesaji), geçerliyse (True, "") döndürür.
        """
        plaka = self.txt_plaka.text().strip().upper()
        marka_model = self.txt_marka_model.text().strip()
        boyali = self.spn_boyali.value()
        degisen = self.spn_degisen.value()
        baz_fiyat = self.dspn_baz_fiyat.value()
        yil = self.spn_yil.value()
        km = self.spn_km.value()

        # 1. Boş alan kontrolü
        if not plaka:
            return False, "Lütfen araç plakasını giriniz!"
        if not marka_model or len(marka_model) < 3:
            return False, "Lütfen geçerli bir Marka ve Model giriniz (en az 3 karakter)!"

        # 2. Türkiye Plaka Formatı Doğrulaması (Örn: 01..81 + 1-3 Harf + 2-4 Rakam)
        plaka_deseni = r"^(0[1-9]|[1-7][0-9]|8[01])\s?[A-ZÇĞİÖŞÜ]{1,3}\s?\d{2,4}$"
        if not re.match(plaka_deseni, plaka):
            return (
                False,
                "Plaka formatı geçersiz!\nÖrnek geçerli formatlar: '34 ABC 123' veya '06TR1234' (İl kodu 01-81 arası olmalıdır).",
            )

        # 3. Aynı plakalı araç mükerrer kayıt kontrolü
        for arac in self.arac_listesi:
            if arac["plaka"] == plaka:
                return False, f"'{plaka}' plakalı araç zaten listede kayıtlı!"

        # 4. Kaporta toplam parça sayısı mantık kontrolü (Bir araçta maksimum 13 ana kaporta parçası bulunur)
        if boyali + degisen > 13:
            return (
                False,
                f"Boyalı ({boyali}) ve Değişen ({degisen}) parça toplamı 13'ten fazla olamaz!",
            )

        # 5. Baz fiyat kontrolü
        if baz_fiyat < 50_000:
            return False, "Emsal baz piyasa fiyatı en az 50.000 TL olmalıdır!"

        # 6. Yıl ve KM mantık kontrolü
        if yil == 2026 and km > 150_000:
            return False, "2026 model bir aracın kilometresi 150.000 km'den büyük olamaz!"

        return True, ""

    def aracKaydet(self):
        """
        B06 — Form verilerini doğrular, okur ve tabloya ekler.
        """
        gecerli, hata_mesaji = self.veriDogrula()
        if not gecerli:
            QMessageBox.warning(self, "Doğrulama Hatası", hata_mesaji)
            self.durum_cubugu.showMessage(f"Doğrulama hatası: {hata_mesaji}", 5000)
            return

        puan, tahmini_deger = self.ekspertizHesapla()
        vites = "Otomatik" if self.rad_otomatik.isChecked() else "Manuel"

        yeni_arac = {
            "plaka": self.txt_plaka.text().strip().upper(),
            "marka_model": self.txt_marka_model.text().strip(),
            "yil": self.spn_yil.value(),
            "km": self.spn_km.value(),
            "yakit": self.cmb_yakit.currentText(),
            "vites": vites,
            "boyali": self.spn_boyali.value(),
            "degisen": self.spn_degisen.value(),
            "agir_hasar": self.chk_agir_hasar.isChecked(),
            "motor_iyi": self.chk_motor_iyi.isChecked(),
            "garanti": self.chk_garanti.isChecked(),
            "baz_fiyat": self.dspn_baz_fiyat.value(),
            "not": self.txt_not.toPlainText().strip(),
            "puan": puan,
            "tahmini_deger": tahmini_deger,
        }

        self.arac_listesi.append(yeni_arac)
        self.tabloyuGuncelle()
        self.formuTemizle()
        self.durum_cubugu.showMessage(
            f"'{yeni_arac['plaka']}' plakalı araç ekspertiz listesine eklendi. (Toplam: {len(self.arac_listesi)})",
            5000,
        )

    def tabloyuGuncelle(self):
        """
        self.arac_listesi içindeki kayıtları QTableWidget'a yansıtır ve özet istatistikleri hesaplar.
        """
        self.tbl_araclar.setRowCount(0)
        toplam_puan = 0

        for satir, arac in enumerate(self.arac_listesi):
            self.tbl_araclar.insertRow(satir)

            fiyat_str = f"{arac['tahmini_deger']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            hucreler = [
                arac["plaka"],
                arac["marka_model"],
                f"{arac['yil']} / {arac['km']:,} km".replace(",", "."),
                f"{arac['yakit']} / {arac['vites']}",
                f"{arac['boyali']} Boya / {arac['degisen']} Değişen",
                f"{arac['puan']} / 100",
                f"{fiyat_str} TL",
            ]

            for sutun, metin in enumerate(hucreler):
                item = QTableWidgetItem(metin)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tbl_araclar.setItem(satir, sutun, item)

            toplam_puan += arac["puan"]

        adet = len(self.arac_listesi)
        self.lbl_toplam_arac.setText(f"Toplam Kayıtlı Araç: {adet}")
        if adet > 0:
            ort = toplam_puan / adet
            self.lbl_ortalama_puan.setText(f"Ortalama Ekspertiz Puanı: {ort:.1f} / 100")
        else:
            self.lbl_ortalama_puan.setText("Ortalama Ekspertiz Puanı: -")

    def formuTemizle(self):
        """
        Form elemanlarını varsayılan değerlerine sıfırlar.
        """
        self.txt_plaka.clear()
        self.txt_marka_model.clear()
        self.spn_yil.setValue(2021)
        self.spn_km.setValue(65000)
        self.cmb_yakit.setCurrentIndex(0)
        self.rad_otomatik.setChecked(True)
        self.spn_boyali.setValue(0)
        self.spn_degisen.setValue(0)
        self.chk_agir_hasar.setChecked(False)
        self.chk_motor_iyi.setChecked(True)
        self.chk_garanti.setChecked(False)
        self.dspn_baz_fiyat.setValue(1_250_000.0)
        self.txt_not.clear()
        self.tbl_araclar.clearSelection()
        self.txt_plaka.setFocus()
        self.anlikDegerlemeGuncelle()
        self.durum_cubugu.showMessage("Form temizlendi.", 3000)

    def seciliAraciSil(self):
        """
        B07 — QMessageBox onay kutusu ile tablodan seçili olan aracı listeden siler.
        """
        secili_satir = self.tbl_araclar.currentRow()
        if secili_satir < 0:
            QMessageBox.information(self, "Bilgi", "Lütfen silmek istediğiniz aracı tablodan seçiniz.")
            return

        arac = self.arac_listesi[secili_satir]
        cevap = QMessageBox.question(
            self,
            "Silme Onayı",
            f"'{arac['plaka']}' ({arac['marka_model']}) kaydını silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if cevap == QMessageBox.StandardButton.Yes:
            del self.arac_listesi[secili_satir]
            self.tabloyuGuncelle()
            self.formuTemizle()
            self.durum_cubugu.showMessage(f"'{arac['plaka']}' plakalı araç kaydı silindi.", 4000)

    def tumListeyiSifirla(self):
        """
        B07 — QMessageBox ile tüm kayıtları sıfırlar.
        """
        if not self.arac_listesi:
            QMessageBox.information(self, "Bilgi", "Listede silinecek araç kaydı bulunmuyor.")
            return

        cevap = QMessageBox.question(
            self,
            "Tüm Listeyi Sıfırla",
            f"Tablodaki toplam {len(self.arac_listesi)} araç kaydının tamamı silinecek. Onaylıyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if cevap == QMessageBox.StandardButton.Yes:
            self.arac_listesi.clear()
            self.tabloyuGuncelle()
            self.formuTemizle()
            self.durum_cubugu.showMessage("Tüm ekspertiz listesi sıfırlandı.", 4000)

    def tablodanSecimYapildi(self):
        """
        B03 — Tablodan bir satır seçildiğinde bilgileri formda gösterir.
        """
        secili_satir = self.tbl_araclar.currentRow()
        if secili_satir < 0 or secili_satir >= len(self.arac_listesi):
            return

        arac = self.arac_listesi[secili_satir]
        self.txt_plaka.setText(arac["plaka"])
        self.txt_marka_model.setText(arac["marka_model"])
        self.spn_yil.setValue(arac["yil"])
        self.spn_km.setValue(arac["km"])
        self.cmb_yakit.setCurrentText(arac["yakit"])
        if arac["vites"] == "Otomatik":
            self.rad_otomatik.setChecked(True)
        else:
            self.rad_manuel.setChecked(True)
        self.spn_boyali.setValue(arac["boyali"])
        self.spn_degisen.setValue(arac["degisen"])
        self.chk_agir_hasar.setChecked(arac["agir_hasar"])
        self.chk_motor_iyi.setChecked(arac["motor_iyi"])
        self.chk_garanti.setChecked(arac["garanti"])
        self.dspn_baz_fiyat.setValue(arac["baz_fiyat"])
        self.txt_not.setPlainText(arac["not"])
        self.durum_cubugu.showMessage(f"Seçili araç: {arac['plaka']} - {arac['marka_model']}", 4000)

    # =========================================================================
    # B05 — .ui dosyası, QUiLoader ile yükleme ve findChild ile bileşene erişim
    # =========================================================================
    def ekspertizRaporuAcUI(self):
        """
        B05 — ekspertiz_raporu.ui dosyasını QUiLoader ile yükler ve findChild ile
        içindeki widget'lara erişerek seçili aracın (veya formdaki aracın) ekspertiz sertifikasını gösterir.
        """
        ui_dosya_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ekspertiz_raporu.ui")
        ui_dosyasi = QFile(ui_dosya_yolu)

        if not ui_dosyasi.open(QIODevice.OpenModeFlag.ReadOnly):
            QMessageBox.critical(self, "Hata", f".ui dosyası açılamadı:\n{ui_dosya_yolu}")
            return

        loader = QUiLoader()
        self.rapor_penceresi = loader.load(ui_dosyasi, self)
        ui_dosyasi.close()

        if self.rapor_penceresi is None:
            QMessageBox.critical(self, "Hata", "QUiLoader .ui dosyasını yükleyemedi!")
            return

        # B05 — findChild ile .ui içindeki bileşenlere (widget) erişim
        lbl_arac_kimlik = self.rapor_penceresi.findChild(QLabel, "lbl_arac_kimlik")
        lbl_teknik_detay = self.rapor_penceresi.findChild(QLabel, "lbl_teknik_detay")
        lbl_kaporta_ozet = self.rapor_penceresi.findChild(QLabel, "lbl_kaporta_ozet")
        prg_ekspertiz_skor = self.rapor_penceresi.findChild(QProgressBar, "prg_ekspertiz_skor")
        lbl_tahmini_fiyat = self.rapor_penceresi.findChild(QLabel, "lbl_tahmini_fiyat")
        txt_rapor_detay = self.rapor_penceresi.findChild(QTextEdit, "txt_rapor_detay")
        btn_rapor_kapat = self.rapor_penceresi.findChild(QPushButton, "btn_rapor_kapat")

        # Seçili satır varsa onu, yoksa formdaki anlık veriyi kullan
        secili_satir = self.tbl_araclar.currentRow()
        if 0 <= secili_satir < len(self.arac_listesi):
            arac = self.arac_listesi[secili_satir]
        else:
            puan, tahmini_deger = self.ekspertizHesapla()
            arac = {
                "plaka": self.txt_plaka.text().strip().upper() or "PLAKA GİRİLMEDİ (ÖNİZLEME)",
                "marka_model": self.txt_marka_model.text().strip() or "Marka/Model Belirtilmedi",
                "yil": self.spn_yil.value(),
                "km": self.spn_km.value(),
                "yakit": self.cmb_yakit.currentText(),
                "vites": "Otomatik" if self.rad_otomatik.isChecked() else "Manuel",
                "boyali": self.spn_boyali.value(),
                "degisen": self.spn_degisen.value(),
                "agir_hasar": self.chk_agir_hasar.isChecked(),
                "motor_iyi": self.chk_motor_iyi.isChecked(),
                "garanti": self.chk_garanti.isChecked(),
                "baz_fiyat": self.dspn_baz_fiyat.value(),
                "not": self.txt_not.toPlainText().strip() or "Ek uzman notu girilmedi.",
                "puan": puan,
                "tahmini_deger": tahmini_deger,
            }

        fiyat_str = f"{arac['tahmini_deger']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        baz_str = f"{arac['baz_fiyat']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # findChild ile bulunan bileşenlerin içeriklerini doldur
        if lbl_arac_kimlik:
            lbl_arac_kimlik.setText(f"{arac['plaka']} — {arac['marka_model']}")
        if lbl_teknik_detay:
            lbl_teknik_detay.setText(f"{arac['yil']} Model | {arac['km']:,} km | {arac['yakit']} | {arac['vites']}".replace(",", "."))
        if lbl_kaporta_ozet:
            tramer = "Ağır Hasar/Pert Kayıtlı" if arac["agir_hasar"] else "Ağır Hasar Kaydı Yok"
            lbl_kaporta_ozet.setText(f"{arac['boyali']} Boyalı, {arac['degisen']} Değişen Parça ({tramer})")
        if prg_ekspertiz_skor:
            prg_ekspertiz_skor.setValue(arac["puan"])
        if lbl_tahmini_fiyat:
            lbl_tahmini_fiyat.setText(f"{fiyat_str} TL (Emsal Baz: {baz_str} TL)")

        if txt_rapor_detay:
            motor_durum = "İyi (%85 ve üzeri)" if arac["motor_iyi"] else "Bakım Gerektiriyor (%85 altı)"
            garanti_durum = "Yetkili Servis Bakımlı / Garantili" if arac["garanti"] else "Garanti Kapsamı Dışında"
            rapor_metni = (
                f"=== DETAYLI EKSPERTİZ DEĞERLENDİRME RAPORU ===\n"
                f"• Araç Plakası ve Modeli : {arac['plaka']} - {arac['marka_model']}\n"
                f"• Motor & Mekanik Durumu : {motor_durum}\n"
                f"• Servis / Garanti Durumu: {garanti_durum}\n"
                f"• Uzman Ekspertiz Notu   : {arac['not'] or 'Belirtilmedi'}\n\n"
                f"=== FİLO GENEL İSTATİSTİKLERİ ===\n"
                f"• Sistemdeki Toplam Araç : {len(self.arac_listesi)} adet\n"
            )
            if self.arac_listesi:
                toplam_deger = sum(a["tahmini_deger"] for a in self.arac_listesi)
                ort_puan = sum(a["puan"] for a in self.arac_listesi) / len(self.arac_listesi)
                toplam_str = f"{toplam_deger:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                rapor_metni += (
                    f"• Filo Ortalama Puanı    : {ort_puan:.1f} / 100\n"
                    f"• Filo Toplam Piyasa Değ.: {toplam_str} TL\n"
                )
            txt_rapor_detay.setPlainText(rapor_metni)

        if btn_rapor_kapat:
            btn_rapor_kapat.clicked.connect(self.rapor_penceresi.close)

        self.durum_cubugu.showMessage("ekspertiz_raporu.ui QUiLoader ile yüklendi ve findChild ile dolduruldu.", 5000)
        self.rapor_penceresi.show()

    # =========================================================================
    # B07 — QFileDialog ve QMessageBox ile Dosya Açma / Kaydetme / Yardım
    # =========================================================================
    def dosyayaKaydet(self):
        """
        B07 — QFileDialog kullanarak araç ekspertiz listesini JSON dosyasına kaydeder.
        """
        if not self.arac_listesi:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek araç verisi bulunmuyor! Önce araç ekleyiniz.")
            return

        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self,
            "Ekspertiz Kayıtlarını Kaydet",
            "ekspertiz_kayitlari.json",
            "JSON Dosyaları (*.json);;Tüm Dosyalar (*)",
        )

        if not dosya_yolu:
            return

        try:
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                json.dump(self.arac_listesi, f, ensure_ascii=False, indent=4)
            QMessageBox.information(
                self,
                "Kayıt Başarılı",
                f"Toplam {len(self.arac_listesi)} araç kaydı başarıyla kaydedildi:\n{dosya_yolu}",
            )
            self.durum_cubugu.showMessage(f"Veriler kaydedildi: {dosya_yolu}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Kayıt Hatası", f"Dosya kaydedilirken hata oluştu:\n{e}")

    def dosyadanAc(self):
        """
        B07 — QFileDialog kullanarak JSON dosyasından araç ekspertiz kayıtlarını yükler.
        """
        dosya_yolu, _ = QFileDialog.getOpenFileName(
            self,
            "Ekspertiz Kayıtlarını Aç",
            "",
            "JSON Dosyaları (*.json);;Tüm Dosyalar (*)",
        )

        if not dosya_yolu:
            return

        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                yuklenen_liste = json.load(f)

            if not isinstance(yuklenen_liste, list):
                raise ValueError("JSON dosyası geçerli bir araç listesi içermiyor!")

            self.arac_listesi = yuklenen_liste
            self.tabloyuGuncelle()
            QMessageBox.information(
                self,
                "Yükleme Başarılı",
                f"{len(self.arac_listesi)} adet araç ekspertiz kaydı başarıyla yüklendi.",
            )
            self.durum_cubugu.showMessage(f"Dosyadan {len(self.arac_listesi)} araç yüklendi: {dosya_yolu}", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Okuma Hatası", f"Dosya okunurken hata oluştu:\n{e}")

    def ornekVeriYukle(self):
        """
        Hızlı test için 3 örnek aracı listeye ekler.
        """
        ornekler = [
            {
                "plaka": "34 ABC 123",
                "marka_model": "Volkswagen Golf 1.5 eTSI R-Line",
                "yil": 2023,
                "km": 24000,
                "yakit": "Hibrit",
                "vites": "Otomatik",
                "boyali": 0,
                "degisen": 0,
                "agir_hasar": False,
                "motor_iyi": True,
                "garanti": True,
                "baz_fiyat": 1_850_000.0,
                "not": "Hatasız, boyasız, yetkili servis bakımlı.",
                "puan": 100,
                "tahmini_deger": 1_961_000.0,
            },
            {
                "plaka": "06 ANK 456",
                "marka_model": "Renault Megane 1.5 BlueDCi Icon",
                "yil": 2020,
                "km": 115000,
                "yakit": "Dizel",
                "vites": "Otomatik",
                "boyali": 2,
                "degisen": 1,
                "agir_hasar": False,
                "motor_iyi": True,
                "garanti": False,
                "baz_fiyat": 1_250_000.0,
                "not": "Sağ ön çamurluk değişen, iki kapı lokal boyalı.",
                "puan": 87,
                "tahmini_deger": 1_156_250.0,
            },
            {
                "plaka": "35 IZM 789",
                "marka_model": "Fiat Egea 1.4 Fire Easy",
                "yil": 2019,
                "km": 168000,
                "yakit": "LPG & Benzin",
                "vites": "Manuel",
                "boyali": 4,
                "degisen": 2,
                "agir_hasar": False,
                "motor_iyi": True,
                "garanti": False,
                "baz_fiyat": 780_000.0,
                "not": "Periyodik bakımları yeni yapıldı, lastikler %80.",
                "puan": 78,
                "tahmini_deger": 655_200.0,
            },
        ]

        eklenen = 0
        mevcut_plakalar = {a["plaka"] for a in self.arac_listesi}
        for o in ornekler:
            if o["plaka"] not in mevcut_plakalar:
                self.arac_listesi.append(o)
                eklenen += 1

        self.tabloyuGuncelle()
        self.durum_cubugu.showMessage(f"{eklenen} adet örnek araç ekspertiz kaydı yüklendi.", 5000)

    def hakkindaGoster(self):
        """
        B07 — QMessageBox ile uygulama hakkında bilgi verir.
        """
        QMessageBox.about(
            self,
            "Uygulama Hakkında",
            "<b>2. El Araç / Otomobil Ekspertiz ve Değerleme Sistemi</b><br><br>"
            "Bu proje PySide6 kullanılarak vize projesi isterlerine (B01 - B07) "
            "tam uyumlu olarak geliştirilmiştir:<br>"
            "• <b>B01:</b> Sanal ortam (.venv), PySide6, QApplication & Olay döngüsü<br>"
            "• <b>B02:</b> QMainWindow miras yapısı, super().__init__(), initUI(), self<br>"
            "• <b>B03:</b> Sinyal & Slot bağlantıları ve anlık olay güdümlü hesaplama<br>"
            "• <b>B04:</b> QHBoxLayout, QVBoxLayout, QFormLayout ve addStretch()<br>"
            "• <b>B05:</b> ekspertiz_raporu.ui, QUiLoader ve findChild() kullanımı<br>"
            "• <b>B06:</b> Form elemanları, veri okuma ve Regex/Mantık doğrulama<br>"
            "• <b>B07:</b> Menü çubuğu, Araç çubuğu, Durum çubuğu, QMessageBox & QFileDialog",
        )

    def uygulamadanCik(self):
        """
        B07 — QMessageBox ile çıkış onayı alır.
        """
        cevap = QMessageBox.question(
            self,
            "Çıkış Onayı",
            "Uygulamadan çıkmak istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if cevap == QMessageBox.StandardButton.Yes:
            self.close()


if __name__ == "__main__":
    # B01 — QApplication nesnesi ve olay döngüsü (Event Loop)
    app = QApplication(sys.argv)
    pencere = OtoEkspertizPenceresi()
    pencere.show()
    sys.exit(app.exec())
