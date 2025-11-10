import requests

url = "http://127.0.0.1:5000/predict"

# Sample user input
data = {
    "skills": "Python, Machine Learning, SQL",
    "interests": "Data Science"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
