#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Baccarat oyun mantığı ve veri yapıları
"""

class Game:
    """Baccarat oyunu ile ilgili temel işlemleri içeren sınıf"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Oyun verilerini sıfırla"""
        self.player_count = 0
        self.banker_count = 0
        self.tie_count = 0
        self.history = []  # Oyun sonuçları geçmişi
    
    def add_result(self, result):
        """
        Oyun sonucu ekle
        
        Args:
            result (str): 'P' (Player), 'B' (Banker) veya 'T' (Tie)
        """
        if result not in ['P', 'B', 'T']:
            raise ValueError("Geçersiz sonuç: 'P', 'B' veya 'T' olmalı")
        
        # Sayaçları güncelle
        if result == 'P':
            self.player_count += 1
        elif result == 'B':
            self.banker_count += 1
        else:  # 'T'
            self.tie_count += 1
        
        # Geçmişe ekle
        self.history.append(result)
    
    def get_stats(self):
        """
        Oyun istatistiklerini döndür
        
        Returns:
            dict: Oyun istatistikleri
        """
        total_hands = self.player_count + self.banker_count + self.tie_count
        
        return {
            'player_count': self.player_count,
            'banker_count': self.banker_count,
            'tie_count': self.tie_count,
            'total_hands': total_hands,
            'player_percentage': (self.player_count / total_hands * 100) if total_hands > 0 else 0,
            'banker_percentage': (self.banker_count / total_hands * 100) if total_hands > 0 else 0,
            'tie_percentage': (self.tie_count / total_hands * 100) if total_hands > 0 else 0
        }
    
    def get_history(self, limit=None):
        """
        Oyun geçmişini döndür
        
        Args:
            limit (int, optional): Döndürülecek sonuç sayısı
            
        Returns:
            list: Oyun sonuçları listesi
        """
        if limit is None:
            return self.history
        return self.history[-limit:]
    
    def get_last_n_results(self, n=10):
        """
        Son n oyun sonucunu döndür
        
        Args:
            n (int): İstenilen sonuç sayısı
            
        Returns:
            list: Son n oyun sonucu
        """
        return self.get_history(n)


class MatrixAnalyzer:
    """5x5 matris analizi sınıfı"""
    
    @staticmethod
    def extract_patterns(matrix):
        """
        5x5 Matrisinden desen çıkar
        
        Args:
            matrix (list): 5x5 matris (2D liste)
            
        Returns:
            dict: Çıkarılan desenler
        """
        patterns = {
            'rows': [],       # Satır desenleri
            'columns': [],    # Sütun desenleri
            'diagonals': [],  # Köşegen desenler
            'blocks': []      # 2x2 bloklar
        }
        
        # Satır desenleri
        for row in matrix:
            pattern = [cell for cell in row if cell is not None]
            if pattern:
                patterns['rows'].append(pattern)
        
        # Sütun desenleri
        for col in range(5):
            pattern = []
            for row in range(5):
                if matrix[row][col] is not None:
                    pattern.append(matrix[row][col])
            if pattern:
                patterns['columns'].append(pattern)
        
        # Köşegen desenler (ana köşegen)
        diagonal = []
        for i in range(5):
            if matrix[i][i] is not None:
                diagonal.append(matrix[i][i])
        if diagonal:
            patterns['diagonals'].append(diagonal)
        
        # Köşegen desenler (ters köşegen)
        diagonal = []
        for i in range(5):
            if matrix[i][4-i] is not None:
                diagonal.append(matrix[i][4-i])
        if diagonal:
            patterns['diagonals'].append(diagonal)
        
        # 2x2 bloklar
        for row in range(4):
            for col in range(4):
                block = [
                    matrix[row][col], matrix[row][col+1],
                    matrix[row+1][col], matrix[row+1][col+1]
                ]
                # None olmayan değerleri filtrele
                block = [cell for cell in block if cell is not None]
                if len(block) >= 3:  # En az 3 hücre dolu ise
                    patterns['blocks'].append(block)
        
        return patterns
    
    @staticmethod
    def count_sequences(matrix):
        """
        Matristeki Player ve Banker dizilerini say
        
        Args:
            matrix (list): 5x5 matris (2D liste)
            
        Returns:
            dict: Dizi sayıları
        """
        # Matrisi düzleştir ve None olmayan değerleri al
        flat_matrix = [cell for row in matrix for cell in row if cell is not None]
        
        # Farklı dizileri say
        sequences = {
            'P': 0,   # Tek 'P'
            'B': 0,   # Tek 'B'
            'PP': 0,  # İki ardışık 'P'
            'BB': 0,  # İki ardışık 'B'
            'PB': 0,  # 'P' sonra 'B'
            'BP': 0,  # 'B' sonra 'P'
            'PPP': 0, # Üç ardışık 'P'
            'BBB': 0, # Üç ardışık 'B'
            'PPB': 0, # İki 'P' sonra 'B'
            'PBB': 0, # Bir 'P' sonra iki 'B'
            'BPP': 0, # Bir 'B' sonra iki 'P'
            'BBP': 0, # İki 'B' sonra 'P'
        }
        
        # Tek değerleri say
        sequences['P'] = flat_matrix.count('P')
        sequences['B'] = flat_matrix.count('B')
        
        # İki ve üç ardışık değerleri say
        for i in range(len(flat_matrix) - 1):
            pair = flat_matrix[i] + flat_matrix[i+1]
            if pair in sequences:
                sequences[pair] += 1
            
            if i < len(flat_matrix) - 2:
                triplet = flat_matrix[i] + flat_matrix[i+1] + flat_matrix[i+2]
                if triplet in sequences:
                    sequences[triplet] += 1
        
        return sequences


