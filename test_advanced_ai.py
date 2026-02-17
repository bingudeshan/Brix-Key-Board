import requests
import json

def test_advanced_ai():
    url = "http://localhost:8000/translate"
    headers = {"Content-Type": "application/json"}
    
    # Test cases matching the user's actual usage
    test_cases = [
        "mama adha gedhara yanna ona na",
        "oya kohomada adha",
        "api bath kanawa",
        "mis mama balannam",
        "dan oya mama type karana Singlish wachan therum gannwa wage",
        "mata bada gini",
        "hari mis mama balannam"
    ]
    
    print("Testing Advanced AI Understanding:\n")
    for i, test_text in enumerate(test_cases, 1):
        payload = {"text": test_text}
        print(f"{i}. Input: \"{test_text}\"")
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
            if response.status_code == 200:
                result = json.loads(response.text)
                print(f"   Output: \"{result.get('translated_text', 'ERROR')}\"")
            else:
                print(f"   ERROR: Status {response.status_code}")
        except Exception as e:
            print(f"   ERROR: {e}")
        print()

if __name__ == "__main__":
    test_advanced_ai()
