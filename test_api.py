import requests
import json

def test_signup():
    url = "http://127.0.0.1:8000/api/v1/auth/signup"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'email': 'test@terranova.ai',
        'password': 'test123',
        'full_name': 'Test User'
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_signup()
