import socket
import subprocess
import requests
import time

# Known details of your Qingping device
DEVICE_IP = "192.168.4.2"
DEVICE_MAC = "2C:CF:67:84:9E:9B"

def arp_scan():
    """Confirm the device is online using ARP"""
    try:
        # Run ARP scan to find devices
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        
        # Check if our MAC address is in the output
        if DEVICE_MAC.lower() in result.stdout.lower():
            print(f"Device with MAC {DEVICE_MAC} found in ARP table")
            return True
        else:
            print(f"Device with MAC {DEVICE_MAC} not found in ARP table")
            return False
    except Exception as e:
        print(f"Error during ARP scan: {e}")
        return False

def connect_to_device():
    """Try to connect to the device and get data"""
    if not arp_scan():
        print("Device may not be reachable")
    
    # Try HTTP connection with common endpoints
    endpoints = ["", "/api", "/data", "/metrics", "/status", "/api/v1/data"]
    headers = {"X-Device-Id": DEVICE_MAC}  # Some APIs use MAC address for authentication
    
    for endpoint in endpoints:
        url = f"http://{DEVICE_IP}{endpoint}"
        try:
            # Try both with and without headers
            for use_headers in [True, False]:
                try:
                    if use_headers:
                        response = requests.get(url, headers=headers, timeout=3)
                    else:
                        response = requests.get(url, timeout=3)
                        
                    if response.status_code == 200:
                        print(f"Success with {url}" + (" (with headers)" if use_headers else ""))
                        return response.text
                except:
                    pass
        except Exception as e:
            print(f"Error with {url}: {e}")
    
    return None

if __name__ == "__main__":
    result = connect_to_device()
    if result:
        print(f"Data retrieved: {result[:200]}...")
    else:
        print("Failed to retrieve data")
