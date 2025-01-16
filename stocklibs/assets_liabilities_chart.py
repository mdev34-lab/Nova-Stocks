from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QMessageBox
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .stockdata import convert_to_brl_naturallanguage 
from .assets import styles
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class AssetsLiabilitiesChart(QMainWindow):
    def __init__(self, ticker=None):
        super().__init__()
        self.setStyleSheet(styles.light_mode)
        self.ticker = ticker
        self.period = "Trimestral"  # Default to quarterly view
        self.setup_ui()
        if ticker:
            self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Gráfico Ativos/Passivos")
        self.setMinimumSize(800, 600)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Period selector
        self.period_selector = QComboBox()
        self.period_selector.addItems(["Trimestral", "Anual"])
        self.period_selector.currentTextChanged.connect(self.on_period_changed)
        layout.addWidget(self.period_selector)

        # Create figure and canvas for the chart
        self.figure = plt.Figure(figsize=(8, 6), facecolor='#252525')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def load_data(self):
        if not self.ticker:
            return

        ticker = self.ticker + ".SA" if not self.ticker.endswith(".SA") else self.ticker
        stock = yf.Ticker(ticker)

        try:
            if self.period == "Trimestral":
                financials = stock.quarterly_balance_sheet
            else:
                financials = stock.balance_sheet

            # Extract total assets
            self.total_assets = financials.loc['Total Assets']

            # Retrieve total liabilities with compatibility checks
            if 'Total Liab' in financials.index:
                self.total_liabilities = financials.loc['Total Liab']
            elif 'Total Liabilities Net Minority Interest' in financials.index:
                self.total_liabilities = financials.loc['Total Liabilities Net Minority Interest']
            else:
                self.total_liabilities = None
                QMessageBox.warning(self, "Dados Não Disponíveis", "Dados de passivos totais não encontrados.")

            # Update the chart if both values are available
            if self.total_liabilities is not None:
                self.update_chart()
            else:
                print("Unable to update chart due to missing liabilities data.")

        except Exception as e:
            print(f"Error loading financial data: {e}")
            raise  # Raise the exception to see the full traceback

    def update_chart(self):
        # Clear the figure
        self.figure.clear()

        # Create gridspec
        gs = gridspec.GridSpec(nrows=1, ncols=1, figure=self.figure)

        # Create the bar chart
        ax = self.figure.add_subplot(gs[0])

        # Set axes background color
        ax.patch.set_facecolor('#1e1e1e')

        # Set x and y axis tick colors
        ax.tick_params(axis='x', colors='#d4d4d4')
        ax.tick_params(axis='y', colors='#d4d4d4')

        # Set spines color
        for spine in ax.spines.values():
            spine.set_color('#333')

        # Set title color
        ax.set_title('Total de Ativos vs Total de Passivos', color='#d4d4d4')

        # Get dates and values
        dates = self.total_assets.index[::-1]  # Reverse the order of dates
        assets_values = self.total_assets.values[::-1]  # Reverse the order of assets values
        liabilities_values = self.total_liabilities.values[::-1]  # Reverse the order of liabilities values

        # Humanize the dates
        def format_human_readable_date(date):
            month_names = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", 
                           "jul.", "ago.", "set.", "out.", "nov.", "dez."]
            return f"{month_names[date.month - 1]} de {date.year}"
        date_labels = [format_human_readable_date(d) for d in dates]

        # Set bar positions
        x = range(len(dates))
        width = 0.35

        # Create bars
        assets_bars = ax.bar([i for i in x], assets_values, width, label='Ativos', color='skyblue')
        liabilities_bars = ax.bar([i + width for i in x], liabilities_values, width, label='Passivos', color='lightcoral')

        # Customize the chart
        ax.set_ylabel('Valor (R$)', color='#d4d4d4')
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(date_labels, rotation=45, color='#d4d4d4')
        ax.legend(loc='upper right', facecolor='#252525', edgecolor='#333', labelcolor='#d4d4d4')

        # Add humanized value labels on top of bars
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                value_str = convert_to_brl_naturallanguage(abs(height))  # Humanize the value
                ax.annotate(value_str,
                          xy=(rect.get_x() + rect.get_width()/2, height),
                          xytext=(0, 3 if height >= 0 else -3),
                          textcoords="offset points",
                          ha='center', va='bottom' if height >= 0 else 'top',
                          color='#d4d4d4')

        autolabel(assets_bars)
        autolabel(liabilities_bars)

        # Adjust layout to prevent label cutoff
        self.figure.tight_layout()

        # Refresh the canvas
        self.canvas.draw()

    def on_period_changed(self, new_period):
        self.period = new_period
        self.load_data()

    def set_ticker(self, ticker):
        self.ticker = ticker
        self.load_data()

