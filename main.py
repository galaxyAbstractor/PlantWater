from machine import Pin, Timer, ADC, I2C
import time
import ssd1306

waterLevel1 = 5000
waterLevel2 = 5000

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)

display = ssd1306.SSD1306_I2C(128, 64, i2c)

tim = Timer(-1)
tim2 = Timer(0)

runningPump = False

pumpAtLevel = 1400
buttonPump = Pin(5, Pin.IN)

pumpLevelMinus = Pin(18, Pin.IN)
pumpLevelPlus = Pin(33, Pin.IN)
readSensorButton = Pin(25, Pin.IN)

floatSensor = Pin(19, Pin.IN, Pin.PULL_UP)

waterSensor1 = ADC(Pin(35))
waterSensor2 = ADC(Pin(34))

waterSensor1.atten(ADC.ATTN_6DB) 
waterSensor2.atten(ADC.ATTN_6DB) 

pump = Pin(23, Pin.OUT, value = 0)

def printScreen():
    display.fill(0)

    display.text("Level 1: " + str(waterLevel1), 10, 10)
    display.text("Level 2: " + str(waterLevel2), 10, 20)
    display.text("Pump at: " + str(pumpAtLevel), 10, 30)

    if (floatSensor.value() == 0 and buttonPump.value() == 1) or runningPump:
        display.text("Pumping!", 10, 40)

    if floatSensor.value() == 1:
        display.text("No water!", 10, 50)

    display.show()

def runPump():
    global runningPump

    if (floatSensor.value() == 1):
        return None

    if (runningPump == True):
        return None
    
    runningPump = True

    printScreen()

    pump.off() # Relay inverted, this turns the relay ON
    time.sleep(2)
    pump.on()

    runningPump = False

    printScreen()

def readSensor(timer, shouldPump = True):
    global pumpAtLevel
    global waterLevel1
    global waterLevel2

    waterLevel1 = waterSensor1.read()
    waterLevel2 = waterSensor2.read()

    if (shouldPump and ((waterLevel1 > pumpAtLevel) or (waterLevel2 > pumpAtLevel))):
        runPump()
    
    printScreen()

def readButtons(timer):
    global pumpAtLevel

    if (floatSensor.value() == 0 and buttonPump.value() == 1):
        pump.off() # Relay inverted, this turns the relay ON
    else:
        pump.on()

    if (pumpLevelMinus.value() == 1 and pumpAtLevel >= 20):
        pumpAtLevel = pumpAtLevel - 20
    
    if (pumpLevelPlus.value() == 1 and pumpAtLevel <= 4075):
        pumpAtLevel = pumpAtLevel + 20

    if (readSensorButton.value() == 1):
        readSensor(timer, False)
    
    printScreen()

tim.init(period=1000 * 60, mode=Timer.PERIODIC, callback=readSensor)
tim2.init(period=300, mode=Timer.PERIODIC, callback=readButtons)

readSensor(None)
