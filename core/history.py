#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Baccarat tahmin geçmişi ve kayıt yönetimi
"""

import os
import json
import csv
from datetime import datetime

class History:
    """Oyun ve tahmin geçmişini yöneten sınıf"""
    
    def __init__(self, history_dir='history'):
        """
        Inicializasyon
        
        Args:
            history_dir (str): Geçmiş dosyalarının saklanacağı dizin
        """
        self.history_dir = history_dir
        self.session_history = []
        self.ensure_history_dir()
    
    def ensure_history_dir(self):
        """Geçmiş dizininin var olduğundan emin ol"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def add_result(self, result, prediction, timestamp=None):
        """
        Yeni bir oyun sonucu ve tahmin ekle
        
        Args:
            result (str): Gerçek sonuç ('P', 'B' veya 'T')
            prediction (str): Yapılan tahmin ('P' veya 'B')
            timestamp (datetime, optional): Zaman damgası
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        entry = {
            'timestamp': timestamp,
            'result': result,
            'prediction': prediction,
            'correct': result == prediction
        }
        
        self.session_history.append(entry)
    
    def save_session(self, filename=None):
        """
        Mevcut oturum geçmişini dosyaya kaydet
        
        Args:
            filename (str, optional): Kaydedilecek dosya adı
            
        Returns:
            str: Kaydedilen dosyanın tam yolu
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"baccarat_session_{timestamp}.json"
        
        filepath = os.path.join(self.history_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.session_history, f, default=str, indent=2)
        
        return filepath
    
    def export_to_csv(self, filename=None):
        """
        Mevcut oturum geçmişini CSV dosyasına dışa aktar
        
        Args:
            filename (str, optional): Kaydedilecek dosya adı
            
        Returns:
            str: Kaydedilen dosyanın tam yolu
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"baccarat_session_{timestamp}.csv"
        
        filepath = os.path.join(self.history_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'result', 'prediction', 'correct']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for entry in self.session_history:
                writer.writerow(entry)
        
        return filepath
    
    def load_session(self, filepath):
        """
        Kaydedilmiş bir oturumu yükle
        
        Args:
            filepath (str): Yüklenecek dosyanın yolu
            
        Returns:
            list: Yüklenen oturum geçmişi
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dosya bulunamadı: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_history = json.load(f)
        
        # Zaman damgalarını datetime nesnelerine çevir
        for entry in loaded_history:
            if isinstance(entry['timestamp'], str):
                try:
                    entry['timestamp'] = datetime.fromisoformat(entry['timestamp'])
                except ValueError:
                    # ISO formatı değilse, orijinal string değerini koru
                    pass
        
        self.session_history = loaded_history
        return loaded_history
    
    def clear_session(self):
        """Mevcut oturum geçmişini temizle"""
        self.session_history = []
    
    def get_session_stats(self):
        """
        Mevcut oturum istatistiklerini hesapla
        
        Returns:
            dict: Oturum istatistikleri
        """
        total_predictions = len(self.session_history)
        if total_predictions == 0:
            return {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy': 0,
                'player_predictions': 0,
                'banker_predictions': 0,
                'player_results': 0,
                'banker_results': 0,
                'tie_results': 0
            }
        
        correct_predictions = sum(1 for entry in self.session_history if entry['correct'])
        
        player_predictions = sum(1 for entry in self.session_history if entry['prediction'] == 'P')
        banker_predictions = sum(1 for entry in self.session_history if entry['prediction'] == 'B')
        
        player_results = sum(1 for entry in self.session_history if entry['result'] == 'P')
        banker_results = sum(1 for entry in self.session_history if entry['result'] == 'B')
        tie_results = sum(1 for entry in self.session_history if entry['result'] == 'T')
        
        return {
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'accuracy': correct_predictions / total_predictions * 100,
            'player_predictions': player_predictions,
            'banker_predictions': banker_predictions,
            'player_results': player_results,
            'banker_results': banker_results,
            'tie_results': tie_results
        }
    
    def get_predictions(self, limit=None):
        """
        Oturum tahminlerini döndür
        
        Args:
            limit (int, optional): Döndürülecek tahmin sayısı
            
        Returns:
            list: Tahminler listesi ('P' veya 'B')
        """
        predictions = [entry['prediction'] for entry in self.session_history]
        
        if limit is None:
            return predictions
        return predictions[-limit:]
    
    def get_results(self, limit=None):
        """
        Oturum sonuçlarını döndür
        
        Args:
            limit (int, optional): Döndürülecek sonuç sayısı
            
        Returns:
            list: Sonuçlar listesi ('P', 'B' veya 'T')
        """
        results = [entry['result'] for entry in self.session_history]
        
        if limit is None:
            return results
        return results[-limit:]