#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QSize

from ui.styles import PLAYER_COLOR, BANKER_COLOR, EMPTY_CELL_BG, CELL_BORDER, TEXT_COLOR

class MatrixCell(QWidget):
    """5x5 Matrisin tek bir hücresini temsil eden widget"""
    
    clicked = pyqtSignal(int, int)  # Tıklama olayı için sinyal: (satır, sütun)
    
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.value = None  # None: boş, 'P': Player, 'B': Banker
        self.setMinimumSize(50, 50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setToolTip(f"Hücre ({row}, {col})")
    
    def setValue(self, value):
        """Hücre değerini ayarla ('P', 'B' veya None)"""
        self.value = value
        self.update()  # Yeniden çizim için
    
    def getValue(self):
        """Hücre değerini döndür"""
        return self.value
    
    def paintEvent(self, event):
        """Hücreyi çiz"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan
        rect = QRect(1, 1, self.width() - 2, self.height() - 2)
        
        if self.value == 'P':
            bg_color = QColor(PLAYER_COLOR)
            text = "P"
        elif self.value == 'B':
            bg_color = QColor(BANKER_COLOR)
            text = "B"
        else:
            bg_color = QColor(EMPTY_CELL_BG)
            text = ""
        
        # Hücre arka planını çiz
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRect(rect)
        
        # Hücre kenarlığını çiz
        painter.setPen(QPen(QColor(CELL_BORDER), 1))
        painter.drawRect(rect)
        
        # Metin çiz
        if text:
            painter.setPen(QColor(TEXT_COLOR))
            painter.drawText(rect, Qt.AlignCenter, text)
    
    def mousePressEvent(self, event):
        """Fare tıklama olayı"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.row, self.col)
        super().mousePressEvent(event)
    
    def sizeHint(self):
        """Tercih edilen boyut"""
        return QSize(60, 60)


class MatrixWidget(QWidget):
    """5x5 Baccarat tahmin matrisini temsil eden widget"""
    
    cellClicked = pyqtSignal(int, int)  # Hücreye tıklama olayı
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        """Kullanıcı arayüzünü oluştur"""
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(2)
        
        # 5x5 matris oluştur
        self.cells = []
        for row in range(5):
            row_cells = []
            for col in range(5):
                cell = MatrixCell(row, col)
                cell.clicked.connect(self.onCellClicked)
                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        self.setLayout(grid_layout)
    
    def onCellClicked(self, row, col):
        """Hücre tıklama olayı"""
        self.cellClicked.emit(row, col)
    
    def setCellValue(self, row, col, value):
        """Belirtilen hücrenin değerini ayarla"""
        if 0 <= row < 5 and 0 <= col < 5:
            self.cells[row][col].setValue(value)
    
    def getCellValue(self, row, col):
        """Belirtilen hücrenin değerini döndür"""
        if 0 <= row < 5 and 0 <= col < 5:
            return self.cells[row][col].getValue()
        return None
    
    def clearMatrix(self):
        """Tüm matrisi temizle"""
        for row in range(5):
            for col in range(5):
                self.cells[row][col].setValue(None)
    
    def getMatrixState(self):
        """Matrisin mevcut durumunu 2D dizi olarak döndür"""
        state = []
        for row in range(5):
            row_values = []
            for col in range(5):
                row_values.append(self.cells[row][col].getValue())
            state.append(row_values)
        return state
    
    def setMatrixState(self, state):
        """Matrisi verilen durum ile güncelle"""
        if not state or len(state) != 5:
            return
            
        for row in range(5):
            if len(state[row]) != 5:
                continue
            for col in range(5):
                self.cells[row][col].setValue(state[row][col])