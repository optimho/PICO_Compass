import struct
import machine
import binascii

class HMC5582:
    
    #Default I2C address
    addre = const(0x1e)   
    #HMC5883 Register numbers 
    configA =  const(0)
    configB =  const(1)
    mode =     const(2)
    outX_MSB = const(3)
    outX_LSB = const(4)
    outZ_MSB = const(5)
    outZ_LSB = const(6)
    outY_MSB = const(7)
    outY_LSB = const(8)
    status =   const(9)
    ident_A =  const(10)
    ident_B =  const(11)
    ident_C =  const(12)
    
    #Mode Register
    #Continuous measurement mode
    #DTRY goes high when there is new data.
    mode_continuous = const(0b00000000)
    #Single measurement mode (Default)
    mode_single = const(0b00000001)
    mode_idle = const(0b00000011)
    #high speed I2C 3400KHz
    mode_continuous_highSpeed = const(0b10000000)
    mode_single_highSpeed = const(0b10000001)
    mode_idle_highSpeed = const(0b10000011)
    
    #Gain selection
    gain_1370 =const(0b00000000) #gain 8
    gain_1090 =const(0b00100000) #gain 7
    gain_820 =const(0b01000000) #gain 6
    gain_660 =const(0b01100000) #gain 5
    gain_440 =const(0b10000000) #gain 4
    gain_390 =const(0b10100000) #gain 3
    gain_330 =const(0b11000000) #gain 2
    gain_230 =const(0b11100000) #Gain 1
    #dictionary of gains
    gainDict = {1: gain_230, 2: gain_330, 3: gain_390, 4: gain_440, 5: gain_660, 6: gain_820, 7: gain_1090, 8: gain_1370}
    
    #Status Register
    rdy = const(1)
    lock = const (1)
    
    #Identification registers
    idenA = const(0b01001000)
    idenB = const(0b00110100)
    idenC = const(0b00110011)
    
    def __init__(self, addr = addre):
        #self.bus=usmBus.SMBus(0, scl=machine.Pin(1), sda=machine.Pin(0), baudrate=100000) 
        self.bus = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0) )
        #self.bus = SMBus(0, pins=('G15','G10'), baudrate=100000)
        self.address = addr
        self.xmzg=0
        self.zmag=0
        self.ymag=0
    
    def __repr__(self):
        rep='compass class using HMC6352 at address' + self.address
        return rep
    def reset(self):
        #TODO
        print('reset')
        pass
       
    def gain(self,gainLevel):
        #Select the gain of the magnetic sensor
        #Gain level is one to 8
        if gainLevel>8: gainLevel =8
        if gainLevel<1: gainLevel =1
        func= self.gainDict.get(gainLevel)
        self.write_byte_data(self.address, configB, func)
        
    
    def configContinuous(self):
        # continuous mode reads
        # HMC5883 address, 0x1E(30)
        # Select configuration register A, 0x00(00)
        #		0x60(96)	Normal measurement configuration, Data output rate = 0.75 Hz
        self.bus.write_byte_data(self.addr, configA, 0x60)
        # HMC5883 address, 0x1E(30)
        # Select mode register, 0x02(02)
        #		0x00(00)	Continuous measurement mode
        self.bus.write_byte_data(self.addr, mode, 0x00)
        time.sleep(0.5)
        
        
    def configSingle(self):
        #single configuration read
        # HMC5883 address, 0x1E(30)
        # Select configuration register A, 0x00(00)
        #		0x60(96)	Normal measurement configuration, Data output rate = 0.75 Hz
        self.write_byte_data(self.address, configA, 0x60)
        # HMC5883 address, 0x1E(30)
        # Select mode register, 0x02(02)
        #		0x00(00)	Continuous measurement mode
        self.write_byte_data(self.address, mode, 0x00)
        time.sleep(0.5)
        
 
    def readSingle(self, register):
    # HMC5883 address, 0x1E(30)
    # Read data back from 0x03(03), 6 bytes
    # X-Axis MSB, X-Axis LSB, Z-Axis MSB, Z-Axis LSB, Y-Axis MSB, Y-Axis LSB

    #register 00 configA Read/Write
    #register 01 configB Read/Write
    #register 02 mode    Read/Write
    #register 03 outX_MSB Read
    #register 04 outX_LSB Read
    #register 05 outZ_MSB Read
    #register 06 outZ_LSB Read
    #register 07 outY_MSB Read
    #register 08 outY_LSB Read
    #register 09 status  Read
    #register 10 ident_A Read 
    #register 11 ident_B Read
    #register 12 ident_C Read
    
   # HMC5883 address, 0x1E(30)
   # Read data back from 0x03(03), 6 bytes
   # X-Axis MSB, X-Axis LSB, Z-Axis MSB, Z-Axis LSB, Y-Axis MSB, Y-Axis LSB     

        time.sleep_ms(10)
        data = self.read_byte_data(self.address, register) 
        time.sleep_ms(10)
        return data
    
    def readData(self):
    # HMC5883 address, 0x1E(30)
    # Read data back from 0x03(03), 6 bytes
    # X-Axis MSB, X-Axis LSB, Z-Axis MSB, Z-Axis LSB, Y-Axis MSB, Y-Axis LSB
 
        time.sleep_ms(10)
        data = self.read_i2c_block_data(self.address, outX_MSB, 6)
        time.sleep_ms(10)
        return data   
   
    def readContinuous(self):
        # HMC5883 address, 0x1E(30)
        # Read data back from 0x03(03), 6 bytes
        # X-Axis MSB, X-Axis LSB, Z-Axis MSB, Z-Axis LSB, Y-Axis MSB, Y-Axis LSB
        time.sleep_ms(7)
        data = self.bus.read_i2c_block_data(address, outX_MSB, 6)
        self.bus.write_byte_data(self.address, outX_MSB)
        time.sleep_ms(68)
        return data

    def convert(self, data):
        # Convert the data
        self.xMag = data[0] * 256 + data[1]
        if self.xMag > 32767:
            self.xMag -= 65536

        self.zMag = data[2] * 256 + data[3]
        if self.zMag > 32767:
            self.zMag -= 65536

        self.yMag = data[4] * 256 + data[5]
        if self.yMag > 32767 :
            self.yMag -= 65536
            
        return (self.xMag, self.yMag, self.zMag)
    
    def busScan(self):
        #check for devices on the I2C bus
        print('going to scan for devces connected to bus')
        devices=self.bus.scan()
        deviceAddresses=[]
        
        if devices:
            for d in devices:
                deviceAddresses.append(d)
                print('Slave with address found -',hex(d))                    
        return deviceAddresses 
    
    def readTestPoint(self):
        test=0
        #This is a quic check to see that you are reading values correctly
        #We read the identifiers from identifier registers and compare them what the datasheet
        #says they will be. 
        
        #print('prepare to read byte from register')
        compare = self.read_byte_data (self.address, ident_A)
        print('read {} from {}'.format((compare), (ident_A)))
        if compare == idenA:
            print('Identity A values are as expected')
            test = 0
        else:
            print('The read identity A value is not the same')
            test = 1
        
        compare = self.read_byte_data(self.address, ident_B)
        print('read {} from {}'.format((compare), (ident_B)))
        if compare == idenB:
            print('Identity B values are as expected')
            test = 0
        else:
            print('The read identity B value is not as expected')
            test = 1
        
        compare = self.read_byte_data(self.address, ident_C)
        print('read {} from {}'.format((compare), (ident_C)))
        if compare == idenC:
            print('Identity C values are as expected')
            test = 0
        else:
            print('The read identity C value is not as expected')
            test = 1
            
        return test
    
    def check(self):
        print ('Check complete')
        
    def readConfigA(self):
        data = self.read_byte_data(self.address, configA)
        return data
    
    def readConfigB(self):
        data = self.read_byte_data(self.address, configB)
        return data       
    
    def readMode(self):
        data = self.read_byte_data(self.address, mode)
        return data 
    
    def read_byte_data(self, addr, register):
        """ Read a single byte from register of device at addr
        Returns a single byte """
        return self.bus.readfrom_mem(addr, register, 1)[0]

    def read_i2c_block_data(self, addr, register, length):
        """ Read a block of length from register of device at addr
            Returns a bytes object filled with whatever was read """
        return self.bus.readfrom_mem(addr, register, length)

    def write_byte_data(self, addr, register, data):
        """ Write a single byte from buffer `data` to register of device at addr
            Returns None """
        # writeto_mem() expects something it can treat as a buffer
        if isinstance(data, int):
            data = bytes([data])
        return self.bus.writeto_mem(addr, register, data)

    def write_i2c_block_data(self, addr, register, data):
        """ Write multiple bytes of data to register of device at addr
            Returns None """
        # writeto_mem() expects something it can treat as a buffer
        if isinstance(data, int):
            data = bytes([data])
        return self.bus.writeto_mem(addr, register, data)

    # The follwing haven't been implemented, but could be.
    def read_byte(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def write_byte(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def read_word_data(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def write_word_data(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")
        


