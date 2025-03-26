#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QGroupBox, QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.styles import (PLAYER_COLOR, BANKER_COLOR, TIE_COLOR, 
                      BACKGROUND_DARKER, TEXT_COLOR)

class PredictionWidget(QWidget):
    """Güncel tahmin bilgisini gösteren widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title_label = QLabel("GÜNCEL TAHMİN")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        
        # Tahmin değeri
        self.prediction_label = QLabel("?")
        self.prediction_label.setAlignment(Qt.AlignCenter)
        self.prediction_label.setStyleSheet(
            f"color: {TEXT_COLOR}; font-size: 28px; font-weight: bold;"
        )
        
        # Güven yüzdesi
        self.confidence_frame = QFrame()
        self.confidence_frame.setFixedSize(40, 40)
        self.confidence_frame.setStyleSheet(
            f"background-color: {BANKER_COLOR}; border-radius: 20px;"
        )
        
        confidence_layout = QVBoxLayout(self.confidence_frame)
        self.confidence_label = QLabel("?%")
        self.confidence_label.setAlignment(Qt.AlignCenter)
        self.confidence_label.setStyleSheet("color: white; font-weight: bold;")
        confidence_layout.addWidget(self.confidence_label)
        
        # Üst kısım düzeni (başlık ve güven)
        top_layout = QHBoxLayout()
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.confidence_frame)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.prediction_label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 8px;")
        self.setMinimumHeight(100)
    
    def setPrediction(self, prediction, confidence=None):
        """Tahmin ve güven değerini ayarla"""
        if prediction == 'P':
            self.prediction_label.setText("PLAYER")
            self.prediction_label.setStyleSheet(
                f"color: {PLAYER_COLOR}; font-size: 28px; font-weight: bold;"
            )
            self.confidence_frame.setStyleSheet(
                f"background-color: {PLAYER_COLOR}; border-radius: 20px;"
            )
        elif prediction == 'B':
            self.prediction_label.setText("BANKER")
            self.prediction_label.setStyleSheet(
                f"color: {BANKER_COLOR}; font-size: 28px; font-weight: bold;"
            )
            self.confidence_frame.setStyleSheet(
                f"background-color: {BANKER_COLOR}; border-radius: 20px;"
            )
        else:
            self.prediction_label.setText("?")
            self.prediction_label.setStyleSheet(
                f"color: {TEXT_COLOR}; font-size: 28px; font-weight: bold;"
            )
            self.confidence_frame.setStyleSheet(
                f"background-color: {TIE_COLOR}; border-radius: 20px;"
            )
        
        # Güven değeri
        if confidence is not None:
            self.confidence_label.setText(f"{confidence}%")
        else:
            self.confidence_label.setText("?%")


class ModelStatsWidget(QWidget):
    """Model istatistiklerini gösteren widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title_label = QLabel("MODEL İSTATİSTİKLERİ")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Tablo başlığı
        header_layout = QHBoxLayout()
        
        model_header = QLabel("MODEL ADI")
        model_header.setAlignment(Qt.AlignCenter)
        model_header.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        
        prediction_header = QLabel("TAHMİNİ")
        prediction_header.setAlignment(Qt.AlignCenter)
        prediction_header.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        
        success_header = QLabel("BAŞARI")
        success_header.setAlignment(Qt.AlignCenter)
        success_header.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        
        header_layout.addWidget(model_header)
        header_layout.addWidget(prediction_header)
        header_layout.addWidget(success_header)
        
        header_frame = QFrame()
        header_frame.setLayout(header_layout)
        header_frame.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 5px;")
        
        layout.addWidget(header_frame)
        
        # Model satırları - şimdilik örnek veriler
        self.models_layout = QVBoxLayout()
        self.addModelRow("DEEP BACCARAT", "B", 92.5)
        self.addModelRow("PATTERN AI", "P", 88.7)
        
        layout.addLayout(self.models_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 8px;")
        self.setMinimumHeight(160)
    
    def addModelRow(self, model_name, prediction, success_rate):
        """Model satırı ekle"""
        row_layout = QHBoxLayout()
        
        model_label = QLabel(model_name)
        model_label.setAlignment(Qt.AlignCenter)
        model_label.setStyleSheet(f"color: {TEXT_COLOR};")
        
        pred_color = PLAYER_COLOR if prediction == 'P' else BANKER_COLOR
        prediction_label = QLabel(prediction)
        prediction_label.setAlignment(Qt.AlignCenter)
        prediction_label.setStyleSheet(f"color: {pred_color}; font-weight: bold;")
        
        success_frame = QFrame()
        success_layout = QHBoxLayout(success_frame)
        success_label = QLabel(f"{success_rate}%")
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("color: white; font-weight: bold;")
        success_layout.addWidget(success_label)
        
        success_frame.setStyleSheet(
            f"background-color: {pred_color}; border-radius: 10px;"
        )
        
        row_layout.addWidget(model_label)
        row_layout.addWidget(prediction_label)
        row_layout.addWidget(success_frame)
        
        row_frame = QFrame()
        row_frame.setLayout(row_layout)
        row_frame.setStyleSheet(f"background-color: {BACKGROUND_DARKER};")
        
        self.models_layout.addWidget(row_frame)
    
    def updateModel(self, model_index, model_name, prediction, success_rate):
        """Varolan model bilgilerini güncelle"""
        # Gerçek uygulamada burada model satırlarını güncelleyebilirsiniz
        pass


class GameStatsWidget(QWidget):
    """Oyun istatistiklerini gösteren widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title_label = QLabel("OYUN İSTATİSTİKLERİ")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        layout.addWidget(title_label)
        
        # İstatistik kartları
        cards_layout = QHBoxLayout()
        
        # Player kartı
        self.player_card = self.createStatCard("PLAYER", "0", PLAYER_COLOR)
        cards_layout.addWidget(self.player_card)
        
        # Banker kartı
        self.banker_card = self.createStatCard("BANKER", "0", BANKER_COLOR)
        cards_layout.addWidget(self.banker_card)
        
        # Tie kartı
        self.tie_card = self.createStatCard("TIE", "0", TIE_COLOR)
        cards_layout.addWidget(self.tie_card)
        
        layout.addLayout(cards_layout)
        
        # Toplam el sayısı
        total_layout = QHBoxLayout()
        
        total_label = QLabel("TOPLAM EL:")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"color: {TEXT_COLOR};")
        
        self.total_count = QLabel("0")
        self.total_count.setAlignment(Qt.AlignCenter)
        self.total_count.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        
        total_layout.addStretch()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_count)
        total_layout.addStretch()
        
        layout.addLayout(total_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 8px;")
        self.setMinimumHeight(140)
    
    def createStatCard(self, title, count, color):
        """İstatistik kartı oluştur"""
        card = QFrame()
        card.setStyleSheet(
            f"background-color: {BACKGROUND_DARKER}; border: 1px solid {color}; border-radius: 5px;"
        )
        
        layout = QVBoxLayout(card)
        
        # Başlık çubuğu
        title_bar = QFrame()
        title_bar.setFixedHeight(5)
        title_bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        
        # Başlık
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; border: none;")
        
        # Sayı
        count_label = QLabel(count)
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold; border: none;")
        
        layout.addWidget(title_bar)
        layout.addWidget(title_label)
        layout.addWidget(count_label)
        
        return card
    
    def updateStats(self, player_count, banker_count, tie_count):
        """İstatistikleri güncelle"""
        # Player sayısını güncelle
        player_label = self.player_card.findChild(QLabel, "", Qt.FindChildrenRecursively)
        if player_label:
            player_label.setText(str(player_count))
        
        # Banker sayısını güncelle
        banker_label = self.banker_card.findChild(QLabel, "", Qt.FindChildrenRecursively)
        if banker_label:
            banker_label.setText(str(banker_count))
        
        # Tie sayısını güncelle
        tie_label = self.tie_card.findChild(QLabel, "", Qt.FindChildrenRecursively)
        if tie_label:
            tie_label.setText(str(tie_count))
        
        # Toplam el sayısını güncelle
        total = player_count + banker_count + tie_count
        self.total_count.setText(str(total))


class HistoryWidget(QWidget):
    """Son tahminleri gösteren widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []  # Tahmin geçmişi ['P', 'B', ...]
        self.initUI()
    
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title_label = QLabel("SON TAHMİNLER")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Tahmin geçmişi alanı
        self.history_frame = QFrame()
        self.history_frame.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 5px;")
        self.history_layout = QHBoxLayout(self.history_frame)
        self.history_layout.setSpacing(5)
        self.history_layout.setContentsMargins(10, 5, 10, 5)
        
        layout.addWidget(self.history_frame)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {BACKGROUND_DARKER}; border-radius: 8px;")
        self.setFixedHeight(80)
    
    def addPrediction(self, prediction):
        """Yeni tahmin ekle"""
        self.history.append(prediction)
        
        # Son 10 tahmini göster
        self.updateHistoryDisplay()
    
    def updateHistoryDisplay(self):
        """Tahmin geçmişi gösterimini güncelle"""
        # Tüm öğeleri temizle
        for i in reversed(range(self.history_layout.count())):
            widget = self.history_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Son 10 tahmini ekle (en son sağda olacak şekilde)
        for pred in self.history[-10:]:
            label = QLabel(pred)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(30, 30)
            
            if pred == 'P':
                label.setStyleSheet(
                    f"background-color: {PLAYER_COLOR}; color: white; border-radius: 15px; font-weight: bold;"
                )
            else:  # 'B'
                label.setStyleSheet(
                    f"background-color: {BANKER_COLOR}; color: white; border-radius: 15px; font-weight: bold;"
                )
            
            self.history_layout.addWidget(label)
        
        # Kalan boşluğu doldur
        if len(self.history) < 10:
            self.history_layout.addStretch()


class StatsWidget(QWidget):
    """Tüm istatistik widgetlerini içeren ana widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Tahmin widget'ı
        self.prediction_widget = PredictionWidget()
        layout.addWidget(self.prediction_widget)
        
        # Model istatistikleri
        self.model_stats = ModelStatsWidget()
        layout.addWidget(self.model_stats)
        
        # Oyun istatistikleri
        self.game_stats = GameStatsWidget()
        layout.addWidget(self.game_stats)
        
        # Tahmin geçmişi
        self.history_widget = HistoryWidget()
        layout.addWidget(self.history_widget)
        
        self.setLayout(layout)
    
    def setPrediction(self, prediction, confidence=None):
        """Güncel tahmini ayarla"""
        self.prediction_widget.setPrediction(prediction, confidence)
    
    def updateGameStats(self, player_count, banker_count, tie_count=0):
        """Oyun istatistiklerini güncelle"""
        self.game_stats.updateStats(player_count, banker_count, tie_count)
    
    def addToHistory(self, prediction):
        """Tahmin geçmişine ekle"""
        self.history_widget.addPrediction(prediction)