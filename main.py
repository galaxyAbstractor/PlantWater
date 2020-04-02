from machine import Pin, Timer, ADC, I2C
import time
import ssd1306

waterLevel1 = 5000
waterLevel2 = 5000

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)

display = ssd1306.SSD1306_I2C(128, 64, i2c)

tim = Timer(-1)
tim2 = Timer(-1)

runningPump = False

pumpAtLevel = 2000
buttonPump = Pin(5, Pin.IN)

pumpLevelMinus = Pin(32, Pin.IN)
pumpLevelPlus = Pin(33, Pin.IN)
readSensorButton = Pin(25, Pin.IN)

floatSensor = Pin(19, Pin.IN, Pin.PULL_UP)

waterSensor1 = ADC(Pin(35))
waterSensor2 = ADC(Pin(34))

pump = Pin(23, Pin.OUT)

def printScreen(self):
    global display
    global waterLevel1
    global waterLevel2
    global pumpAtLevel
    global buttonPump
    global runningPump
    global floatSensor

    display.fill(0)

    display.text("Level 1: " + str(waterLevel1), 10, 10)
    display.text("Level 2: " + str(waterLevel2), 10, 20)
    display.text("Pump at: " + str(pumpAtLevel), 10, 30)

    if (floatSensor.value() == 0 and buttonPump.value() == 1) or runningPump:
        display.text("Pumping!", 10, 40)

    if floatSensor.value() == 1:
        display.text("No water!", 10, 50)

    display.show()

def runPump(self):
    global pump
    global runningPump
    global floatSensor

    if (floatSensor.value() == 1):
        return None

    if (runningPump == False):
        return None
    
    runningPump = True

    printScreen(self)

    pump.on()
    time.sleep(2)
    pump.off()

    runningPump = False

    printScreen(self)

def readSensor(self, shouldPump = True):
    global pumpAtLevel
    global waterLevel1
    global waterLevel2
    global waterSensor1
    global waterSensor2

    waterLevel1 = waterSensor1.read()
    waterLevel2 = waterSensor2.read()

    if (shouldPump and ((waterLevel1 < pumpAtLevel) or (waterLevel2 < pumpAtLevel))):
        runPump(self)
    
    printScreen(self)

def readButtons(self):
    global buttonPump
    global pumpLevelMinus
    global pumpLevelPlus
    global pumpAtLevel
    global pump
    global readSensorButton
    global floatSensor

    if (floatSensor.value() == 0 and buttonPump.value() == 1):
        pump.on()
    else:
        pump.off()

    if (pumpLevelMinus.value() == 1 and pumpAtLevel >= 20):
        pumpAtLevel = pumpAtLevel - 20
    
    if (pumpLevelPlus.value() == 1 and pumpAtLevel <= 4075):
        pumpAtLevel = pumpAtLevel + 20

    if (readSensorButton.value() == 1):
        readSensor(self, False)
    
    printScreen(self)

tim.init(period=1000 * 60 * 10, mode=Timer.PERIODIC, callback=readSensor)
tim2.init(period=300, mode=Timer.PERIODIC, callback=readButtons)

readSensor(None)
