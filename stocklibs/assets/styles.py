import darkdetect

# Define colors for dark theme
_BG_PRIMARY = "#1e1e1e"  # Dark background
_BG_SECONDARY = "#252525"  # Slightly lighter background for panels
_TEXT_PRIMARY = "#d4d4d4"  # Light text
_TEXT_DISABLED = "#666"  # Disabled text
_BORDER_COLOR = "#333"  # Dark border
_HOVER_BG = "#333"  # Hover background
_ACTIVE_BG = "#444"  # Active background
_DISABLED_BG = "#2a2a2a"  # Disabled background
_SUCCESS_BG = "#28a745"  # Success color
_TEXT_SUCCESS = "#fff"  # Success text
_ERROR_BG = "#dc3545"  # Error color
_TEXT_ERROR = "#fff"  # Error text
_SEPARATOR_COLOR = "#444"  # Separator color
_DISABLED_BORDER = "#555"  # Disabled border
_HIGHLIGHT_COLOR = "#007bff" # Highlight color

light_mode = f"""
QWidget {{
    background-color: {_BG_PRIMARY};
    color: {_TEXT_PRIMARY};
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    letter-spacing: -0.3px;
    margin: 0;
    padding: 0;
}}

QToolBar {{
    background-color: {_BG_SECONDARY};
    border-bottom: 1px solid {_BORDER_COLOR};
    padding: 8px;
}}

QToolButton, QComboBox, QLineEdit {{
    margin-right: 4px;
    padding: 6px;
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
}}

QToolButton:hover, QComboBox:hover, QLineEdit:hover {{
    background-color: {_HOVER_BG};
}}

QToolButton:pressed, QComboBox:pressed, QLineEdit:pressed {{
    background-color: {_ACTIVE_BG};
}}

QToolButton:disabled, QComboBox:disabled, QLineEdit:disabled {{
    background-color: {_DISABLED_BG};
    color: {_TEXT_DISABLED};
    border: 1px solid {_DISABLED_BORDER};
}}

QComboBox, QLineEdit {{
    font-size: 12px;
}}

.editor-container {{
    width: 80%;
    margin: 40px auto 20px auto;
    background-color: {_BG_SECONDARY};
    border: 1px solid {_BORDER_COLOR};
    border-radius: 8px;
    padding: 10px;
    box-sizing: border-box;
}}

.editor {{
    width: 100%;
    min-height: 400px;
    border: none;
    padding: 10px;
    font-size: 16px;
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
    outline: none;
}}

.status-bar {{
    display: flex;
    justify-content: flex-end;
    padding: 5px;
    background-color: {_BG_SECONDARY};
    border-top: 1px solid {_BORDER_COLOR};
}}

QPushButton {{
    margin-right: 4px;
    padding: 8px 12px;
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
}}

QPushButton:hover {{
    background-color: {_HOVER_BG};
}}

QPushButton:pressed {{
    background-color: {_ACTIVE_BG};
}}

QPushButton#okButton {{
    background-color: {_SUCCESS_BG};
    color: {_TEXT_SUCCESS};
    border: none;
}}

QPushButton#cancelButton {{
    background-color: {_ERROR_BG};
    color: {_TEXT_ERROR};
    border: none;
}}

QMenu {{
    background-color: {_BG_SECONDARY};
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
}}

QMenu:disabled {{
    background-color: {_DISABLED_BG} !important;
    color: {_TEXT_DISABLED} !important;
}}

QMenu::item {{
    padding: 6px 10px;
    color: {_TEXT_PRIMARY};
}}

QMenu::item:selected {{
    background-color: {_HOVER_BG};
}}

QMenu::item:disabled {{
    color: {_TEXT_DISABLED} !important;
    background-color: {_DISABLED_BG} !important;
    border: 1px solid {_DISABLED_BORDER};
}}

QMenu::separator {{
    height: 1px;
    background-color: {_SEPARATOR_COLOR};
    margin: 4px 0;
}}

QScrollBar:vertical {{
    border: 1px solid {_BORDER_COLOR};
    background-color: {_BG_SECONDARY};
    width: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {_HOVER_BG};
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:vertical {{
    border: none;
    background: none;
    width: 0px;
    height: 0px;
}}

QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
    width: 0px;
    height: 0px;
}}

QScrollBar:horizontal {{
    border: 1px solid {_BORDER_COLOR};
    background-color: {_BG_SECONDARY};
    height: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {_HOVER_BG};
    min-width: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:horizontal {{
    border: none;
    background: none;
    width: 0px;
    height: 0px;
}}

QScrollBar::sub-line:horizontal {{
    border: none;
    background: none;
    width: 0px;
    height: 0px;
}}

QComboBox {{
    margin-right: 4px;
    padding: 6px;
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
}}

QComboBox:hover {{
    background-color: {_HOVER_BG};
}}

QComboBox:pressed {{
    background-color: {_ACTIVE_BG};
}}

QComboBox:disabled {{
    background-color: {_DISABLED_BG};
    color: {_TEXT_DISABLED};
    border: 1px solid {_DISABLED_BORDER};
}}

QComboBox QAbstractItemView {{
    background-color: {_BG_SECONDARY};
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    padding: 5px;
}}

QComboBox QAbstractItemView::item {{
    padding: 6px 10px;
    color: {_TEXT_PRIMARY};
}}

QComboBox QAbstractItemView::item:selected {{
    background-color: {_HOVER_BG};
}}

QComboBox QAbstractItemView::item:disabled {{
    color: {_TEXT_DISABLED} !important;
    background-color: {_DISABLED_BG} !important;
    border: 1px solid {_DISABLED_BORDER};
}}

QLabel {{
    font-size: 14px;
    color: {_TEXT_PRIMARY};
    margin-bottom: 5px;
}}

QLabel b {{
    color: {_HIGHLIGHT_COLOR};
}}

QDialog {{
    background-color: {_BG_PRIMARY};
    color: {_TEXT_PRIMARY};
}}

QDialog QLabel {{
    color: {_TEXT_PRIMARY};
}}

QDialog QDateEdit {{
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    padding: 6px;
}}

QDialog QDateEdit:hover {{
    background-color: {_HOVER_BG};
}}

QDialog QDateEdit:disabled {{
    background-color: {_DISABLED_BG};
    color: {_TEXT_DISABLED};
    border: 1px solid {_DISABLED_BORDER};
}}

QDialog QDialogButtonBox QPushButton {{
    margin-right: 4px;
    padding: 8px 12px;
    border: 1px solid {_BORDER_COLOR};
    border-radius: 4px;
    background-color: {_BG_SECONDARY};
    color: {_TEXT_PRIMARY};
}}

QDialog QDialogButtonBox QPushButton:hover {{
    background-color: {_HOVER_BG};
}}

QDialog QDialogButtonBox QPushButton:pressed {{
    background-color: {_ACTIVE_BG};
}}

QDialog QDialogButtonBox QPushButton#okButton {{
    background-color: {_SUCCESS_BG};
    color: {_TEXT_SUCCESS};
    border: none;
}}

QDialog QDialogButtonBox QPushButton#cancelButton {{
    background-color: {_ERROR_BG};
    color: {_TEXT_ERROR};
    border: none;
}}
"""