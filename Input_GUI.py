from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import sys,functools

buttons = []
checkboxes = []
sliders = []
spinboxes = []
inputD = []
inputA = []

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Arduino GUI Controller")
        self.columns = QVBoxLayout()

        self.addInputWidgets()

        components = QWidget()
        components.setLayout(self.columns)
        self.setCentralWidget(components)

        self.show()

    def update_widgets(self):
        text = ""
        for i in buttons:
            text += i[0] + " Button (Digital Input) on pin " + str(i[1]) + "\n"

    def addInputWidgets(self):
        inputRow = QHBoxLayout()
        nameLineEdit = QLineEdit()
        addButton = QPushButton()
        pinTypes = QComboBox()
        pinTypes.addItems(['1.Buttons', '2.Checkboxes', '3.Sliders', '4.Spinboxes','5.Digital Input','6.Analog Input'])
        addButton.setText("Add")
        inputRow.addWidget(nameLineEdit)
        inputRow.addWidget(pinTypes)
        inputRow.addWidget(addButton)
        rowWidget = QWidget()
        rowWidget.setLayout(inputRow)
        self.columns.addWidget(rowWidget)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = GUI()
    sys.exit(app.exec_())