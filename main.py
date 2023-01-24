import time
from machine import I2C, Pin
from Lib import SCD30
from Lib import BME280
import xbee

i2c = I2C(1)
i2c1 = I2C(1, freq=400000)
scd30 = SCD30.SCD30(i2c, 97)
bme = BME280.BME280(i2c=i2c1)
TARGET_64BIT_ADDR = b'\x00\x00\x00\x00\x00\x00\x00\x00'
MESSAGE = ""
sleep_ms = 0
sampleRate = 60000 #milli-seconds
separator = " | "

while True:
    temp = bme.temperature
    hum = bme.humidity
    presh = bme.pressure

    # Wait for sensor data to be ready to read (by default every 2 seconds)
    while scd30.get_status_ready() != 1:
        time.sleep_ms(200)
    co2 = scd30.CO2
    MESSAGE = str(temp) + separator + str(hum) + separator + str(presh) + separator + str(co2)
    print(MESSAGE)

    try:
        xbee.transmit(TARGET_64BIT_ADDR, MESSAGE)
    except Exception as e:
        print("Transmit failure: %s" % str(e))
    sleep_ms = xbee.XBee().sleep_now(sampleRate, pin_wake=False)
