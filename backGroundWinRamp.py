import sys
from PyQt4.QtGui import *

if __name__ == "__main__":

    app = QApplication([])

    w = QWidget()
    p = QPalette()
    gradient = QLinearGradient(0, 0, 0, 400)
    gradient.setColorAt(0.0, QColor(240, 240, 240))
    gradient.setColorAt(1.0, QColor(240, 160, 160))
    p.setBrush(QPalette.Window, QBrush(gradient))
    w.setPalette(p)

    w.show()
    app.exec_()
