from micropython import const
from machine import Pin, Timer, ADC
#from hardware.button import Button
from hardware.aswitch import Pushbutton as Button
from hardware.basehardware import BaseHardware
import utime

BUTTON_A_PIN = const(2)
BATT_PIN = const(35)
LED = const(2)

class Hardware(BaseHardware):
    
    def __init__(self, config) :

        # MH-ET Live ESP32  hardware specific
        pin_a = Pin(BUTTON_A_PIN, mode=Pin.IN, pull=None)

        
        self.buttonA = Button(pin=pin_a)
        self.buttonA.press_func(self.button_A_callback, (pin_a,))  # Note how function and args are passed
        
        self.led = Pin(LED, mode=Pin.OUT)

        #configure the battery reading
        #self.vbat = ADC(Pin(BATT_PIN))
        #self.vbat.atten(ADC.ATTN_0DB)
        #self.vbat.width(ADC.WIDTH_12BIT)

        self.tranport_handler = None
        super().__init__(config)
    
    def get_bat_voltage(self):
        '''
        Override the default battery voltage reading to return the voltage 
        level of the battery
        '''
        #raw = self.vbat.read()
        #volt = raw/4095 * 3.7
        #volt = round(volt,2) 
        return 0

    def set_pin_callback(self, button, cb):
        '''
        call this to override the PIN callback function
        '''
        if button == BUTTON_A_PIN:
            self.buttonA = Button(pin=Pin(BUTTON_A_PIN, mode=Pin.IN, pull=None),  
                callback=cb, trigger=Pin.IRQ_FALLING)

    def set_transport_handler(self, transport_handler):
        self.tranport_handler = transport_handler
    
    def blink(self, totalblink=5):
        count=0
        while count < totalblink:
            self.led.value(1)
            utime.sleep(0.1)
            self.led.value(0)
            utime.sleep(0.1)
            count +=1
        
    def show_setupcomplete(self):
        self.blink(10)
        
    def button_A_callback(self, pin):
        print("Button A (%s) changed to: %r" % (pin, pin.value()))
        if pin.value() == 0 :
            # handle the request
            topic = self.tranport_handler.topicprefix + 'cmnd/studyrmfan/press'
            self.tranport_handler.publish(topic, 'on')


