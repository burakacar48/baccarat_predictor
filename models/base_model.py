#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Baccarat tahmin modellerinin temel sınıfı
"""

from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Tüm tahmin modellerinin temel sınıfı"""
    
    def __init__(self, name="BaseModel"):
        """
        Inicializasyon
        
        Args:
            name (str): Model adı
        """
        self.name = name
        self.predictions = []  # Yapılan tahminler
        self.results = []      # Gerçek sonuçlar
        self.accuracy = 0.0    # Başarı oranı
    
    @abstractmethod
    def predict(self, matrix, history=None):
        """
        Tahmin yap (alt sınıflar tarafından uygulanmalı)
        
        Args:
            matrix (list): 5x5 matris (2D liste)
            history (list, optional): Oyun sonuçları geçmişi
            
        Returns:
            tuple: (tahmin, güven skoru)
        """
        pass
    
    def add_result(self, prediction, result):
        """
        Tahmin ve sonuç ekle
        
        Args:
            prediction (str): Yapılan tahmin ('P' veya 'B')
            result (str): Gerçek sonuç ('P', 'B' veya 'T')
        """
        self.predictions.append(prediction)
        self.results.append(result)
        self._update_accuracy()
    
    def _update_accuracy(self):
        """Başarı oranını güncelle"""
        if not self.predictions:
            self.accuracy = 0.0
            return
        
        # Tie sonuçları tahmin doğruluğunu etkilemez (tie olmayan sonuçlara bak)
        valid_predictions = [i for i, res in enumerate(self.results) if res != 'T']
        
        if not valid_predictions:
            self.accuracy = 0.0
            return
        
        correct = sum(1 for i in valid_predictions if self.predictions[i] == self.results[i])
        self.accuracy = (correct / len(valid_predictions)) * 100
    
    def get_stats(self):
        """
        Model istatistiklerini döndür
        
        Returns:
            dict: Model istatistikleri
        """
        total = len(self.predictions)
        tie_count = self.results.count('T')
        valid_predictions = total - tie_count
        
        return {
            'name': self.name,
            'total_predictions': total,
            'valid_predictions': valid_predictions,
            'accuracy': self.accuracy,
            'player_predictions': self.predictions.count('P'),
            'banker_predictions': self.predictions.count('B'),
            'last_prediction': self.predictions[-1] if self.predictions else None
        }
    
    def reset(self):
        """Model verilerini sıfırla"""
        self.predictions = []
        self.results = []
        self.accuracy = 0.0