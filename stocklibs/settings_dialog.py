from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QLabel, QSpinBox, QCheckBox, QComboBox, QDateEdit, QPushButton, QMessageBox
from PySide6.QtCore import QDate, Signal
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
import json
import os

class SettingsManager:
    def __init__(self):
        # Define default settings
        self._defaults = {
            "ma_period": 20,
            "ema_period": 20,
            "wma_period": 20,
            "rsi_period": 14,
            "macd_fast_period": 12,
            "macd_slow_period": 26,
            "macd_signal_period": 9,
            "stochastic_k_period": 14,
            "stochastic_d_period": 3,
            "start_date": QDate.currentDate().addYears(-1),
            "end_date": QDate.currentDate(),
            "candlestick_period": 1
        }

        # Initialize settings with defaults
        self._settings = self._defaults.copy()

        # Try to load saved settings
        self._load_settings()

    def _get_settings_path(self):
        if sys.platform == "win32":
            return os.path.join(os.getenv('APPDATA'), 'stockanalysis', 'settings.json')
        else:
            return os.path.join(os.path.expanduser('~'), '.config', 'stockanalysis', 'settings.json')

    def _load_settings(self):
        try:
            path = self._get_settings_path()
            if os.path.exists(path):
                with open(path, 'r') as f:
                    loaded_settings = json.load(f)

                    # Convert date strings to QDate objects
                    if 'start_date' in loaded_settings:
                        loaded_settings['start_date'] = QDate.fromString(loaded_settings['start_date'], "yyyy-MM-dd")
                    if 'end_date' in loaded_settings:
                        loaded_settings['end_date'] = QDate.fromString(loaded_settings['end_date'], "yyyy-MM-dd")

                    # Update settings with loaded values
                    self._settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        try:
            path = self._get_settings_path()
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Convert QDate objects to strings
            settings_to_save = self._settings.copy()
            if isinstance(settings_to_save['start_date'], QDate):
                settings_to_save['start_date'] = settings_to_save['start_date'].toString("yyyy-MM-dd")
            if isinstance(settings_to_save['end_date'], QDate):
                settings_to_save['end_date'] = settings_to_save['end_date'].toString("yyyy-MM-dd")

            with open(path, 'w') as f:
                json.dump(settings_to_save, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def reset_to_defaults(self):
        self._settings = self._defaults.copy()
        self.save_settings()

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        if key in self._settings:
            self._settings[key] = value
            self.save_settings()

    @property
    def start_date(self): return self._settings['start_date']
    @start_date.setter
    def start_date(self, value):
        if isinstance(value, str):
            value = QDate.fromString(value, "yyyy-MM-dd")
        self._settings['start_date'] = value
        self.save_settings()

    @property
    def end_date(self): return self._settings['end_date']
    @end_date.setter
    def end_date(self, value):
        if isinstance(value, str):
            value = QDate.fromString(value, "yyyy-MM-dd")
        self._settings['end_date'] = value
        self.save_settings()

    @property
    def ma_period(self): return self._settings['ma_period']
    @ma_period.setter
    def ma_period(self, value):
        self._settings['ma_period'] = value
        self.save_settings()

    @property
    def ema_period(self): return self._settings['ema_period']
    @ema_period.setter
    def ema_period(self, value):
        self._settings['ema_period'] = value
        self.save_settings()

    @property
    def wma_period(self): return self._settings['wma_period']
    @wma_period.setter
    def wma_period(self, value):
        self._settings['wma_period'] = value
        self.save_settings()

    @property
    def rsi_period(self): return self._settings['rsi_period']
    @rsi_period.setter
    def rsi_period(self, value):
        self._settings['rsi_period'] = value
        self.save_settings()

    @property
    def macd_fast_period(self): return self._settings['macd_fast_period']
    @macd_fast_period.setter
    def macd_fast_period(self, value):
        self._settings['macd_fast_period'] = value
        self.save_settings()

    @property
    def macd_slow_period(self): return self._settings['macd_slow_period']
    @macd_slow_period.setter
    def macd_slow_period(self, value):
        self._settings['macd_slow_period'] = value
        self.save_settings()

    @property
    def macd_signal_period(self): return self._settings['macd_signal_period']
    @macd_signal_period.setter
    def macd_signal_period(self, value):
        self._settings['macd_signal_period'] = value
        self.save_settings()

    @property
    def stochastic_k_period(self): return self._settings['stochastic_k_period']
    @stochastic_k_period.setter
    def stochastic_k_period(self, value):
        self._settings['stochastic_k_period'] = value
        self.save_settings()

    @property
    def stochastic_d_period(self): return self._settings['stochastic_d_period']
    @stochastic_d_period.setter
    def stochastic_d_period(self, value):
        self._settings['stochastic_d_period'] = value
        self.save_settings()

    @property
    def candlestick_period(self): return self._settings['candlestick_period']
    @candlestick_period.setter
    def candlestick_period(self, value):
        self._settings['candlestick_period'] = value
        self.save_settings()

class SettingsDialog(QDialog):
    settings_changed = Signal()

    def __init__(self, parent=None, settings_manager=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Configurações")
        self.settings_manager = settings_manager if settings_manager else SettingsManager()
        self.setup_ui()
        self.load_settings()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Create tabs
        self.indicators_tab = self.create_indicators_tab()
        self.data_tab = self.create_data_tab()

        self.tabs.addTab(self.indicators_tab, "Indicadores")
        self.tabs.addTab(self.data_tab, "Dados")

        layout.addWidget(self.tabs)

        # Buttons
        self.apply_button = QPushButton("Aplicar")
        self.cancel_button = QPushButton("Cancelar")
        self.reset_button = QPushButton("Restaurar Padrões")

        layout.addWidget(self.apply_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def create_indicators_tab(self):
        tab = QFormLayout()

        # SMA
        self.sma_period = QSpinBox()
        self.sma_period.setRange(1, 200)
        tab.addRow(QLabel("Período SMA:"), self.sma_period)

        # EMA
        self.ema_period = QSpinBox()
        self.ema_period.setRange(1, 200)
        tab.addRow(QLabel("Período EMA:"), self.ema_period)

        # WMA
        self.wma_period = QSpinBox()
        self.wma_period.setRange(1, 200)
        tab.addRow(QLabel("Período WMA:"), self.wma_period)

        # RSI
        self.rsi_period = QSpinBox()
        self.rsi_period.setRange(1, 200)
        tab.addRow(QLabel("Período RSI:"), self.rsi_period)

        # MACD
        self.macd_fast_period = QSpinBox()
        self.macd_fast_period.setRange(1, 200)
        tab.addRow(QLabel("Período MACD Rápido:"), self.macd_fast_period)

        self.macd_slow_period = QSpinBox()
        self.macd_slow_period.setRange(1, 200)
        tab.addRow(QLabel("Período MACD Lento:"), self.macd_slow_period)

        self.macd_signal_period = QSpinBox()
        self.macd_signal_period.setRange(1, 200)
        tab.addRow(QLabel("Período Sinal MACD:"), self.macd_signal_period)

        # Stochastic
        self.stochastic_k_period = QSpinBox()
        self.stochastic_k_period.setRange(1, 200)
        tab.addRow(QLabel("Período K Estocástico:"), self.stochastic_k_period)

        self.stochastic_d_period = QSpinBox()
        self.stochastic_d_period.setRange(1, 200)
        tab.addRow(QLabel("Período D Estocástico:"), self.stochastic_d_period)

        # Create a widget to hold the layout
        indicators_widget = QWidget()
        indicators_widget.setLayout(tab)
        return indicators_widget

    def create_data_tab(self):
        tab = QFormLayout()
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addYears(-1))
        tab.addRow(QLabel("Data de Início Padrão:"), self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        tab.addRow(QLabel("Data de Fim Padrão:"), self.end_date)

        self.candlestick_period = QSpinBox()
        self.candlestick_period.setRange(1, 365)  # Set appropriate range
        tab.addRow(QLabel("Período de Candlestick padrão (dias):"), self.candlestick_period)

        # Create a widget to hold the layout
        data_widget = QWidget()
        data_widget.setLayout(tab)
        return data_widget

    def load_settings(self):
        # Load settings from SettingsManager
        self.sma_period.setValue(self.settings_manager.ma_period)
        self.ema_period.setValue(self.settings_manager.ema_period)
        self.wma_period.setValue(self.settings_manager.wma_period)
        self.rsi_period.setValue(self.settings_manager.rsi_period)
        self.macd_fast_period.setValue(self.settings_manager.macd_fast_period)
        self.macd_slow_period.setValue(self.settings_manager.macd_slow_period)
        self.macd_signal_period.setValue(self.settings_manager.macd_signal_period)
        self.stochastic_k_period.setValue(self.settings_manager.stochastic_k_period)
        self.stochastic_d_period.setValue(self.settings_manager.stochastic_d_period)
        self.start_date.setDate(self.settings_manager.start_date)
        self.end_date.setDate(self.settings_manager.end_date)
        self.candlestick_period.setValue(self.settings_manager.candlestick_period)

    def save_settings(self):
        # Save settings to SettingsManager
        self.settings_manager.ma_period = self.sma_period.value()
        self.settings_manager.ema_period = self.ema_period.value()
        self.settings_manager.wma_period = self.wma_period.value()
        self.settings_manager.rsi_period = self.rsi_period.value()
        self.settings_manager.macd_fast_period = self.macd_fast_period.value()
        self.settings_manager.macd_slow_period = self.macd_slow_period.value()
        self.settings_manager.macd_signal_period = self.macd_signal_period.value()
        self.settings_manager.stochastic_k_period = self.stochastic_k_period.value()
        self.settings_manager.stochastic_d_period = self.stochastic_d_period.value()
        self.settings_manager.start_date = self.start_date.date()
        self.settings_manager.end_date = self.end_date.date()
        self.settings_manager.candlestick_period = self.candlestick_period.value()

    def reset_to_defaults(self):
        # Reset settings to default values
        self.settings_manager.reset_to_defaults()
        self.load_settings()

    def apply_changes(self):
        self.save_settings()
        self.settings_changed.emit()
        self.close()

    def connect_signals(self):
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button.clicked.connect(self.close)
        self.reset_button.clicked.connect(self.reset_to_defaults)