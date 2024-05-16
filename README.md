# Arduino GUI Controller

## Serial Codes

### Define input pin
```|i_#PINNUMBER#|``` <br>
PINNUMBER = {"2","14" - (analog pin A0(Uno))....} <br>

### Define output pin
```|o_#PINNUMBER#|``` <br>
PINNUMBER = {"2","14" - (analog pin A0(Uno))....}

### Set output pin value
```|s_#TYPE#_#PINNUMBER#_#VALUE#|``` <br>
PINNUMBER = {"2","14" - (analog pin A0(Uno))....}<br>
TYPE = {"A" - analog,"D" - digital}<br>
VALUE = {<br>
&emsp;if digital = {0,1},<br>
&emsp;if analog = {0...255}<br>
    }

### Get input pin value
```|g_#TYPE#_#PINNUMBER#|``` <br>
PINNUMBER = {"2","14" - (analog pin A0(Uno))....}<br>
TYPE = {"A" - analog,"D" - digital}<br>

#### Reply
```|r_#TYPE#_#PINNUMBER#_#VALUE#|``` <br>
TYPE = {"A" - analog,"D" - digital}<br>
PINNUMBER = {"2","14" - (analog pin A0(Uno))....}<br>
VALUE = {<br>
&emsp;if digital = {0,1},<br>
&emsp;if analog = {0...1023}<br>
    }

## GUI

- Spin box | Input updating speed

### Inputs
- Label | Digital Input (HIGH,LOW)
- Label | Analog Input
- Graph | Analog Input

### Outputs
- Spin box | Analog  Outputs (0,255)
- Slider | Analog  Outputs (0,255)
- Buttons | Digital Outputs
- Check box | Digital Outputs


## Pin types

1st bit - Analog Read<br>
2nd bit - Digital Read<br>
3rd bit - Analog Write<br>
4th bit - Digital Write<br>

### Control Types
1. Buttons
2. Checkboxes
3. Sliders
4. Spinboxes
5. Digital Input
6. Analog Input

### Board TXT file
```#PIN_NUMBER#,#PIN_NAME#,#TYPE#``` <br>


## To Do

- Add input displaying graph
- Make initialization UI for to setup pins