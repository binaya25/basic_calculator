import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.display = QLineEdit()
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.textEdited.connect(self.validate_input)
        self.display.keyPressEvent = self.handle_keypress
        grid.addWidget(self.display, 0, 0, 1, 4)

        buttons = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '=', 'C']
        row, col = 1, 0

        for button in buttons:
            if button == '=':
                btn = QPushButton(button)
                btn.clicked.connect(self.evaluate)
            elif button == 'C':
                btn = QPushButton(button)
                btn.clicked.connect(self.clear_display)
            else:
                btn = QPushButton(button)
                btn.clicked.connect(lambda checked, x=button: self.add_to_display(x))
            grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.setWindowTitle('Summercamp PyQt Calculator')
        self.show()

    def add_to_display(self, value):
        cursor_position = self.display.cursorPosition()
        self.display.setText(self.display.text()[:cursor_position] + value + self.display.text()[cursor_position:])
        self.display.setCursorPosition(cursor_position + len(value))

    def validate_input(self, text):
        if not text.replace('.', '').isdigit() and text not in ['/', '*', '-', '+']:
            self.display.setText("Error")

    def handle_keypress(self, event):
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.clear_display()
        elif event.text().isdigit() or event.text() in ['/', '*', '-', '+', '.']:
            self.add_to_display(event.text())
        else:
            super(Calculator, self).keyPressEvent(event)

    def evaluate(self):
        try:
            result = str(eval(self.display.text()))
            self.display.setText(result)
        except:
            self.display.setText("Error")

    def clear_display(self):
        self.display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec_())