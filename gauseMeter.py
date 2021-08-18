"""
I2C Program this one reads a compass module
"""

                
from hmc5883L import HMC5582


print('```````````````')

compass = HMC5582()
compass.check()
compass.busScan()
print ('using ==>', repr(HMC5582))
compass.readTestPoint()
print(compass.readConfigA())
print(compass.readConfigB())
print(compass.readMode())
compass.configSingle()
compass.gain(1)
print('ConfigA', compass.readConfigA())
print('ConfigB', compass.readConfigB())
print('ConfigMode', compass.readMode())
print (compass.readSingle(3))
print (compass.readSingle(4))
print (compass.readSingle(5))
print (compass.readSingle(6))
print (compass.readSingle(7))
print (compass.readSingle(8))

data= compass.readData()
print ('data 1', data[0])
print ('data 2', data[1])
print ('data 3', data[2])
print ('data 4', data[3])
print ('data 5', data[4])
print ('data 6', data[5])

compass.convert(data)
print ('x magnetics', compass.xMag)
print ('y magnetics', compass.yMag)
print ('z magnetics', compass.zMag)


