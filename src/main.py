from PyQt5.QtWidgets import QApplication

from interface import CoinConverterInterface

app = QApplication([])
window = CoinConverterInterface()
window.show()
app.exec_()