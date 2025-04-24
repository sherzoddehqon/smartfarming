import requests
import json
import time

# Your Qingping Air Monitor IP address
DEVICE_IP = "192.168.4.2"
BASE_URL = f"http://{DEVICE_IP}"

def get_device_data():
    try:
        # Try common API endpoints used by Qingping devices
        endpoints = [
            "/api/v1/status",
            "/data",
            "/state",
            "/api/status",
            "/api/data"
        ]
        
        for endpoint in endpoints:
            try:
                url = BASE_URL + endpoint
                print(f"Trying {url}...")
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"Success with endpoint: {endpoint}")
                    print(f"Response: {response.text}")
                    try:
                        data = response.json()
                        return data
                    except:
                        print("Response is not JSON format")
                        return response.text
            except requests.exceptions.RequestException as e:
                print(f"Failed with endpoint {endpoint}: {e}")
                continue
        
        print("Couldn't find a working API endpoint")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print(f"Attempting to connect to Qingping Air Monitor at {DEVICE_IP}")
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
