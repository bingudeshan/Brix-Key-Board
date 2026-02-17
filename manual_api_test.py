import requests
import json

def test_api():
    url = "http://localhost:8000/translate"
    # Test a common phrase that should be handled locally (quota saver)
    payload = {"text": "hari"} 
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending request to {url} with '{payload['text']}'...")
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test a complex phrase that should hit Gemini
        payload2 = {"text": "mama balannam"}
        print(f"\nSending request to {url} with '{payload2['text']}'...")
        response2 = requests.post(url, data=json.dumps(payload2), headers=headers, timeout=5)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
