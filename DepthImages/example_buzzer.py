#!/usr/bin/python

# DRV2605 reference: http://www.ti.com/lit/ds/symlink/drv2605.pdf
# MSP430TCH5E haptics library reference: http://www.ti.com/lit/ug/slau543/slau543.pdf

import time
import smbus

class haptic():
    bus = smbus.SMBus(1)# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    
    def bRead(self, register):
        return self.bus.read_byte_data(self.DRV2605_ADDR, register)

    def bWrite(self, register, value):
        return self.bus.write_byte_data(self.DRV2605_ADDR, register, value)

    def readDeviceID(self):
        statusx = self.bRead(self.DRV2605_REG_STATUS)
        print(self.DRV2605_DEVICE_ID)
        return self.DRV2605_DEVICE_ID[statusx >> 5]

    def readStatus(self):
        status = self.bRead(self.DRV2605_REG_STATUS)
        if status & 0xF:
            return "abnormal"
        else:
            return "normal"

    def __selectLibrary__(self,libraryValue):
        # Todo: this has the side effect of setting the HI_Z bit to 0 (which is the default value)
        # Read section 4.2 of http://www.ti.com/lit/ug/slau543/slau543.pdf to determine which library is the best fit for a given actuator
        self.bWrite(self.DRV2605_REG_LIBRARY, libraryValue)

    def __init__(self):
        
        self.DRV2605_ADDR = 0x5A

        self.DRV2605_REG_STATUS = 0x00
        self.DRV2605_REG_MODE = 0x01
        self.DRV2605_MODE_INTTRIG = 0x00
        self.DRV2605_MODE_EXTTRIGEDGE = 0x01
        self.DRV2605_MODE_EXTTRIGLVL = 0x02
        self.DRV2605_MODE_PWMANALOG = 0x03
        self.DRV2605_MODE_AUDIOVIBE = 0x04
        self.DRV2605_MODE_REALTIME = 0x05
        self.DRV2605_MODE_DIAGNOS = 0x06
        self.DRV2605_MODE_AUTOCAL = 0x07

        self.DRV2605_REG_RTPIN = 0x02
        self.DRV2605_REG_LIBRARY = 0x03
        self.DRV2605_REG_WAVESEQ1 = 0x04
        self.DRV2605_REG_WAVESEQ2 = 0x05
        self.DRV2605_REG_WAVESEQ3 = 0x06
        self.DRV2605_REG_WAVESEQ4 = 0x07
        self.DRV2605_REG_WAVESEQ5 = 0x08
        self.DRV2605_REG_WAVESEQ6 = 0x09
        self.DRV2605_REG_WAVESEQ7 = 0x0A
        self.DRV2605_REG_WAVESEQ8 = 0x0B

        self.DRV2605_REG_GO = 0x0C
        self.DRV2605_REG_OVERDRIVE = 0x0D
        self.DRV2605_REG_SUSTAINPOS = 0x0E
        self.DRV2605_REG_SUSTAINNEG = 0x0F
        self.DRV2605_REG_BREAK = 0x10
        self.DRV2605_REG_AUDIOCTRL = 0x11
        self.DRV2605_REG_AUDIOLVL = 0x12
        self.DRV2605_REG_AUDIOMAX = 0x13
        self.DRV2605_REG_RATEDV = 0x16
        self.DRV2605_REG_CLAMPV = 0x17
        self.DRV2605_REG_AUTOCALCOMP = 0x18
        self.DRV2605_REG_AUTOCALEMP = 0x19
        self.DRV2605_REG_FEEDBACK = 0x1A
        self.DRV2605_REG_CONTROL1 = 0x1B
        self.DRV2605_REG_CONTROL2 = 0x1C
        self.DRV2605_REG_CONTROL3 = 0x1D
        self.DRV2605_REG_CONTROL4 = 0x1E
        self.DRV2605_REG_VBAT = 0x21
        self.DRV2605_REG_LRARESON = 0x22

        self.DRV2605_DEVICE_ID = {3: "DRV2605", 4: "DRV2604", 6: "DRV2604L", 7: "DRV2605L"}

        self.DRV2605_EFF_DESC = ["Strong Click - 100%", "Strong Click - 60%", "Strong Click - 30%", "Sharp Click - 100%", "Sharp Click - 60%", "Sharp Click - 30%", "Soft Bump - 100%", "Soft Bump - 60%", "Soft Bump - 30%", "Double Click - 100%", "Double Click - 60%", "Triple Click - 100%", "Soft Fuzz - 60%", "Strong Buzz - 100%", "Empty", "Empty", "Strong Click 1 - 100%", "Strong Click 2 - 80%", "Strong Click 3 - 60%", "Sharp Click 4 - 30%", "Medium Click 1 - 100%", "Medium Click 2 - 80%", "Medium Click 3 - 60%", "Sharp Tick 1 - 100%", "Sharp Tick 2 - 80%", "Sharp Tick 3 - 60%", "Short Double Click Strong 1 - 100%", "Short Double Click Strong 2 - 80%", "Short Double Click Strong 3 - 60%", "Short Double Click Strong 4 - 30%", "Short Double Click Medium 1 - 100%", "Short Double Click Medium 2 - 80%", "Short Double Click Medium 3 - 60%", "Short Double Sharp Tick 1 - 100%", "Short Double Sharp Tick 2 - 80%", "Short Double Sharp Tick 3 - 60%", "Long Double Sharp Click Strong 1 - 100%", "Long Double Sharp Click Strong 2 - 60%", "Long Double Sharp Click Strong 3 - 30%", "Long Double Sharp Click Strong 4 - 100%", "Long Double Sharp Click Medium 1 - 100%", "Long Double Sharp Click Medium 2 - 80%", "Long Double Sharp Click Medium 3 - 60%", "Long Double Sharp Tick 1 - 100%", "Long Double Sharp Tick 2 - 80%", "Long Double Sharp Tick 3 - 60%", "Buzz 1 - 100%", "Buzz 2 - 80%", "Buzz 3 - 60%", "Buzz 4 - 40%", "Buzz 5 - 20%", "Pulsing Strong 1 - 100%", "Pulsing Strong 2- 60%", "Pulsing Medium 1 - 100%", "Pulsing Medium 2 - 60%", "Pulsing Sharp 1 - 100%", "Pulsing Sharp 2- 60%", "Transition Click 1 - 100%", "Transition Click 2 - 80%", "Transition Click 3 - 60%", "Transition Click 4 - 40%", "Transition Click 5 - 20%", "Transition Click 6 - 10%", "Transition Hum 1- 100%", "Transition Hum 2 - 80%", "Transition Hum 3 - 60%", "Transition Hum 4 - 40%", "Transition Hum 5 - 20%", "Transition Hum 6 - 10%", "Transition Ramp Down Long Smooth 1 - 100 to 0%", "Transition Ramp Down Long Smooth 2 - 100 to 0%", "Transition Ramp Down Medium Smooth 1 - 100 to 0%", "Transition Ramp Down Medium Smooth 2 - 100 to 0%", "Transition Ramp Down Short Smooth 1 - 100 to 0%", "Transition Ramp Down Short Smooth 2 - 100 to 0%", "Transition Ramp Down Long Sharp 1 - 100 to 0%", "Transition Ramp Down Long Sharp 2 - 100 to 0%",
                            "Transition Ramp Down Medium Sharp 1 - 100 to 0%", "Transition Ramp Down Medium Sharp 2 - 100 to 0%", "Transition Ramp Down Short Sharp 1 - 100 to 0%", "Transition Ramp Down Short Sharp 2 - 100 to 0%", "Transition Ramp Up Long Smooth 1 - 0 to 100%", "Transition Ramp Up Long Smooth 2 - 0 to 100%", "Transition Ramp Up Medium Smooth 1 - 0 to 100%", "Transition Ramp Up Medium Smooth 2 - 0 to 100%", "Transition Ramp Up Short Smooth 1 - 0 to 100%", "Transition Ramp Up Short Smooth 2 - 0 to 100%", "Transition Ramp Up Long Sharp 1 - 0 to 100%", "Transition Ramp Up Long Sharp 2 - 0 to 100%", "Transition Ramp Up Medium Sharp 1 - 0 to 100%", "Transition Ramp Up Medium Sharp 2 - 0 to 100%", "Transition Ramp Up Short Sharp 1 - 0 to 100%", "Transition Ramp Up Short Sharp 2 - 0 to 100%", "Transition Ramp Down Long Smooth 1 - 50 to 0%", "Transition Ramp Down Long Smooth 2 - 50 to 0%", "Transition Ramp Down Medium Smooth 1 - 50 to 0%", "Transition Ramp Down Medium Smooth 2 - 50 to 0%", "Transition Ramp Down Short Smooth 1 - 50 to 0%", "Transition Ramp Down Short Smooth 2 - 50 to 0%", "Transition Ramp Down Long Sharp 1 - 50 to 0%", "Transition Ramp Down Long Sharp 2 - 50 to 0%", "Transition Ramp Down Medium Sharp 1 - 50 to 0%", "Transition Ramp Down Medium Sharp 2 - 50 to 0%", "Transition Ramp Down Short Sharp 1 - 50 to 0%", "Transition Ramp Down Short Sharp 2 - 50 to 0%", "Transition Ramp Up Long Smooth 1 - 0 to 50%", "Transition Ramp Up Long Smooth 2 - 0 to 50%", "Transition Ramp Up Medium Smooth 1 - 0 to 50%", "Transition Ramp Up Medium Smooth 2 - 0 to 50%", "Transition Ramp Up Short Smooth 1 - 0 to 50%", "Transition Ramp Up Short Smooth 2 - 0 to 50%", "Transition Ramp Up Long Sharp 1 - 0 to 50%", "Transition Ramp Up Long Sharp 2 - 0 to 50%", "Transition Ramp Up Medium Sharp 1 - 0 to 50%", "Transition Ramp Up Medium Sharp 2 - 0 to 50%", "Transition Ramp Up Short Sharp 1 - 0 to 50%", "Transition Ramp Up Short Sharp 2 - 0 to 50%", "Long buzz for programmatic stopping - 100%, 10 seconds max", "Smooth Hum 1 (No kick or brake pulse) - 50%", "Smooth Hum 2 (No kick or brake pulse) - 40%", "Smooth Hum 3 (No kick or brake pulse) - 30%", "Smooth Hum 4 (No kick or brake pulse) - 20%", "Smooth Hum 5 (No kick or brake pulse) - 10%", "Empty", "Empty", "Empty", "Empty", "Empty"]

        #print("DRV2605 device ID: " + str(self.readDeviceID()))
        #print("DRV2605 status: " + str(self.readStatus()))

        # Clear the STANDBY bit to exit the standby state (and go to the ready state)
        self.bWrite(self.DRV2605_REG_MODE, 0x00)

        # Switch to library B
        # selectLibrary(2)

        # Turn on N_ERM_LRA
        # bWrite(DRV2605_REG_FEEDBACK, bRead(DRV2605_REG_FEEDBACK) | 0xFF)

        # Set the ERM_OPEN_LOOP bit (bit 5) of the Control3 register to 1
        # "Open-loop operation is recommended for ERM mode when using the ROM libraries"
        self.bWrite(self.DRV2605_REG_CONTROL3, self.bRead(self.DRV2605_REG_CONTROL3) | 0x20)

    def playEffect(self, effect):
        # See Appendix A of http://www.ti.com/lit/ug/slau543/slau543.pdf
        self.bWrite(self.DRV2605_REG_WAVESEQ1, effect)
        self.bWrite(self.DRV2605_REG_WAVESEQ2, 0)
        self.bWrite(self.DRV2605_REG_GO, 1)

    def playAllWaveforms(self):
        effect = 1

        while effect < 124:
            # Skip empty effects & effect "Long buzz for programmatic stopping - 100%, 10 seconds max"
            if effect not in (15, 16, 118):
                print("Effect " + str(effect) + ": " +
                      self.DRV2605_EFF_DESC[effect - 1])

                self.playEffect(effect)

                time.sleep(2)

            effect += 1

