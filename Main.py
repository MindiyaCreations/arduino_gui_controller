from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import sys,time,serial

buttons = [["Built in LED1",13]]
checkboxes = [["Built in LED2",13]]
sliders = [["Built in LED3",13]]
spinboxes = [["Built in LED4",13]]

arduino=serial.Serial(port='COM5', baudrate=115200, timeout=0.1)
time.sleep(2)

def send_message(val):
    encodedMessage=val.encode()
    arduino.write(encodedMessage)
    print(val)    
    data=arduino.readlines()
    k = []
    for i in data:
        k.append(i.decode())
    print (k)

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("Arduino GUI Controller")

        columns = QVBoxLayout()

        for widget in buttons:
            button = QPushButton()
            button.setText('Pin '+str(widget[1]))
            send_message('|o_'+str(widget[1])+'|')
            button.pressed.connect(lambda: self.buttonAction(widget[1],1))
            button.released.connect(lambda: self.buttonAction(widget[1],0))
            columns.addWidget(self.widgetTemplate(widget,button,text=widget[0]))

        for widget in checkboxes:
            checkbox = QCheckBox()
            send_message('|o_'+str(widget[1])+'|')
            checkbox.stateChanged.connect(lambda: self.checkboxAction(widget[1],checkbox.checkState()))
            columns.addWidget(self.widgetTemplate(widget,checkbox))

        for widget in spinboxes:
            spinbox = QSpinBox()
            send_message('|o_'+str(widget[1])+'|')
            spinbox.setMinimum(0)
            spinbox.setMaximum(255)
            spinbox.valueChanged.connect(lambda: self.spinboxAction(widget[1],spinbox.value()))
            columns.addWidget(self.widgetTemplate(widget,spinbox))
        
        for widget in sliders:
            slider = QSlider(Qt.Horizontal)
            send_message('|o_'+str(widget[1])+'|')
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.valueChanged.connect(lambda: self.sliderAction(widget[1],slider.value()))
            columns.addWidget(self.widgetTemplate(widget,slider))

        components = QWidget()
        components.setLayout(columns)
        self.setCentralWidget(components)

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

    def checkboxAction(self,pin,state):
        print(str(pin) + " checked "+str(state))
        send_message("|s_D_"+str(pin)+"_"+str(state)+"|")

    def spinboxAction(self,pin,value):
        print(str(pin) + " spinbox value "+str(value))
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")

    def sliderAction(self,pin,value):
        print(str(pin) + " slider value "+str(value))
        send_message("|s_A_"+str(pin)+"_"+str(value)+"|")


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = GUI()
    sys.exit(app.exec_())