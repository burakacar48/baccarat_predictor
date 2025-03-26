#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Desen tabanlı Baccarat tahmin modeli
"""

from models.base_model import BaseModel
from core.game import MatrixAnalyzer, GameAnalyzer

class PatternAI(BaseModel):
    """Desen tanıma ile tahmin yapan model"""
    
    def __init__(self):
        """Inicializasyon"""
        super().__init__(name="PATTERN AI")
        self.analyzer = MatrixAnalyzer()
        self.game_analyzer = GameAnalyzer()
        
        # Desen ağırlıkları
        self.weights = {
            'recent_trend': 0.4,   # Son trend ağırlığı
            'streaks': 0.3,        # Dizi analizi ağırlığı
            'matrix_patterns': 0.3 # Matris desenleri ağırlığı
        }
    
    def predict(self, matrix, history=None):
        """
        Desen analizi ile tahmin yap
        
        Args:
            matrix (list): 5x5 matris (2D liste)
            history (list, optional): Oyun sonuçları geçmişi
            
        Returns:
            tuple: (tahmin, güven skoru)
        """
        # Matristen örüntüleri çıkar
        patterns = self.analyzer.extract_patterns(matrix)
        
        # Dizi sayılarını hesapla
        sequences = self.analyzer.count_sequences(matrix)
        
        # Eğilim analizi (history varsa)
        trend_analysis = None
        if history and len(history) >= 10:
            trend_analysis = self.game_analyzer.analyze_trends(history)
        
        # Tahmin skorlarını hesapla
        player_score = 0
        banker_score = 0
        confidence = 0
        
        # 1. Matris desenleri analizi (toplam ağırlık: 0.3)
        matrix_player_score, matrix_banker_score = self._analyze_matrix_patterns(patterns, sequences)
        pattern_weight = self.weights['matrix_patterns']
        player_score += matrix_player_score * pattern_weight
        banker_score += matrix_banker_score * pattern_weight
        
        # 2. Oyun geçmişi analizi (toplam ağırlık: 0.7)
        if trend_analysis:
            # Son trend analizi (toplam ağırlık: 0.4)
            trend_player_score, trend_banker_score = self._analyze_trends(trend_analysis)
            trend_weight = self.weights['recent_trend']
            player_score += trend_player_score * trend_weight
            banker_score += trend_banker_score * trend_weight
            
            # Dizi analizi (toplam ağırlık: 0.3)
            streak_player_score, streak_banker_score = self._analyze_streaks(trend_analysis)
            streak_weight = self.weights['streaks']
            player_score += streak_player_score * streak_weight
            banker_score += streak_banker_score * streak_weight
        
        # Tahmin ve güven hesapla
        prediction = 'P' if player_score > banker_score else 'B'
        
        # Güven skorunu hesapla (0-100 arası)
        total_score = player_score + banker_score
        if total_score > 0:
            win_score = max(player_score, banker_score)
            confidence = (win_score / total_score) * 100
            confidence = min(99.9, max(50.0, confidence))  # 50-99.9 arasına sınırla
        else:
            confidence = 50.0  # Varsayılan değer
        
        return prediction, confidence
    
    def _analyze_matrix_patterns(self, patterns, sequences):
        """
        Matris desenlerini analiz et
        
        Args:
            patterns (dict): Çıkarılan desenler
            sequences (dict): Dizi sayıları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        player_score = 0
        banker_score = 0
        
        # 1. Toplam P ve B sayıları
        p_count = sequences['P']
        b_count = sequences['B']
        
        # Banker genellikle daha yüksek kazanma şansına sahip
        # Bu yüzden burada hafif bir düzeltme uygulanır
        adjusted_p = p_count * 1.05  # Player'a hafif ağırlık ver
        adjusted_b = b_count
        
        # Eğer toplam sayılar dengeli değilse, daha az olanın lehine puan ver
        if adjusted_p > adjusted_b * 1.5:
            banker_score += 0.6  # Banker çok az çıktıysa, Banker'ın gelmesi daha olası
        elif adjusted_b > adjusted_p * 1.5:
            player_score += 0.6  # Player çok az çıktıysa, Player'ın gelmesi daha olası
        
        # 2. İkili dizileri analiz et
        pp_count = sequences['PP']
        bb_count = sequences['BB']
        pb_count = sequences['PB']
        bp_count = sequences['BP']
        
        # Alternan desenler (PB, BP) güçlü göstergelerdir
        if pb_count > pp_count:
            banker_score += 0.4  # P sonrası B gelme olasılığı yüksek
        if bp_count > bb_count:
            player_score += 0.4  # B sonrası P gelme olasılığı yüksek
        
        # 3. Üçlü dizileri analiz et
        ppp_count = sequences['PPP']
        bbb_count = sequences['BBB']
        
        # Uzun tek tip diziler genellikle tersine döner
        if ppp_count > 0:
            banker_score += 0.3
        if bbb_count > 0:
            player_score += 0.3
        
        return player_score, banker_score
    
    def _analyze_trends(self, trend_analysis):
        """
        Son trendleri analiz et
        
        Args:
            trend_analysis (dict): Trend analizi sonuçları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        player_score = 0
        banker_score = 0
        
        distribution = trend_analysis['distribution']
        
        # Dağılım analizi
        p_ratio = distribution['P']
        b_ratio = distribution['B']
        
        # Banker lehine hafif düzeltme (gerçek Baccarat olasılıklarını yansıtır)
        adjusted_p = p_ratio
        adjusted_b = b_ratio * 1.05
        
        # Oran farkı büyükse, daha düşük orana sahip sonucu tercih et
        if adjusted_p > adjusted_b * 1.5:
            banker_score += 0.7  # Banker az çıkmışsa, Banker olasılığı yüksek
        elif adjusted_b > adjusted_p * 1.5:
            player_score += 0.7  # Player az çıkmışsa, Player olasılığı yüksek
        
        # Son sonuca göre analiz
        last_result = trend_analysis['last_result']
        
        if last_result == 'P':
            # Son sonuç P ise, sonraki sonuç B olma eğiliminde olabilir
            banker_score += 0.3
        elif last_result == 'B':
            # Son sonuç B ise, sonraki sonuç P olma eğiliminde olabilir
            player_score += 0.3
        
        return player_score, banker_score
    
    def _analyze_streaks(self, trend_analysis):
        """
        Dizi durumunu analiz et
        
        Args:
            trend_analysis (dict): Trend analizi sonuçları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        player_score = 0
        banker_score = 0
        
        streaks = trend_analysis['streaks']
        alternation_rate = trend_analysis['alternation_rate']
        
        # Mevcut diziler
        current_p_streak = streaks['P']
        current_b_streak = streaks['B']
        
        # Maksimum diziler
        max_p_streak = streaks['max_P']
        max_b_streak = streaks['max_B']
        
        # Alternans oranı yüksekse (P-B-P-B sık değişiyorsa)
        if alternation_rate > 0.6:
            # Son sonuç neyse, tersini tahmin et
            last_result = trend_analysis['last_result']
            if last_result == 'P':
                banker_score += 0.5
            elif last_result == 'B':
                player_score += 0.5
        
        # Uzun diziler genellikle bozulur
        if current_p_streak >= 3:
            banker_score += min(0.6, current_p_streak * 0.1)  # P dizisi uzunsa, B olasılığı artar
        if current_b_streak >= 3:
            player_score += min(0.6, current_b_streak * 0.1)  # B dizisi uzunsa, P olasılığı artar
        
        # Eğer bir dizi tipi hiç yoksa veya çok azsa, o tipin gelme olasılığı artar
        if max_p_streak == 0 or (max_p_streak == 1 and current_p_streak == 0):
            player_score += 0.4
        if max_b_streak == 0 or (max_b_streak == 1 and current_b_streak == 0):
            banker_score += 0.4
        
        return player_score, banker_score