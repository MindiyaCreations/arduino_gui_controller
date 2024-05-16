from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import sys,functools,csv,os

f = []
for (dirpath, dirnames, filenames) in os.walk("pins"):
    f.extend(filenames)
    break

board_names = []
pin_pin = []
pin_name = []
pin_type = []

for file in f:
    board_names.append(file.replace(".txt",""))
    temp_pin_pin = []
    temp_pin_name = []
    temp_pin_type = []
    with open("pins/"+file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for pins in spamreader:
            data = pins[0].split(',')
            temp_pin_pin.append(int(data[0]))
            temp_pin_name.append(data[1])
            temp_pin_type.append(int(data[2]))
    pin_pin.append(temp_pin_pin)
    pin_name.append(temp_pin_name)
    pin_type.append(temp_pin_type)

# print(pin_pin)
# print(pin_name)
# print(pin_type)

buttons = []
checkboxes = []
sliders = []
spinboxes = []
inputD = []
inputA = []

class GUI(QMainWindow):
    selected_board_id = -1
    pin_data_list = []
    pin_data_list_id = []
    pin_data_list_widget = []
    pin_name_list  = []

    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Arduino GUI Controller")
        self.columns = QVBoxLayout()

        self.selectBoard()

        components = QWidget()
        components.setLayout(self.columns)
        self.setCentralWidget(components)

        self.show()

    def selectBoard(self):
        inputRow = QVBoxLayout()
        next = QPushButton()
        self.boardCheckbox = QComboBox()
        text = QLabel()
        text.setText("Select board")
        self.boardCheckbox.addItems(board_names)
        next.setText("Next")
        inputRow.addWidget(text)
        inputRow.addWidget(self.boardCheckbox)
        inputRow.addWidget(next)
        self.boardRowWidget = QWidget()
        self.boardRowWidget.setLayout(inputRow)
        self.columns.addWidget(self.boardRowWidget)
        next.pressed.connect(self.showpins)

    def showpins(self):
        self.pin_name_list = pin_name[self.selected_board_id].copy()
        self.pin_name_list = sorted(self.pin_name_list,key=len)
        self.boardRowWidget.hide()
        self.selected_board_id = board_names.index(self.boardCheckbox.currentText())
        self.addInputWidgets()

    def update_widgets(self):
        pinID = pin_name[self.selected_board_id].index(self.pinNumbers.currentText())
        pin_data = [self.nameLineEdit.text(),pin_pin[self.selected_board_id][pinID],int(self.pinTypes.currentText()[0:1])]
        self.pin_data_list.append(pin_data)
        self.pin_data_list_id.append(pinID)
        inputRow = QHBoxLayout()
        deleteButton = QPushButton()
        label = QLabel()
        label.setText(str(pinID) + ") Pin " + pin_name[self.selected_board_id][pinID] + " named " + self.nameLineEdit.text() + " used as " + self.pinTypes.currentText()[2:])
        deleteButton.setText("Delete")
        deleteButton.pressed.connect(functools.partial(self.removeItem,pinID))
        inputRow.addWidget(label)
        inputRow.addWidget(deleteButton)
        sector = QWidget()
        sector.setLayout(inputRow)
        self.pin_data_list_widget.append(sector)
        self.pin_disp_col.addWidget(sector)
        self.pin_name_list.remove(self.pinNumbers.currentText())
        self.pin_name_list = sorted(self.pin_name_list,key=len)
        self.pinNumbers.clear()
        self.pinNumbers.addItems(self.pin_name_list)

    def removeItem(self,pinID):
        itemID = self.pin_data_list_id.index(pinID)
        self.pin_data_list[itemID] = []
        self.pin_data_list_widget[itemID].hide()
        self.pin_name_list.append(pin_name[self.selected_board_id][self.pin_data_list_id[itemID]])
        self.pin_name_list = sorted(self.pin_name_list,key=len)
        self.pinNumbers.clear()
        self.pinNumbers.addItems(self.pin_name_list)
        self.show()


    def addInputWidgets(self):
        inputRow = QHBoxLayout()
        self.nameLineEdit = QLineEdit()
        addButton = QPushButton()
        finishButton = QPushButton()
        self.pinTypes = QComboBox()
        self.pinNumbers = QComboBox()
        self.pinNumbers.addItems(self.pin_name_list)
        self.pinNumbers.currentTextChanged.connect(self.changePinTypes)
        self.changePinTypes()
        addButton.setText("Add")
        finishButton.setText("Finish")
        inputRow.addWidget(self.pinNumbers)
        inputRow.addWidget(self.nameLineEdit)
        inputRow.addWidget(self.pinTypes)
        inputRow.addWidget(addButton)
        addButton.pressed.connect(self.update_widgets)
        finishButton.pressed.connect(self.finish_func)
        rowWidget = QWidget()
        rowWidget.setLayout(inputRow)
        self.columns.addWidget(rowWidget)
        self.pin_disp_col = QVBoxLayout()
        pin_disp_col_widget = QWidget()
        pin_disp_col_widget.setLayout(self.pin_disp_col)
        self.columns.addWidget(pin_disp_col_widget)
        self.columns.addWidget(finishButton)

    def changePinTypes(self):
        if(self.pinNumbers.currentText() == ''):
            return
        pinId = pin_name[self.selected_board_id].index(self.pinNumbers.currentText())
        self.pinTypes.clear()
        items = []
        pinType = pin_type[self.selected_board_id][pinId]
        self.nameLineEdit.setText(self.pinNumbers.currentText())
        if(pinType&1!=0):
            items.append('1.Buttons')
            items.append('2.Checkboxes')
        if(pinType&2!=0):
            items.append('3.Sliders')
            items.append('4.Spinboxes')
        if(pinType&8!=0):
            items.append('6.Analog Input')
        if(pinType&4!=0):
            items.append('5.Digital Input')
        self.pinTypes.addItems(items)

    def finish_func(self):
        print(self.pin_data_list)
        with open('config.csv', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerows(self.pin_data_list)
        self.close()
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = GUI()
    sys.exit(app.exec_())