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

## GUI

- Spin box | Input updating speed

### Inputs
- Label | Digital Input (HIGH,LOW)
- Label | Analog Input

### Outputs
- Spin box | Analog  Outputs (0,255)
- Slider | Analog  Outputs (0,255)
- Buttons | Digital Outputs
- Check box | Digital Outputs