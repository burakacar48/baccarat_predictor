#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QGroupBox, QSplitter, QFrame,
                            QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.matrix_widget import MatrixWidget
from ui.stats_widget import StatsWidget
from ui.styles import (APP_STYLE, PLAYER_BTN_STYLE, BANKER_BTN_STYLE, 
                      ACTION_BTN_STYLE, BACKGROUND_DARK)

import os
import json

class MainWindow(QMainWindow):
    """Baccarat tahmin uygulaması ana pencere sınıfı"""
    
    def __init__(self):
        super().__init__()
        self.history = []  # Matris durumu geçmişi
        self.current_step = -1  # Geçerli adım
        self.player_count = 0
        self.banker_count = 0
        self.tie_count = 0
        
        self._initUI()  # Metod ismi düzeltildi
        self.setWindowTitle("Baccarat Tahmin Uygulaması")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(APP_STYLE)
    
    def _initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Sol Panel (Matris ve Butonlar)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Matris Grubu
        matrix_group = QGroupBox("Tahmin Matrisi")
        matrix_layout = QVBoxLayout(matrix_group)
        
        # Matris Widget'ı
        self.matrix_widget = MatrixWidget()
        self.matrix_widget.cellClicked.connect(self.onMatrixCellClicked)
        matrix_layout.addWidget(self.matrix_widget)
        
        left_layout.addWidget(matrix_group, 5)  # 5 birim genişliğinde
        
        # Buton Paneli
        button_panel = QWidget()
        button_layout = QVBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # İşlem Butonları
        action_layout = QHBoxLayout()
        
        self.undo_btn = QPushButton("GERİ AL")
        self.undo_btn.setStyleSheet(ACTION_BTN_STYLE)
        self.undo_btn.clicked.connect(self.onUndoClicked)
        self.undo_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("TEMİZLE")
        self.clear_btn.setStyleSheet(ACTION_BTN_STYLE)
        self.clear_btn.clicked.connect(self.onClearClicked)
        
        self.save_btn = QPushButton("KAYDET")
        self.save_btn.setStyleSheet(ACTION_BTN_STYLE)
        self.save_btn.clicked.connect(self.onSaveClicked)
        
        action_layout.addWidget(self.undo_btn)
        action_layout.addWidget(self.clear_btn)
        action_layout.addWidget(self.save_btn)
        
        button_layout.addLayout(action_layout)
        
        # Tahmin Butonları
        prediction_layout = QHBoxLayout()
        
        self.player_btn = QPushButton("PLAYER")
        self.player_btn.setStyleSheet(PLAYER_BTN_STYLE)
        self.player_btn.setFixedHeight(50)
        self.player_btn.clicked.connect(lambda: self.onPredictionButtonClicked('P'))
        
        self.banker_btn = QPushButton("BANKER")
        self.banker_btn.setStyleSheet(BANKER_BTN_STYLE)
        self.banker_btn.setFixedHeight(50)
        self.banker_btn.clicked.connect(lambda: self.onPredictionButtonClicked('B'))
        
        prediction_layout.addWidget(self.player_btn)
        prediction_layout.addWidget(self.banker_btn)
        
        button_layout.addLayout(prediction_layout)
        
        left_layout.addWidget(button_panel, 1)  # 1 birim genişliğinde
        
        # Sağ Panel (İstatistikler)
        self.stats_widget = StatsWidget()
        
        # Ana düzene panelleri ekle
        main_layout.addWidget(left_panel, 1)  # 1 birim genişliğinde
        main_layout.addWidget(self.stats_widget, 1)  # 1 birim genişliğinde
        
        self.setCentralWidget(main_widget)
        
        # Başlangıç istatistikleri
        self.stats_widget.updateGameStats(self.player_count, self.banker_count, self.tie_count)
    
    def onMatrixCellClicked(self, row, col):
        """Matris hücresine tıklandığında"""
        current_value = self.matrix_widget.getCellValue(row, col)
        
        # Değeri döngüsel olarak değiştir: None -> P -> B -> None
        if current_value is None:
            new_value = 'P'
            self.player_count += 1
        elif current_value == 'P':
            new_value = 'B'
            self.player_count -= 1
            self.banker_count += 1
        else:  # 'B'
            new_value = None
            self.banker_count -= 1
        
        # Hücreyi güncelle
        self.matrix_widget.setCellValue(row, col, new_value)
        
        # İstatistikleri güncelle
        self.stats_widget.updateGameStats(self.player_count, self.banker_count, self.tie_count)
        
        # Geçmişe durumu kaydet
        self.saveStateToHistory()
    
    def onPredictionButtonClicked(self, prediction):
        """Prediction butonlarından birine tıklandığında"""
        # Tahmini belirle
        self.stats_widget.setPrediction(prediction, 85)  # Güven değeri şimdilik sabit
        
        # Geçmişe ekle
        self.stats_widget.addToHistory(prediction)
        
        # Gerçek uygulamada, burada model tahmini ve güncellemesi yapılır
        QMessageBox.information(self, "Tahmin", 
            f"{'PLAYER' if prediction == 'P' else 'BANKER'} tahmini yapıldı!")
    
    def onUndoClicked(self):
        """Geri al butonuna tıklandığında"""
        if self.current_step > 0:
            self.current_step -= 1
            state = self.history[self.current_step]
            
            # Oyun sayılarını sıfırla ve yeni duruma göre hesapla
            self.player_count = 0
            self.banker_count = 0
            
            # Matrisi önceki duruma getir
            self.matrix_widget.setMatrixState(state)
            
            # P ve B sayılarını tekrar say
            for row in range(5):
                for col in range(5):
                    value = self.matrix_widget.getCellValue(row, col)
                    if value == 'P':
                        self.player_count += 1
                    elif value == 'B':
                        self.banker_count += 1
            
            # İstatistikleri güncelle
            self.stats_widget.updateGameStats(self.player_count, self.banker_count, self.tie_count)
            
            # Buton durumunu güncelle
            self.undo_btn.setEnabled(self.current_step > 0)
    
    def onClearClicked(self):
        """Temizle butonuna tıklandığında"""
        reply = QMessageBox.question(self, 'Temizle',
            "Matrisi temizlemek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Matrisi temizle
            self.matrix_widget.clearMatrix()
            
            # Sayaçları sıfırla
            self.player_count = 0
            self.banker_count = 0
            
            # İstatistikleri güncelle
            self.stats_widget.updateGameStats(self.player_count, self.banker_count, self.tie_count)
            
            # Geçmişi temizle
            self.history = []
            self.current_step = -1
            self.saveStateToHistory()  # Boş durumu kaydet
            
            # Buton durumunu güncelle
            self.undo_btn.setEnabled(False)
    
    def onSaveClicked(self):
        """Kaydet butonuna tıklandığında"""
        filename, _ = QFileDialog.getSaveFileName(self, "Matrisi Kaydet", 
                                                  os.path.expanduser("~/Desktop/baccarat_matrix.json"),
                                                  "JSON Dosyaları (*.json)")
        
        if filename:
            try:
                # Mevcut durumu al
                state = self.matrix_widget.getMatrixState()
                
                # JSON dosyasına kaydet
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(state, f)
                
                QMessageBox.information(self, "Kaydedildi", 
                    f"Matris başarıyla kaydedildi:\n{filename}")
            except Exception as e:
                QMessageBox.warning(self, "Hata", 
                    f"Kaydetme sırasında bir hata oluştu:\n{str(e)}")
    
    def saveStateToHistory(self):
        """Mevcut matrisi geçmişe kaydet"""
        current_state = self.matrix_widget.getMatrixState()
        
        # Eğer geri alınmış bir durumdan sonra değişiklik yapıldıysa
        # o noktadan sonraki geçmişi sil
        if self.current_step < len(self.history) - 1:
            self.history = self.history[:self.current_step + 1]
        
        # Yeni durumu ekle
        self.history.append(current_state)
        self.current_step = len(self.history) - 1
        
        # Geri al butonunu etkinleştir
        self.undo_btn.setEnabled(self.current_step > 0)