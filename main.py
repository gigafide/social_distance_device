# IMPORT NECESSARY DEPENDENCIES
# THE SSD1306 DEPENDENCY IS AN EXTERNAL DEPENDENCY
from machine import Pin, I2C, Timer, PWM
from ssd1306 import SSD1306_I2C
import utime


# INITIALIZE DISPLAY
i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=40000)
oled = SSD1306_I2C(128,64,i2c)

# INITIALIZE HC-SR04 SENSOR
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# INITITALIZE BUZZER #
buzzer = PWM(Pin(13))
# set audio frequency
buzzer.freq(500)
# set audio volume from 0 to 1000
buzzer.duty_u16(1000)

# INITIALIZE VARIABLES #
target_distance = 2 #meters

# CREATE A FUNCTION TO CHECK FOR DISTANCE #
def sensor():
	# turn off trigger, and wait for 2 microseconds
    trigger.low()
    utime.sleep_us(2)
	# turn on trigger, and wait for 5 microseconds
    trigger.high()
    utime.sleep_us(5)
	# turn off trigger
    trigger.low()
	# count time it takes to receive an echo
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
	#convert the time to measurements
    #measurement in cm
    #distance = (timepassed * 0.0343) / 2
    #measurement in m
    distance = (timepassed * 0.000343) / 2
    #measurement in feet
	  #distance = (timepassed * 1125) / 2
    return distance

# ADD MAIN LOOP TO 'TRY' STATEMENT IN CASE OF ERRORS #
try:
	# CREATE MAIN LOOP #
    while True:
		# WIPE DISPLAY SCREEN #
        oled.fill(0)
		# GET RESULT FROM SENSOR #
        result = sensor()
        if result < target_distance:
            buzzer.duty_u16(1000)
            oled.text("TOO CLOSE!",0,20)
        else:
            buzzer.duty_u16(0)
        oled.text("Distance:",0,0)
        oled.text(str(result) + " m",0,10)
        oled.text("",0,20)
        oled.show()
        utime.sleep(1)            
except KeyboardInterrupt:
    pass
