from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import time

# Known MAC address of your Qingping device
DEVICE_MAC = "2C:CF:67:84:9E:9B"  # This is the Wi-Fi MAC, Bluetooth MAC may be different

def connect_to_device():
    try:
        print(f"Attempting to connect to device: {DEVICE_MAC}")
        peripheral = Peripheral(DEVICE_MAC)
        
        # Get all services
        services = peripheral.getServices()
        
        for service in services:
            print(f"Service: {service.uuid}")
            characteristics = service.getCharacteristics()
            
            for char in characteristics:
                print(f"  Characteristic: {char.uuid}")
                if char.supportsRead():
                    value = char.read()
                    print(f"    Value: {value}")
        
        peripheral.disconnect()
        return True
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return False

if __name__ == "__main__":
    success = connect_to_device()
    if success:
        print("Successfully connected and read data")
    else:
        print("Failed to connect or read data")
