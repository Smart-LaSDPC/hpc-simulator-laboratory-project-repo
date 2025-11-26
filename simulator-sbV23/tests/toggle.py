import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class ToggleButtonDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Toggle Button Example')
        self.setGeometry(100, 100, 200, 150)

        layout = QVBoxLayout()

        self.label = QLabel('Button is OFF', self)
        layout.addWidget(self.label)

        self.toggle_button = QPushButton('OFF', self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_button_state)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

    def toggle_button_state(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText('ON')
            self.label.setText('Button is ON')
        else:
            self.toggle_button.setText('OFF')
            self.label.setText('Button is OFF')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToggleButtonDemo()
    ex.show()
    sys.exit(app.exec_())
