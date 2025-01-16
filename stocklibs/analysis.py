from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class StockAnalysis:
    medias: list = field(default_factory=list)
    plot_history: list = field(default_factory=list)  # Initialize the history stack
    
    start_date: date = field(default_factory=lambda: date.today() - timedelta(days=365))
    end_date: date = field(default_factory=date.today)
    
    ma_period: int = 9
    candlestick_period: int = 1  # Default candlestick period in days
    
    ticker: str = None  # Initialize ticker attribute
    
    show_volume: bool = False
    show_ifr: bool = False  # New attribute to track IFR visibility
    show_macd: bool = False  # New attribute to track MACD visibility
    show_bandas_bollinger: bool = False  # New attribute to track Bollinger Bands visibility
    show_estocastico_normal: bool = False  # New attribute to track Estocástico Normal visibility
    show_estocastico_lento: bool = False  # New attribute to track Estocástico Lento visibility
    show_buy_signals: bool = False  # New attribute to track buy signals visibility
    
    candlestick_cache: dict = field(default_factory=dict)  # Cache para armazenar dados dos candlesticks

    def toggle_ifr(self):
        self.show_ifr = not self.show_ifr
        self.show_macd, self.show_estocastico_normal, self.show_estocastico_lento, self.show_buy_signals, self.show_volume = False, False, False, False, False

    def toggle_macd(self):
        self.show_macd = not self.show_macd
        self.show_ifr, self.show_estocastico_normal, self.show_estocastico_lento, self.show_buy_signals, self.show_volume = False, False, False, False, False

    def toggle_estocastico_normal(self):
        self.show_estocastico_normal = not self.show_estocastico_normal
        self.show_ifr, self.show_macd, self.show_estocastico_lento, self.show_buy_signals, self.show_volume = False, False, False, False, False

    def toggle_estocastico_lento(self):
        self.show_estocastico_lento = not self.show_estocastico_lento
        self.show_ifr, self.show_macd, self.show_estocastico_normal, self.show_buy_signals, self.show_volume = False, False, False, False, False

    def mostrar_bandas_bollinger(self):
        self.show_bandas_bollinger = not self.show_bandas_bollinger

    def show_volumes(self):
        self.show_volume = not self.show_volume  # Alterna o estado de exibição do volume   
        self.show_ifr, self.show_macd, self.show_estocastico_normal, self.show_estocastico_lento = False, False, False, False