import requests

url = 'http://127.0.0.1:8080/predict/'
try:
    with open(r'data/05_models/test.csv', 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")  # To see the content of the response
except requests.exceptions.RequestException as e:  # This will catch any request-related errors
    print(f"Request failed: {e}")
