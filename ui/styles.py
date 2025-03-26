#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uygulama stil ve renk tanımları
"""

# Ana renkler
BACKGROUND_DARK = "#1A1A2E"
BACKGROUND_DARKER = "#16213E"
BACKGROUND_LIGHTER = "#0F3460"
TEXT_COLOR = "#E0E0E0"
ACCENT_COLOR = "#E94560"

# Oyuncu renkleri
PLAYER_COLOR = "#1565C0"  # Mavi
BANKER_COLOR = "#E94560"  # Kırmızı
TIE_COLOR = "#0F3460"     # Koyu mavi

# Matris hücre renkleri
PLAYER_CELL_BG = "#1565C0"
BANKER_CELL_BG = "#E94560"
EMPTY_CELL_BG = "#16213E"
CELL_BORDER = "#533483"

# Buton stilleri
BUTTON_STYLE = """
    QPushButton {
        background-color: %s;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 8px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: %s;
    }
    QPushButton:pressed {
        background-color: %s;
    }
"""

# Ana uygulama stili
APP_STYLE = """
    QMainWindow, QDialog {
        background-color: #1A1A2E;
    }
    QLabel {
        color: #E0E0E0;
    }
    QGroupBox {
        background-color: #16213E;
        border-radius: 5px;
        border: 1px solid #0F3460;
        margin-top: 10px;
        font-weight: bold;
        color: #E0E0E0;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
"""

# Buton stilleri
PLAYER_BTN_STYLE = BUTTON_STYLE % (PLAYER_COLOR, "#0D47A1", "#0A3D91")
BANKER_BTN_STYLE = BUTTON_STYLE % (BANKER_COLOR, "#D81B60", "#C2185B")
ACTION_BTN_STYLE = BUTTON_STYLE % (BACKGROUND_LIGHTER, "#0C2D4D", "#0A243D")