class GameAnalyzer:
    """Oyun sonuçları analizi sınıfı"""
    
    @staticmethod
    def analyze_trends(history, window_size=10):
        """
        Oyun geçmişindeki trendleri analiz et
        
        Args:
            history (list): Oyun sonuçları listesi ('P', 'B', 'T')
            window_size (int): Analiz penceresi boyutu
            
        Returns:
            dict: Analiz sonuçları
        """
        if not history or len(history) < window_size:
            return None
        
        # Son window_size kadar sonucu al
        recent = history[-window_size:]
        
        p_count = recent.count('P')
        b_count = recent.count('B')
        t_count = recent.count('T')
        
        # Son oyunlardaki dağılım
        distribution = {
            'P': p_count / window_size,
            'B': b_count / window_size,
            'T': t_count / window_size
        }
        
        # Ardışık oyunları say
        streaks = {
            'P': 0,  # Mevcut Player dizisi
            'B': 0,  # Mevcut Banker dizisi
            'max_P': 0,  # En uzun Player dizisi
            'max_B': 0   # En uzun Banker dizisi
        }
        
        current_streak = None
        current_count = 0
        
        for result in recent:
            if result == 'T':  # Tie'lar dizi sayımını etkilemez
                continue
                
            if result == current_streak:
                current_count += 1
            else:
                # Yeni dizi başladı
                if current_streak == 'P':
                    streaks['max_P'] = max(streaks['max_P'], current_count)
                elif current_streak == 'B':
                    streaks['max_B'] = max(streaks['max_B'], current_count)
                
                current_streak = result
                current_count = 1
        
        # Son diziyi kontrol et
        if current_streak == 'P':
            streaks['P'] = current_count
            streaks['max_P'] = max(streaks['max_P'], current_count)
        elif current_streak == 'B':
            streaks['B'] = current_count
            streaks['max_B'] = max(streaks['max_B'], current_count)
        
        # Alternans (P-B değişim) oranı hesapla
        alternations = 0
        for i in range(len(recent) - 1):
            if recent[i] != recent[i + 1] and recent[i] != 'T' and recent[i + 1] != 'T':
                alternations += 1
        
        alternation_rate = alternations / (window_size - 1) if window_size > 1 else 0
        
        return {
            'distribution': distribution,
            'streaks': streaks,
            'alternation_rate': alternation_rate,
            'last_result': recent[-1]
        }