
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf
import pandas as pd
from .stockdata import convert_to_brl_naturallanguage
from .assets import styles
import matplotlib.gridspec as gridspec

class RevenueIncomeChart(QMainWindow):
    def __init__(self, ticker=None):
        super().__init__()
        self.setStyleSheet(styles.light_mode)
        self.ticker = ticker
        self.period = "Trimestral"  # Default to quarterly view
        self.setup_ui()
        if ticker:
            self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Gráfico Receita/Renda Líquida")
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
        self.figure = Figure(figsize=(8, 6), facecolor='#252525')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def load_data(self):
        if not self.ticker:
            return

        ticker = self.ticker + ".SA" if not self.ticker.endswith(".SA") else self.ticker
        stock = yf.Ticker(ticker)

        try:
            if self.period == "Trimestral":
                financials = stock.quarterly_financials
            else:
                financials = stock.financials

            # Extract revenue and net income
            self.revenue = financials.loc['Total Revenue']
            self.net_income = financials.loc['Net Income']
            
            # Update the chart
            self.update_chart()
            
        except Exception as e:
            print(f"Error loading financial  {e}")

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
        ax.set_title('Receita vs Renda Líquida', color='#d4d4d4')

        # Get dates and values
        dates = self.revenue.index[::-1]  # Reverse the order of dates
        revenue_values = self.revenue.values[::-1]  # Reverse the order of revenue values
        net_income_values = self.net_income.values[::-1]  # Reverse the order of net income values
        
        # Convert dates to Brazilian natural language format
        def format_brazilian_date(date):
            month_names = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", 
                           "jul.", "ago.", "set.", "out.", "nov.", "dez."]
            return f"{month_names[date.month - 1]} de {date.year}"
        date_labels = [format_brazilian_date(d) for d in dates]
        
        # Set bar positions
        x = range(len(dates))
        width = 0.35
        
        # Create bars
        revenue_bars = ax.bar([i for i in x], revenue_values, width, 
                            label='Receita', color='skyblue')
        income_bars = ax.bar([i + width for i in x], net_income_values, width,
                           label='Renda Líquida', color='lightgreen')

        # Customize the chart
        ax.set_ylabel('Valor (R$)', color='#d4d4d4')
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(date_labels, rotation=45, color='#d4d4d4')
        ax.legend(loc='upper right', facecolor='#252525', edgecolor='#333', labelcolor='#d4d4d4')

        # Add value labels on top of bars
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                value_str = convert_to_brl_naturallanguage(abs(height))
                ax.annotate(value_str,
                          xy=(rect.get_x() + rect.get_width()/2, height),
                          xytext=(0, 3 if height >= 0 else -3),
                          textcoords="offset points",
                          ha='center', va='bottom' if height >= 0 else 'top',
                          color='#d4d4d4')

        autolabel(revenue_bars)
        autolabel(income_bars)

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