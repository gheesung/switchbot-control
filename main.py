import network, socket, time, json
import gc

from machine import Pin, Timer, reset
from devices.switchbot import Device
from transport.mqtthandler import MQTTHandler
from hardware.mhetlive import Hardware

class mqtt2bleGateway():
    """miio2mqttGateway
    
    The gateway converts mqtt request and send to/receive from BLE devices.
    """
    def __init__(self) :
        """Initialise the Gateway
        """        
        self.deviceconfig = {}
        self.device_req_handler = {}
        self.config = None
        self.client = None
        self.config = None
        self.protocol_handler = None 
        self.devices = {}
        self.ble_activated = False
        self.ble_handle = None
        self.hardware =None

        # start the BLE
        #self.startBLE()

        print("Starting up mqtt2ble gateway....")
        

        # load the configuration
        with open('./config.json') as f:
            self.config=json.load(f)

        # setup the hardware. The hardware need to be setup before the devices
        # because some devices require the hardware to be initialised. 
        # e.g. ble
        hardware = self.config["hardware"]
        print ("Hardware :", hardware)
        hardware_config = self.config[hardware]
        self.hardware = Hardware(hardware_config)
        
        # setup the MQTT handler
        mqttconfig = self.config["mqtt"]
        self.protocol_handler = MQTTHandler(self.hardware, mqttconfig)

        # setup the devices
        devices = self.config["devices"]
        for device in devices:
            device["instance"] = Device(self.hardware, device)
            # create a hashmap of devices
            devicename = device["devicename"]
            self.device_req_handler[devicename]=device

        # pass the device handler to the transport handler
        self.protocol_handler.devicehandler = self.device_req_handler

        # pass the transport and device handler to the hardware
        self.hardware.set_transport_handler(self.protocol_handler)
        self.hardware.start_transport()
        
        for device in self.device_req_handler.items():
            #devicename = device['devicename']
            print("Added :", device)
        
        # hardware device to indicate visually (if possible) when the setup is completed.
        #self.protocol_handler.set_visual_indicator(self.hardware.blink)
        self.hardware.show_setupcomplete()
        
        #blescanner_config = self.config["blescanner"]
        #self.BLEScanner = BLEScanner(self.hardware, blescanner_config)
        #self.BLEScanner.start()

    def start(self) :
        self.hardware.start()
            
    
def main():
    gw = mqtt2bleGateway()
    gw.start()

if __name__ == "__main__":
    main()