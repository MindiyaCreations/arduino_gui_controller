from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import sys,time,serial,functools,csv

buttons = []
checkboxes = []
sliders = []
spinboxes = []
inputD = []
inputA = []

with open("config.csv", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for pins in spamreader:
        data = pins[0].split(',')
        type = int(data[2])
        pin_data = [data[1],int(data[0])]
        if type == 1:
            buttons.append(pin_data)
        elif type == 2:
            checkboxes.append(pin_data)
        elif type == 3:
            sliders.append(pin_data)
        elif type == 4:
            spinboxes.append(pin_data)
        elif type == 5:
            inputD.append(pin_data)
        elif type == 6:
            inputA.append(pin_data)

arduino=serial.Serial(port='COM5', baudrate=115200, timeout=0.1)
time.sleep(3)

def send_message(val,ret=False):
    encodedMessage=val.encode()
    arduino.write(encodedMessage)
    print(val)    
    data=arduino.readlines()
    k = []
    for i in data:
        k.append(i.decode().replace('\r','').replace('\n',''))
    print (k)
    for command in k:
        if(command[0] == '|' and command[-1] == '|'):
            commands = command.replace('|','').split('_')
            if(commands[0] == 'r'):
                return int(commands[2]),int(commands[3])
    return -1,-1

class GUI(QMainWindow):
    inputDWidgets = []
    inputAWidgets = []
    inputDPinIndex = []
    inputAPinIndex = []
    checkboxWidgets = []
    spinboxWidgets = []
    sliderWidgets = []

    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Arduino GUI Controller")

        columns = QVBoxLayout()

        for widget in buttons:
            button = QPushButton()
            button.setText('Pin '+str(widget[1]))
            send_message('|o_'+str(widget[1])+'|')
            button.pressed.connect(functools.partial(self.buttonAction,widget[1],1))
            button.released.connect(functools.partial(self.buttonAction,widget[1],0))
            columns.addWidget(self.widgetTemplate(widget,button,text=widget[0]))

        for i in range(len(checkboxes)):
            checkbox = QCheckBox()
            self.checkboxWidgets.append(checkbox)
            send_message('|o_'+str(checkboxes[i][1])+'|')
            self.checkboxWidgets[-1].stateChanged.connect(functools.partial(self.checkboxAction,i))
            columns.addWidget(self.widgetTemplate(checkboxes[i],self.checkboxWidgets[-1]))

        for i in range(len(spinboxes)):
            spinbox = QSpinBox()
            self.spinboxWidgets.append(spinbox)
            send_message('|o_'+str(spinboxes[i][1])+'|')
            self.spinboxWidgets[-1].setMinimum(0)
            self.spinboxWidgets[-1].setMaximum(255)
            self.spinboxWidgets[-1].valueChanged.connect(functools.partial(self.spinboxAction,i))
            columns.addWidget(self.widgetTemplate(spinboxes[i],self.spinboxWidgets[-1]))
        
        for i in range(len(sliders)):
            slider = QSlider(Qt.Horizontal)
            self.sliderWidgets.append(slider)
            send_message('|o_'+str(sliders[i][1])+'|')
            self.sliderWidgets[-1].setMinimum(0)
            self.sliderWidgets[-1].setMaximum(255)
            self.sliderWidgets[-1].valueChanged.connect(functools.partial(self.sliderAction,i))
            columns.addWidget(self.widgetTemplate(sliders[i],self.sliderWidgets[-1]))

        for widget in inputD:
            label = QLabel()
            send_message('|i_'+str(widget[1])+'|')
            self.inputDWidgets.append(label)
            self.inputDWidgets[-1].setText(' - Value')
            self.inputDPinIndex.append(widget[1])
            columns.addWidget(self.widgetTemplate(widget,label))

        for widget in inputA:
            label = QLabel()
            send_message('|i_'+str(widget[1])+'|')
            self.inputAWidgets.append(label)
            self.inputAWidgets[-1].setText(' - Value')
            self.inputAPinIndex.append(widget[1])
            columns.addWidget(self.widgetTemplate(widget,label))

        components = QWidget()
        components.setLayout(columns)
        self.setCentralWidget(components)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showInputs)
        self.timer.start(2000)

        self.show()

    def widgetTemplate(self,widgetVal,Widget,text = ""):
        row = QHBoxLayout()
        label = QLabel()
        if(text == ""):
            label.setText(widgetVal[0] + ' {Pin '+str(widgetVal[1]) + '}')
        else:
            label.setText(text)
        row.addWidget(label)
        row.addWidget(Widget)
        rowWidget = QWidget()
        rowWidget.setLayout(row)
        return rowWidget

    def buttonAction(self,pin,pressed):
        send_message("|s_D_"+str(pin)+"_"+str(pressed)+"|")

    def checkboxAction(self,id):
        value = 1 if self.checkboxWidgets[id].isChecked() else 0
        pin = checkboxes[id][1]
        send_message("|s_D_"+str(pin)+"_"+str(value)+"|")

    def spinboxAction(self,id):
        value = self.spinboxWidgets[id].value()
        pin = spinboxes[id][1]
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def sliderAction(self,id):
        value = self.sliderWidgets[id].value()
        pin = sliders[id][1]
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def showInputs(self):
        inputDValues = [-1] * len(inputD)
        inputAValues = [-1] * len(inputA)
        for i in range(len(inputD)):
            pin,val = send_message("|g_D_"+str(inputD[i][1])+'|',ret=True)
            if(pin == -1):
                continue
            inputDValues[self.inputDPinIndex.index(pin)] = val
        for i in range(len(inputA)):
            pin,val = send_message("|g_A_"+str(inputA[i][1])+'|',ret=True)
            if(pin == -1):
                continue
            inputAValues[self.inputAPinIndex.index(pin)] = val

        for i in range(len(inputD)):
            self.inputDWidgets[i].setText(' : '+str(inputDValues[i]))
        for i in range(len(inputA)):
            self.inputAWidgets[i].setText(' : '+str(inputAValues[i]))

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = GUI()
    sys.exit(app.exec_())