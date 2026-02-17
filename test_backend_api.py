import requests
import json

def test_backend():
    url = "http://localhost:8000/translate"
    payload = {"text": "amma mn het malagedr yanawa"}
    
    print("🧪 Testing backend translation...")
    print(f"URL: {url}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Backend took too long to respond")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend is not running")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_backend()
