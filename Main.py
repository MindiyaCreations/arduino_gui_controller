from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import sys,time,serial,functools

buttons = [["A",2],["B",3],["C",4]]
checkboxes = [["D",5],["E",6],["F",7]]
sliders = [["G",8],["H",9],["I",10]]
spinboxes = [["J",11],["K",12],["L",13]]
inputD = [["M",14],["N",15],["O",16]]
inputA = [["P",17],["Q",18],["R",19]]

arduino=serial.Serial(port='COM5', baudrate=115200, timeout=0.1)
time.sleep(3)

def send_message(val,ret=False):
    encodedMessage=val.encode()
    arduino.write(encodedMessage)
    print(val)    
    data=arduino.readlines()
    k = []
    for i in data:
        k.append(i.decode())
    print (k)
    if(ret):
        if(len(k) == 0):
            return -1
        if(len(k) == 1):
            return k[0]
        return k[-1]

class GUI(QMainWindow):
    inputDWidgets = []
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
        if(pressed):    
            print(str(pin) + " Pressed")
        else:    
            print(str(pin) + " Released")

    def checkboxAction(self,id):
        value = self.checkboxWidgets[id].isChecked()
        pin = checkboxes[id][1]
        print(str(pin) + " spinbox value "+str(value))
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def spinboxAction(self,id):
        value = self.spinboxWidgets[id].value()
        pin = spinboxes[id][1]
        print(str(pin) + " spinbox value "+str(value))
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def sliderAction(self,id):
        value = self.sliderWidgets[id].value()
        pin = sliders[id][1]
        print(str(pin) + " slider value "+str(value))
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def showInputs(self):
        for i in range(len(inputD)):
            val = send_message("|g_D_"+str(inputD[i][1])+']',ret=True)
            self.inputDWidgets[i].setText(' : '+str(val))

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = GUI()
    sys.exit(app.exec_())