from PyQt5.QtWidgets import ( 
    QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLineEdit, QPushButton, QLabel, 
    QComboBox, QFrame, QSpacerItem, 
    QSizePolicy, QCompleter
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from dotenv import load_dotenv 
import os  

from logic import CurrencyConverterLogic 

class CoinConverterInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coin Converter")
        self.setGeometry(100, 100, 960, 600)
        self.setStyleSheet("background-color: #1c1c1c;")
        
        load_dotenv()  
        api_key = os.getenv("API_KEY") 
        if not api_key:
            raise ValueError("API_KEY не найден в .env файле!")
        
        TITLE_FONT_SIZE = 24
        LABEL_FONT_SIZE = 14
        FIELDS_SIZE = 220
        BUTTON_COLOR = "#2f56f5"
        
        self.converter_logic = CurrencyConverterLogic(api_key)
        
        self.currencies = self.converter_logic.get_currencies()
        if not self.currencies:
            print("Не удалось загрузить список валют. Используется стандартный список.")
            self.currencies = ["USD", "EUR", "RUB", "GBP"] 
        
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        title_container = QWidget()
        title_layout = QVBoxLayout()
        title_label = QLabel("Coin Converter")
        title_label.setFont(QFont("Arial", TITLE_FONT_SIZE, QFont.Bold))
        title_label.setStyleSheet("color: #63fffc;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: lightgray;")
        title_layout.addWidget(line)
        
        title_container.setLayout(title_layout)
        main_layout.addWidget(title_container, stretch=1)
        
        currency_container = QWidget()
        currency_layout = QVBoxLayout()
        
        currency_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        currency_fields_layout = QHBoxLayout()
        
        left_side = QVBoxLayout()
        left_currency_label = QLabel("From:")
        left_currency_label.setFont(QFont("Arial", LABEL_FONT_SIZE))
        left_currency_label.setStyleSheet("color: #7891f5;")
        left_side.addWidget(left_currency_label)
        
        self.left_currency_combo = QComboBox()
        self.left_currency_combo.setEditable(True) 
        self.left_currency_combo.setInsertPolicy(QComboBox.NoInsert) 
        self.left_currency_combo.completer().setCompletionMode(QCompleter.PopupCompletion) 
        self.left_currency_combo.addItems(self.currencies) 
        self.left_currency_combo.setStyleSheet(
            "background-color: white; color: black; padding: 5px; border: 1px solid gray;"
        )
        self.left_currency_combo.setFixedWidth(FIELDS_SIZE)
        left_side.addWidget(self.left_currency_combo)
        
        self.left_amount_input = QLineEdit()
        self.left_amount_input.setPlaceholderText("Enter amount")
        self.left_amount_input.setStyleSheet(
            "background-color: white; color: black; padding: 5px; border: 1px solid gray;"
        )
        self.left_amount_input.setFixedWidth(FIELDS_SIZE)
        left_side.addWidget(self.left_amount_input)
        
        currency_fields_layout.addLayout(left_side)
        
        # Правая часть
        right_side = QVBoxLayout()
        right_currency_label = QLabel("To:")
        right_currency_label.setFont(QFont("Arial", LABEL_FONT_SIZE))
        right_currency_label.setStyleSheet("color: #7891f5;")
        right_side.addWidget(right_currency_label)
        
        self.right_currency_combo = QComboBox()
        self.right_currency_combo.setEditable(True) 
        self.right_currency_combo.setInsertPolicy(QComboBox.NoInsert) 
        self.right_currency_combo.completer().setCompletionMode(QCompleter.PopupCompletion) 
        self.right_currency_combo.addItems(self.currencies) 
        self.right_currency_combo.setStyleSheet(
            "background-color: white; color: black; padding: 5px; border: 1px solid gray;"
        )
        self.right_currency_combo.setFixedWidth(FIELDS_SIZE)
        right_side.addWidget(self.right_currency_combo)
        
        self.right_amount_output = QLineEdit()
        self.right_amount_output.setReadOnly(True)
        self.right_amount_output.setStyleSheet(
            "background-color: white; color: black; padding: 5px; border: 1px solid gray;"
        )
        self.right_amount_output.setFixedWidth(FIELDS_SIZE)
        right_side.addWidget(self.right_amount_output)
        
        currency_fields_layout.addLayout(right_side)
        
        currency_layout.addLayout(currency_fields_layout)
        
        currency_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        currency_container.setLayout(currency_layout)
        main_layout.addWidget(currency_container, stretch=7)
        
        button_container = QWidget()
        button_layout = QVBoxLayout()
        
        inner_button_layout = QHBoxLayout()
        
        inner_button_layout.addStretch()
        
        calculate_button = QPushButton("Calculate")
        calculate_button.setStyleSheet(
            f"background-color: {BUTTON_COLOR}; color: white; font-size: 16px; padding: 10px 20px;"
        )
        calculate_button.clicked.connect(self.calculate_conversion) 
        inner_button_layout.addWidget(calculate_button)
        
        inner_button_layout.addStretch()
        
        # Кнопка "Exit" справа
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet(
            f"background-color: {BUTTON_COLOR}; color: white; font-size: 16px; padding: 10px 20px;"
        )
        exit_button.clicked.connect(self.close)
        exit_button_layout = QHBoxLayout()  
        exit_button_layout.addStretch() 
        exit_button_layout.addWidget(exit_button)
        
        button_layout.addLayout(inner_button_layout)
        button_layout.addLayout(exit_button_layout)
        
        button_container.setLayout(button_layout)
        main_layout.addWidget(button_container, stretch=2)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def calculate_conversion(self):
        """
        Выполняет конвертацию валюты при нажатии кнопки "Calculate".
        """
        try:
            base_currency = self.left_currency_combo.currentText().strip().upper()
            target_currency = self.right_currency_combo.currentText().strip().upper()
            amount = float(self.left_amount_input.text())
            
            print(f"Начало конвертации: {amount} {base_currency} -> {target_currency}")
            
            result = self.converter_logic.convert_currency(amount, base_currency, target_currency)
            
            if result is not None:
                self.right_amount_output.setText(f"{result:.6f}")
                print(f"Конвертация завершена успешно: {amount} {base_currency} = {result:.6f} {target_currency}")
            else:
                self.right_amount_output.setText("Ошибка конвертации")
                print("Конвертация не удалась.")
        except ValueError:
            self.right_amount_output.setText("Введите корректное число")
            print("Ошибка: Введено некорректное число.")
        except Exception as e:
            self.right_amount_output.setText(f"Произошла ошибка: {str(e)}")
            print(f"Произошла ошибка: {e}")