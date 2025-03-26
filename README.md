# Baccarat Tahmin Uygulaması

Modern ve kullanıcı dostu bir arayüze sahip, gelişmiş tahmin algoritmalarıyla desteklenen bir baccarat tahmin uygulaması.

## Özellikler

- 5x5 tahmin matrisi görselleştirmesi
- Çoklu tahmin modelleri:
  - Pattern AI: Desen tanıma tabanlı tahmin algoritması
  - Deep Baccarat: İstatistiksel analiz tabanlı tahmin algoritması
- Gerçek zamanlı tahmin ve güven düzeyi gösterimi
- Oyun istatistikleri takibi
- Tahmin geçmişi
- Matrisi kaydetme ve yükleme özellikleri

## Kurulum

### Gereksinimler

- Python 3.6 veya üzeri
- PyQt5

```bash
# Gerekli kütüphaneleri yükleyin
pip install PyQt5
```

### Çalıştırma

```bash
# Ana dizinde çalıştırın
python main.py
```

## Proje Yapısı

```
baccarat_predictor/
├── main.py                  # Ana uygulama başlangıç noktası
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # Ana pencere UI sınıfı
│   ├── matrix_widget.py     # 5x5 matris widget'ı
│   ├── stats_widget.py      # İstatistikler widget'ı
│   └── styles.py            # Renkler ve stiller
├── core/
│   ├── __init__.py
│   ├── game.py              # Oyun mantığı ve veri yapıları
│   └── history.py           # Geçmiş kayıtları yönetimi
└── models/
    ├── __init__.py
    ├── base_model.py        # Temel model sınıfı
    ├── deep_baccarat.py     # Deep Baccarat modeli
    └── pattern_ai.py        # Pattern AI modeli
```

## Kullanım

1. Uygulama başlatıldığında, 5x5 matris ve tahmin panelleri görüntülenir.
2. Matris hücrelerine tıklayarak geçmiş oyun sonuçlarını girebilirsiniz:
   - Boş hücreye tıklama: Player (P) olarak işaretler
   - P işaretli hücreye tıklama: Banker (B) olarak değiştirir
   - B işaretli hücreye tıklama: Hücreyi temizler
3. Player veya Banker butonlarına tıklayarak tahmin yapabilirsiniz
4. Geri Al butonu ile son değişikliği geri alabilirsiniz
5. Temizle butonu ile tüm matrisi sıfırlayabilirsiniz
6. Kaydet butonu ile mevcut matrisi JSON formatında kaydedebilirsiniz

## Tahmin Modelleri

### Pattern AI

Desen tanıma algoritması, matristeki desenleri analiz ederek ve geçmiş sonuçlardaki kalıpları inceleyerek tahmin yapar:

- Matris desenleri analizi (satır, sütun, köşegen ve blok desenler)
- Dizi analizi (ardışık Player veya Banker sonuçları)
- Alterasyon analizi (P-B değişim sıklığı)

### Deep Baccarat

İstatistiksel analiz tabanlı bir model olup, Baccarat'ın gerçek olasılıklarını ve davranış örüntülerini göz önüne alır:

- Gerçek Baccarat olasılıklarına dayalı yanlılık düzeltmesi
- Ortalamaya dönüş (regression to the mean) ilkesi
- Uzun dizilerin kırılma eğilimi analizi
- Oransal dengesizlik düzeltmesi

## Model Geliştirme

Yeni tahmin modelleri eklemek için:

1. `models/base_model.py` içindeki `BaseModel` sınıfından türetilen yeni bir sınıf oluşturun
2. `predict()` metodunu uygulayın
3. Modeli ana uygulamaya entegre edin

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## İletişim

Sorularınız veya önerileriniz için lütfen iletişime geçin.