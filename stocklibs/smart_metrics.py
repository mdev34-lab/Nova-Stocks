from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QLineEdit, QScrollArea, QLabel)
from PySide6.QtCore import Qt
from .stockdata import fetch_pvp
from .stockdata import decidir_potencial_de_crescimento
from .assets import styles

class SmartMetricsWindow(QMainWindow):
    def __init__(self, ticker=None):
        super().__init__()
        self.setStyleSheet(styles.light_mode)
        self.ticker = ticker
        self.setup_ui()
        if ticker:
            self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Métricas Inteligentes")
        self.setMinimumSize(600, 400)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar métricas...")
        self.search_bar.textChanged.connect(self.filter_metrics)
        layout.addWidget(self.search_bar)

        # Scroll area for metrics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.metrics_widget = QWidget()
        self.metrics_layout = QVBoxLayout(self.metrics_widget)
        self.metrics_layout.setAlignment(Qt.AlignTop)  # Align metrics to the top
        self.metrics_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.metrics_layout.setSpacing(0)  # Remove spacing
        scroll.setWidget(self.metrics_widget)
        layout.addWidget(scroll)

        # Initialize metrics indicators
        self.valuation_status_indicator = QLabel("Status de Valorização: Não Disponível")
        self.metrics_layout.addWidget(self.valuation_status_indicator)

        # Initialize potencial de crescimento indicator
        self.potencial_crescimento_indicator = QLabel("Potencial de Crescimento Avaliado Automaticamente: Não Disponível")
        self.metrics_layout.addWidget(self.potencial_crescimento_indicator)

    def filter_metrics(self):
        search_text = self.search_bar.text().lower()  # Obter texto da barra de busca
        # Atualizar a visibilidade dos indicadores com base no texto de busca
        for i in range(self.metrics_layout.count()):
            indicator = self.metrics_layout.itemAt(i).widget()
            if isinstance(indicator, QLabel):
                if search_text in indicator.text().lower():
                    indicator.show()  # Mostrar se corresponder
                else:
                    indicator.hide()  # Ocultar se não corresponder

    def load_data(self):
        # Logic to load data for the given ticker
        pvp_value = self.get_pvp_value()  # Assume this method fetches the P/VP value
        status = self.calculate_valuation_status(pvp_value)

        # Define color based on status
        if status == "Subvalorizado":
            color = "green"
        elif status == "Supervalorizado":
            color = "red"
        else:
            color = "black"  # Default color for Balanceado

        # Update the indicator text with color
        self.valuation_status_indicator.setText(f"Status de Valorização: <b><span style='color: {color};'>{status}</span></b>")

        # Adicionar o indicador de potencial de crescimento
        potencial_crescimento, taxa_confianca = decidir_potencial_de_crescimento(self.ticker)

        # Definir a cor com base no potencial de crescimento
        if potencial_crescimento == 'Acima da média':
            cor_crescimento = 'green'
        elif potencial_crescimento == 'Abaixo da média':
            cor_crescimento = 'red'
        else:
            cor_crescimento = 'black'  # Para 'Dados insuficientes' ou 'Regular'

        # Atualizar o texto do indicador de potencial de crescimento
        self.potencial_crescimento_indicator.setText(f"Potencial de Crescimento (avaliado automaticamente): <b><span style='color: {cor_crescimento};'>{potencial_crescimento} ({taxa_confianca:.2f}% de confiança)</span></b>")

    def calculate_valuation_status(self, pvp):
        if pvp == "Indisponível": return "Indisponível"
        if pvp < 0.95:
            return "Subvalorizado"
        elif 0.95 <= pvp <= 1.05:
            return "Balanceado"
        else:
            return "Supervalorizado"

    def get_pvp_value(self):
        # Fetch the P/VP value using the stockdata module
        try:
            return float(fetch_pvp(self.ticker))  # Use the ticker to get the P/VP
        except TypeError:
            return "Indisponível"