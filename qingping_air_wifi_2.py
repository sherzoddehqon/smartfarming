import requests
import json
import time

# Your Qingping Air Monitor details
DEVICE_IP = "192.168.4.2"
DEVICE_MAC = "2C:CF:67:84:9E:9B"  # Hardware address from connection info
BASE_URL = f"http://{DEVICE_IP}"

def get_device_data():
    try:
        # Some API endpoints with potential MAC address parameters
        endpoints = [
            "/api/v1/devices/latest",
            f"/api/v1/device/{DEVICE_MAC}/data",  # Some APIs use MAC in the path
            "/api/v1/measurements",
            "/api/v1/status",
            "/data",
            "/state",
            "/api/status",
            "/api/data"
        ]
        
        # Common headers that might be required
        headers = {
            "User-Agent": "QingpingClient/1.0",
            "X-Device-Id": DEVICE_MAC,  # Some APIs use MAC in headers
            "Accept": "application/json"
        }
        
        for endpoint in endpoints:
            try:
                url = BASE_URL + endpoint
                print(f"Trying {url}...")
                
                # Try with and without headers
                for use_headers in [True, False]:
                    try:
                        if use_headers:
                            response = requests.get(url, headers=headers, timeout=5)
                            print(f"  With headers...")
                        else:
                            response = requests.get(url, timeout=5)
                            print(f"  Without headers...")
                            
                        if response.status_code == 200:
                            print(f"Success with endpoint: {endpoint}" + (" with headers" if use_headers else ""))
                            print(f"Response: {response.text[:200]}..." if len(response.text) > 200 else f"Response: {response.text}")
                            try:
                                data = response.json()
                                return data
                            except:
                                print("Response is not JSON format")
                                return response.text
                    except requests.exceptions.RequestException as e:
                        print(f"  Failed: {e}")
            except Exception as e:
                print(f"Failed with endpoint {endpoint}: {e}")
                continue
        
        print("Couldn't find a working API endpoint")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print(f"Attempting to connect to Qingping Air Monitor (MAC: {DEVICE_MAC}) at {DEVICE_IP}")
    while True:
        data = get_device_data()
        if data:
            print(f"Data retrieved at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(json.dumps(data, indent=2) if isinstance(data, dict) else data)
        else:
            print("Failed to retrieve data")
        
        # Wait before next attempt
        wait_time = 60  # seconds
        print(f"Waiting {wait_time} seconds before next reading...")
        time.sleep(wait_time)
