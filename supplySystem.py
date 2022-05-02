import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time
import json

BUTTON = 8

prevState = GPIO.LOW
currentState = GPIO.LOW
machineState = GPIO.LOW

# variablePWM
I_MOTOR_PIN = 10
R_MOTOR_PIN = 11
M_MOTOR_PIN = 12
FLOAT_SENSOR = 40
pod1Val, pod2Val = 0, 0
FREQ_I = 100  # Hz
FREQ_R = 100  # Hz
FREQ_M = 10   # Hz
pwmIDutyCycle, pwmRDutyCycle = 0, 0
pumpI, pumpR, pumpM = 0, 0, 0
# pressure sensors
pSense1BAR, pSense2BAR = 0, 0

# tank state -> full(1) or empty(0)
tankState = GPIO.LOW

# Machine stateData
stateData = {}

# ADC to read analog inputs -> potentiometer and pressure sensor
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# remapReset
reMapMax = 26000
reMapMin = 0

def setup():
    global pumpI, pumpR, pumpM
    GPIO.setwarnings(False)

    # Setup GPIO for shutdown pins on each VL53L0X
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(BUTTON, GPIO.IN)
    GPIO.setup(FLOAT_SENSOR, GPIO.IN)
    GPIO.setup(M_MOTOR_PIN, GPIO.OUT)
    GPIO.setup(I_MOTOR_PIN, GPIO.OUT)
    GPIO.setup(R_MOTOR_PIN, GPIO.OUT)

    pumpM = GPIO.PWM(M_MOTOR_PIN, FREQ_M)
    pumpI = GPIO.PWM(I_MOTOR_PIN, FREQ_I)
    pumpR = GPIO.PWM(R_MOTOR_PIN, FREQ_R)

def reMap(val, minVal=reMapMin, maxVal=reMapMax, maxOutputVal=100, roundoff=True):
    global reMapMax
    reMapVal = (val - minVal)*maxOutputVal/(maxVal - minVal)
    if roundoff:
        if(reMapVal>100):
            reMapMax = val
            reMapVal = 100
        return round(reMapVal)
    else:
        return round(reMapVal,2)


def systemON():
    global pod1Val, pod2Val, pSense1BAR, pSense2BAR, tankState

    # MINI TANK
    tankState = GPIO.input(FLOAT_SENSOR)
    if (tankState) == GPIO.HIGH:
        pumpM.start(0)
    else:
        pumpM.start(100)
    try: 
        val1 = adcRead(0)
        val2 = adcRead(1)
        # print(val1)
        # print(val2)
        pod1Val = reMap(val1)
        pod2Val = reMap(val2)
        # generatePWM
        pumpI.start(pod1Val)
        pumpR.start(pod2Val)
        # pressure sensor readings and calculations
        val3 = adcRead(2)
        val4 = adcRead(3)
        # print(val3)    
        # print(val4)
        pSense1BAR = reMap(val3, maxVal=24000, maxOutputVal=2, roundoff=False)
        pSense2BAR = reMap(val4, maxVal=24000,maxOutputVal=1, roundoff=False)
        # pSense1BAR = map(val1,0,1023,0,2)
        # pSense2BAR = map(val2,0,1023,0,1)
    except StopIteration:
        pass

def systemOFF():
    global pSense1BAR, pSense2BAR, pod1Val, pod2Val
    pSense1BAR = 0
    pSense2BAR = 0
    pod1Val = 0
    pod2Val = 0
    pumpI.start(0)
    pumpR.start(0)
    pumpM.start(0)

def updateState():
    global stateData
    mState , tState = '',''
    if (not machineState == True):
        mState = "ON"
        if (tankState == True):
            tState = "FULL"
        else:
            tState = "FILLING..."
    else:
        mState = "OFF"
        tState = "---"
    
    stateData = {
        'machineState': mState,
        'inputPump': pod1Val,
        'recirculationPump': pod2Val,
        'inputPressure': pSense1BAR,
        'recirculationPressure': pSense2BAR,
        'tankFull': tState
    }

def adcRead(pin):
    try : 
        return adc.read_adc(pin, gain=GAIN)
    except OSError as error : 
        flag = True
        print("cannot detect ADC connector.")
        while flag:
            try :
                machineState = GPIO.input(BUTTON)
                if machineState == GPIO.HIGH:
                    raise StopIteration
                return  adc.read_adc(pin, gain=GAIN)
            except OSError as error : 
                flag = True
            

def loop():
    global machineState
    # global currentState, prevState, machineState
    # currentState = GPIO.input(BUTTON)
    # if(currentState != prevState):
    #     if(currentState == GPIO.LOW):
    #         machineState = not machineState
    #         prevState = not prevState
    # elif(currentState == GPIO.HIGH):
    #     prevState = not prevState
    # time.sleep(0.001)
    machineState = GPIO.input(BUTTON)
    if(machineState == GPIO.HIGH):
        systemOFF()

    else:
        systemON()

    updateState()
    return json.dumps(stateData)

def main():
    setup()
    while(1):
        loop()
if __name__ == "__main__":
    main()