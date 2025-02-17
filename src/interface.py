from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QComboBox, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from dotenv import load_dotenv 
import os  

from logic import CurrencyConverterLogic 


class CoinConverterInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coin Converter")
        self.setGeometry(100, 100, 960, 600)
        self.setStyleSheet("background-color: darkgray;")

        load_dotenv()  
        api_key = os.getenv("API_KEY") 

        if not api_key:
            raise ValueError("API_KEY не найден в .env файле!")

        TITLE_FONT_SIZE = 24
        LABEL_FONT_SIZE = 14
        FIELDS_SIZE = 220
        BUTTON_COLOR = "darkblue"

        # Создаем экземпляр логики
        self.converter_logic = CurrencyConverterLogic(api_key)

        # Основной контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхний блок: Название приложения (10% высоты)
        title_container = QWidget()
        title_layout = QVBoxLayout()

        title_label = QLabel("Coin Converter")
        title_label.setFont(QFont("Arial", TITLE_FONT_SIZE, QFont.Bold))
        title_label.setStyleSheet("color: darkblue;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: lightgray;")
        title_layout.addWidget(line)

        title_container.setLayout(title_layout)
        main_layout.addWidget(title_container, stretch=1)

        # Блок с выбором валют и вводом чисел (70% высоты)
        currency_container = QWidget()
        currency_layout = QVBoxLayout()

        # Добавление верхнего отступа
        currency_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Горизонтальный макет для выбора валют
        currency_fields_layout = QHBoxLayout()

        # Левая часть
        left_side = QVBoxLayout()
        left_currency_label = QLabel("From:")
        left_currency_label.setFont(QFont("Arial", LABEL_FONT_SIZE))
        left_currency_label.setStyleSheet("color: black;")
        left_side.addWidget(left_currency_label)

        self.left_currency_combo = QComboBox()
        self.left_currency_combo.addItems(["USD", "EUR", "RUB", "GBP"])
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
        right_currency_label.setStyleSheet("color: black;")
        right_side.addWidget(right_currency_label)

        self.right_currency_combo = QComboBox()
        self.right_currency_combo.addItems(["USD", "EUR", "RUB", "GBP"])
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

        # Добавление поля с валютами в вертикальный макет
        currency_layout.addLayout(currency_fields_layout)

        # Добавление нижнего отступа
        currency_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        currency_container.setLayout(currency_layout)
        main_layout.addWidget(currency_container, stretch=7)

        # Нижний блок: Кнопки (20% высоты)
        button_container = QWidget()
        button_layout = QVBoxLayout()

        # Внутренний QHBoxLayout для кнопок
        inner_button_layout = QHBoxLayout()

        # Добавляем растягиваемое пространство перед кнопкой "Calculate"
        inner_button_layout.addStretch()

        # Кнопка "Calculate" по центру
        calculate_button = QPushButton("Calculate")
        calculate_button.setStyleSheet(
            f"background-color: {BUTTON_COLOR}; color: white; font-size: 16px; padding: 10px 20px;"
        )
        calculate_button.clicked.connect(self.calculate_conversion)  # Подключаем обработчик
        inner_button_layout.addWidget(calculate_button)

        # Добавляем растягиваемое пространство после кнопки "Calculate"
        inner_button_layout.addStretch()

        # Кнопка "Exit" справа
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet(
            f"background-color: {BUTTON_COLOR}; color: white; font-size: 16px; padding: 10px 20px;"
        )
        exit_button.clicked.connect(self.close)  # Закрыть приложение
        exit_button_layout = QHBoxLayout()  # Отдельный макет для "Exit"
        exit_button_layout.addStretch()  # Отодвинуть кнопку вправо
        exit_button_layout.addWidget(exit_button)

        # Добавляем внутренние макеты в основной макет кнопок
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
            # Получаем данные из полей ввода
            base_currency = self.left_currency_combo.currentText()
            target_currency = self.right_currency_combo.currentText()
            amount = float(self.left_amount_input.text())

            # Выполняем конвертацию
            result = self.converter_logic.convert_currency(amount, base_currency, target_currency)

            if result is not None:
                self.right_amount_output.setText(f"{result:.2f}")  # Отображаем результат
            else:
                self.right_amount_output.setText("Ошибка конвертации")
        except ValueError:
            self.right_amount_output.setText("Введите корректное число")
        except Exception as e:
            self.right_amount_output.setText(f"Произошла ошибка: {str(e)}")
