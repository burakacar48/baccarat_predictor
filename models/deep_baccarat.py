#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
İstatistiksel tabanlı Baccarat tahmin modeli
"""

from models.base_model import BaseModel
from core.game import MatrixAnalyzer, GameAnalyzer
import random
import math

class DeepBaccarat(BaseModel):
    """İstatistiksel analiz ile tahmin yapan model"""
    
    def __init__(self):
        """Inicializasyon"""
        super().__init__(name="DEEP BACCARAT")
        self.analyzer = MatrixAnalyzer()
        self.game_analyzer = GameAnalyzer()
        
        # İstatistiksel katsayılar
        self.banker_bias = 0.0046  # Banker'ın gerçek avantajı (yaklaşık %0.46)
        
        # Tahmin faktörleri
        self.factors = {
            'historical_bias': 0.30,    # Gerçek istatistiklere dayalı yanlılık
            'recent_patterns': 0.35,    # Son sonuçlardaki desenler
            'streak_analysis': 0.20,    # Dizilerin analizi
            'head_to_head': 0.15        # P ve B sayıları karşılaştırması
        }
    
    def predict(self, matrix, history=None):
        """
        İstatistiksel analiz ile tahmin yap
        
        Args:
            matrix (list): 5x5 matris (2D liste)
            history (list, optional): Oyun sonuçları geçmişi
            
        Returns:
            tuple: (tahmin, güven skoru)
        """
        # Matristen veri çıkar
        patterns = self.analyzer.extract_patterns(matrix)
        sequences = self.analyzer.count_sequences(matrix)
        
        # Geçmiş oyun sonuçlarını analiz et
        trend_analysis = None
        if history and len(history) >= 10:
            trend_analysis = self.game_analyzer.analyze_trends(history)
        
        # Temel olasılıklar (gerçek Baccarat olasılıkları)
        p_probability = 0.4462  # Player kazanma olasılığı
        b_probability = 0.4585  # Banker kazanma olasılığı (komisyon olmadan)
        # Not: Tie olasılığı yaklaşık 0.0953 (burada kullanılmıyor)
        
        # 1. Gerçek olasılıklara dayalı yanlılık faktörü
        banker_bias_score = self.banker_bias
        
        # 2. Matris ve geçmiş analizi
        banker_score = b_probability + banker_bias_score
        player_score = p_probability
        
        # Katsayıları uygula
        matrix_p_score, matrix_b_score = self._analyze_sequences(sequences)
        historical_bias_factor = self.factors['historical_bias']
        player_score = player_score * historical_bias_factor + matrix_p_score * (1 - historical_bias_factor)
        banker_score = banker_score * historical_bias_factor + matrix_b_score * (1 - historical_bias_factor)
        
        # Eğer geçmiş verisi varsa, trend analizini kullan
        if trend_analysis:
            recent_p_score, recent_b_score = self._analyze_recent_trends(trend_analysis)
            streak_p_score, streak_b_score = self._analyze_streaks(trend_analysis)
            
            # Ağırlıklı ortalama hesapla
            recent_factor = self.factors['recent_patterns']
            streak_factor = self.factors['streak_analysis']
            head_to_head_factor = self.factors['head_to_head']
            
            # Mevcut skorları güncelle
            weighted_p_score = (
                player_score * (1 - recent_factor - streak_factor - head_to_head_factor) +
                recent_p_score * recent_factor +
                streak_p_score * streak_factor
            )
            
            weighted_b_score = (
                banker_score * (1 - recent_factor - streak_factor - head_to_head_factor) +
                recent_b_score * recent_factor +
                streak_b_score * streak_factor
            )
            
            # Head-to-head karşılaştırma
            h2h_p_score, h2h_b_score = self._head_to_head_comparison(trend_analysis)
            weighted_p_score += h2h_p_score * head_to_head_factor
            weighted_b_score += h2h_b_score * head_to_head_factor
            
            player_score = weighted_p_score
            banker_score = weighted_b_score
        
        # Tahmin ve güven hesapla
        prediction = 'P' if player_score > banker_score else 'B'
        
        # Güven skorunu hesapla (yüzde olarak)
        total_score = player_score + banker_score
        win_score = max(player_score, banker_score)
        confidence = (win_score / total_score) * 100
        
        # Güven skorunu 50-99.9 arasına sınırla
        confidence = min(99.9, max(50.0, confidence))
        
        return prediction, confidence
    
    def _analyze_sequences(self, sequences):
        """
        Dizi verilerini analiz et
        
        Args:
            sequences (dict): Dizi sayıları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        # Toplam P ve B sayıları
        p_count = sequences['P']
        b_count = sequences['B']
        total = p_count + b_count
        
        if total == 0:
            return 0.5, 0.5  # Veri yoksa, eşit olasılık
        
        # İkili ve üçlü dizilerin sayıları
        pp_count = sequences.get('PP', 0)
        bb_count = sequences.get('BB', 0)
        pb_count = sequences.get('PB', 0)
        bp_count = sequences.get('BP', 0)
        
        # Baccarat'ta temel olasılıklara göre banka lehine düzeltme
        base_p_prob = 0.4462
        base_b_prob = 0.4585
        
        # Dizi analizine dayalı olasılık ayarlamaları
        p_prob = base_p_prob
        b_prob = base_b_prob
        
        # Toplam orantıya göre düzeltme
        p_ratio = p_count / total
        b_ratio = b_count / total
        
        if p_ratio > 0.6:  # P fazla çıkmışsa, dengelenme eğilimi
            b_prob += 0.05
        elif b_ratio > 0.6:  # B fazla çıkmışsa, dengelenme eğilimi
            p_prob += 0.05
        
        # Son dizilerin analizi (PB ve BP desenleri)
        if pb_count > 0 and pp_count < pb_count:
            b_prob += 0.03  # P'den sonra genellikle B geliyorsa
        if bp_count > 0 and bb_count < bp_count:
            p_prob += 0.03  # B'den sonra genellikle P geliyorsa
        
        return p_prob, b_prob
    
    def _analyze_recent_trends(self, trend_analysis):
        """
        Son trendleri analiz et
        
        Args:
            trend_analysis (dict): Trend analizi sonuçları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        distribution = trend_analysis['distribution']
        
        p_ratio = distribution['P']
        b_ratio = distribution['B']
        
        # Banka lehine doğal avantaj
        adjusted_p_ratio = p_ratio
        adjusted_b_ratio = b_ratio + self.banker_bias
        
        # Sapma hesapla (ortalamadan)
        p_expected = 0.4462
        b_expected = 0.4585
        
        p_deviation = adjusted_p_ratio - p_expected
        b_deviation = adjusted_b_ratio - b_expected
        
        # Regresyon etkisi: Olasılıklar ortalamalara doğru eğilim gösterir
        p_score = p_expected - p_deviation * 0.7  # Sapmanın tersi yönünde düzeltme
        b_score = b_expected - b_deviation * 0.7
        
        # Son sonuca göre ek düzeltme
        last_result = trend_analysis['last_result']
        if last_result == 'P':
            b_score += 0.02  # P sonrası B olasılığı hafif artar
        elif last_result == 'B':
            p_score += 0.02  # B sonrası P olasılığı hafif artar
        
        return p_score, b_score
    
    def _analyze_streaks(self, trend_analysis):
        """
        Dizilerin analizini yap
        
        Args:
            trend_analysis (dict): Trend analizi sonuçları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        streaks = trend_analysis['streaks']
        
        # Mevcut diziler
        current_p_streak = streaks.get('P', 0)
        current_b_streak = streaks.get('B', 0)
        
        # Temel olasılıklar
        p_score = 0.4462
        b_score = 0.4585
        
        # Uzun dizilerin kırılma eğilimi (exponensiyal artan düzeltme)
        if current_p_streak >= 2:
            factor = 1 - math.exp(-0.3 * current_p_streak)  # Dizi uzadıkça artan faktör
            streak_correction = 0.1 * factor
            p_score -= streak_correction
            b_score += streak_correction
        
        if current_b_streak >= 2:
            factor = 1 - math.exp(-0.3 * current_b_streak)
            streak_correction = 0.1 * factor
            b_score -= streak_correction
            p_score += streak_correction
        
        # Alternans oranına göre düzeltme
        alternation_rate = trend_analysis.get('alternation_rate', 0)
        
        if alternation_rate > 0.7:  # Sık değişim varsa
            # Son sonucun tersine yönlendirme
            last_result = trend_analysis['last_result']
            if last_result == 'P':
                p_score -= 0.05
                b_score += 0.05
            elif last_result == 'B':
                b_score -= 0.05
                p_score += 0.05
        elif alternation_rate < 0.3:  # Az değişim varsa (desenler devam ediyor)
            # Son sonucun tekrarına yönlendirme
            last_result = trend_analysis['last_result']
            if last_result == 'P':
                p_score += 0.03
                b_score -= 0.03
            elif last_result == 'B':
                b_score += 0.03
                p_score -= 0.03
        
        return p_score, b_score
    
    def _head_to_head_comparison(self, trend_analysis):
        """
        P ve B sonuçlarının doğrudan karşılaştırması
        
        Args:
            trend_analysis (dict): Trend analizi sonuçları
            
        Returns:
            tuple: (player_score, banker_score)
        """
        distribution = trend_analysis['distribution']
        
        p_ratio = distribution['P']
        b_ratio = distribution['B']
        
        # Fark hesapla
        difference = abs(p_ratio - b_ratio)
        
        # Temel olasılıklar
        p_score = 0.4462
        b_score = 0.4585
        
        if difference > 0.2:  # Büyük fark varsa, dengelenme eğilimi
            if p_ratio > b_ratio:
                # P fazla çıkmışsa, B olasılığını artır
                adjustment = min(difference * 0.5, 0.15)  # Maksimum düzeltme
                p_score -= adjustment
                b_score += adjustment
            else:
                # B fazla çıkmışsa, P olasılığını artır
                adjustment = min(difference * 0.5, 0.15)
                b_score -= adjustment
                p_score += adjustment
        
        return p_score, b_score