from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                 QLineEdit, QScrollArea, QLabel)
import yfinance as yf
from PySide6.QtCore import Qt
from .stockdata import (fetch_stock_data, fetch_monthly_financials, convert_to_brl_naturallanguage)
from . import stockdata
from .assets import styles

class MetricsWindow(QMainWindow):
    def __init__(self, ticker=None):
        super().__init__()
        self.setStyleSheet(styles.light_mode)
        self.ticker = ticker
        self.setup_ui()
        if ticker:
            self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Métricas Detalhadas")
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
        self.pvp_indicator = QLabel("P/VP: 0")
        self.pe_indicator = QLabel("P/L: 0")
        self.roe_indicator = QLabel("ROE: 0")
        self.dividend_yield_indicator = QLabel("Dividend Yield: 0")
        self.debt_to_ebitda_indicator = QLabel("Dívida/EBITDA: 0")
        self.net_margin_indicator = QLabel("Margem Líquida: 0")
        self.shares_outstanding_indicator = QLabel("Ações em Circulação: 0")
        self.equity_indicator = QLabel("Capital Próprio: R$ 0.00")
        self.total_liabilities_indicator = QLabel("Total de Passivos: R$ 0.00")
        self.total_assets_indicator = QLabel("Total de Ativos: R$ 0.00")
        self.cash_and_short_term_investments_indicator = QLabel("Dinheiro e Investimentos de Curto Prazo: R$ 0.00")
        self.net_income_indicator = QLabel("Renda Líquida: R$ 0.00")
        self.ebitda_indicator = QLabel("LAJIDA: R$ 0.00")
        self.depreciation_expenses_indicator = QLabel("Despesas com Amortização: R$ 0.00")
        self.interest_expenses_indicator = QLabel("Despesas com Juros: R$ 0.00")
        self.total_expenses_indicator = QLabel("Despesas Totais: R$ 0.00")

        # Initialize metrics labels dictionary
        self.metric_labels = {}

    def load_data(self):
        if not self.ticker:
            return

        ticker = self.ticker + ".SA" if not self.ticker.endswith(".SA") else self.ticker
        
        # Fetch all data
        stock_data = fetch_stock_data(ticker.upper())
        financial_data = fetch_monthly_financials(ticker.upper())

        # Fetch some data
        pvp = stockdata.fetch_pvp(ticker.upper())
        pe = stockdata.fetch_pe(ticker.upper())
        roe = stockdata.fetch_roe(ticker.upper())
        dividend_yield = stockdata.fetch_dividend_yield(ticker.upper())
        debt_to_ebitda = stockdata.fetch_debt_to_ebitda(ticker.upper())
        net_margin = stockdata.fetch_net_margin(ticker.upper())

        # Retrieve key financial data
        shares_outstanding = stock_data['sharesOutstanding']  # Ações em circulação
        equity = stock_data['equity']
        total_liabilities = stock_data['totalLiabilities']
        total_assets = stock_data['totalAssets']
        cash = stock_data['cash']
        short_term_investments = stock_data['shortTermInvestments']
        net_income = float(''.join(filter(str.isdigit, financial_data['net_income']))) \
            if not isinstance(financial_data['net_income'], (int, float)) \
            else financial_data['net_income']
        ebitda = float(''.join(filter(str.isdigit, financial_data['ebitda']))) \
            if not isinstance(financial_data['ebitda'], (int, float)) \
            else financial_data['ebitda']
        depreciation_expenses = float(''.join(filter(str.isdigit, financial_data['depreciation_expenses']))) \
            if not isinstance(financial_data['depreciation_expenses'], (int, float)) \
            else financial_data['depreciation_expenses']
        interest_expenses = float(''.join(filter(str.isdigit, financial_data['interest_expenses']))) \
            if not isinstance(financial_data['interest_expenses'], (int, float)) \
            else financial_data['interest_expenses']
        total_expenses = float(''.join(filter(str.isdigit, financial_data['total_expenses']))) \
            if not isinstance(financial_data['total_expenses'], (int, float)) \
            else financial_data['total_expenses']

        # Update metrics indicators with fetched data
        self.pvp_indicator.setText(f"P/VP: {pvp}")
        self.pe_indicator.setText(f"P/L: {pe}")
        self.roe_indicator.setText(f"ROE: {roe}")
        self.dividend_yield_indicator.setText(f"Dividend Yield: {dividend_yield}")
        self.debt_to_ebitda_indicator.setText(f"Dívida/EBITDA: {debt_to_ebitda:.2f}")
        self.net_margin_indicator.setText(f"Margem Líquida: {net_margin}")
        self.shares_outstanding_indicator.setText(f"Ações em Circulação: {convert_to_brl_naturallanguage(shares_outstanding)}")
        if equity != 'Indeterminado': self.equity_indicator.setText(f"Capital Próprio: R$ {equity:.2f}")
        else: self.equity_indicator.setText(f"Capital Próprio: {equity}")
        self.total_liabilities_indicator.setText(f"Total de Passivos: {convert_to_brl_naturallanguage(total_liabilities)}")
        self.total_assets_indicator.setText(f"Total de Ativos: {convert_to_brl_naturallanguage(total_assets)}")
        if cash != 'Indeterminado' and short_term_investments != 'Indeterminado': self.cash_and_short_term_investments_indicator.setText(f"Dinheiro e Investimentos de Curto Prazo: R$ {cash + short_term_investments:.2f}")
        else: self.cash_and_short_term_investments_indicator.setText(f"Dinheiro e Investimentos de Curto Prazo: Indeterminado")
        self.net_income_indicator.setText(f"Renda Líquida: {convert_to_brl_naturallanguage(net_income)}")
        self.ebitda_indicator.setText(f"LAJIDA: {convert_to_brl_naturallanguage(ebitda)}")
        self.depreciation_expenses_indicator.setText(f"Despesas com Amortização: {convert_to_brl_naturallanguage(depreciation_expenses)}")
        self.interest_expenses_indicator.setText(f"Despesas com Juros: {convert_to_brl_naturallanguage(interest_expenses)}")
        self.total_expenses_indicator.setText(f"Despesas Totais: {convert_to_brl_naturallanguage(total_expenses)}")

        # Combine all metrics
        self.all_metrics = {
            # Basic Info
            "Último Fechamento": stock_data.get('last_close', 'Indeterminado'),
            "Variações de Hoje": stock_data.get('today_variation', 'Indeterminado'),
            "Variações do Ano": stock_data.get('year_variation', 'Indeterminado'),
            "Capitalização de Mercado": stock_data.get('market_cap', 'Indeterminado'),
            "Volume Médio": stock_data.get('average_volume', 'Indeterminado'),
            "Rendimento de Dividendos": self.dividend_yield_indicator.text().split(': ')[1],
            "Bolsa Principal": stock_data.get('main_exchange', 'Indeterminado'),
            
            # Main Metrics
            "P/VP": self.pvp_indicator.text().split(': ')[1],
            "P/L": self.pe_indicator.text().split(': ')[1],
            "ROE": self.roe_indicator.text().split(': ')[1],
            "Dívida/EBITDA": self.debt_to_ebitda_indicator.text().split(': ')[1],
            "Margem Líquida": self.net_margin_indicator.text().split(': ')[1],
            "Ações em Circulação": self.shares_outstanding_indicator.text().split(': ')[1],
            "Total de Passivos": self.total_liabilities_indicator.text().split(': ')[1],
            "Total de Ativos": self.total_assets_indicator.text().split(': ')[1],
            "Renda Líquida": self.net_income_indicator.text().split(': ')[1],
            "LAJIDA": self.ebitda_indicator.text().split(': ')[1],
            "Despesas com Amortização": self.depreciation_expenses_indicator.text().split(': ')[1],
            "Despesas com Juros": self.interest_expenses_indicator.text().split(': ')[1],
            "Despesas Totais": self.total_expenses_indicator.text().split(': ')[1],
            
            # Financial Info
            "Receita": financial_data.get('revenue', 'Indeterminado'),
            "Gastos Operacionais": financial_data.get('operating_expenses', 'Indeterminado'),
            "Lucros por Ação": financial_data.get('earnings_per_share', 'Indeterminado'),
            "Margem de Lucro Líquida": financial_data.get('net_profit_margin', 'Indeterminado'),
            "Carga Tributária Efetiva": financial_data.get('effective_tax_rate', 'Indeterminado'),
            "Despesas com Pesquisa e Desenvolvimento": financial_data.get('research_and_development_expenses', 'Indeterminado'),
            "Despesas com Vendas, Geral e Administrativa": financial_data.get('selling_general_and_administrative_expenses', 'Indeterminado'),
        }

        self.display_metrics(self.all_metrics)

    def display_metrics(self, metrics_dict):
        # Clear existing metrics
        for label in self.metric_labels.values():
            label.deleteLater()
        self.metric_labels.clear()

        # Add metrics to layout
        for key, value in metrics_dict.items():
            label = QLabel(f"<b>{key}:</b> {value}")
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setWordWrap(True)

            # Set text interaction flags to allow selection
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.metrics_layout.addWidget(label)
            self.metric_labels[key] = label

    def filter_metrics(self, search_text):
        if not search_text:
            # Show all metrics if search is empty
            filtered_metrics = self.all_metrics
        else:
            # Filter metrics based on search text
            search_text = search_text.lower()
            filtered_metrics = {
                key: value for key, value in self.all_metrics.items()
                if search_text in key.lower() or 
                   (isinstance(value, str) and search_text in value.lower())
            }

        self.display_metrics(filtered_metrics)

    def set_ticker(self, ticker):
        self.ticker = ticker
        self.load_data()
