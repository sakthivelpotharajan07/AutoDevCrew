import requests

url = "http://localhost:8000/run_pipeline"
payload = {"requirement": "user login page"}

response = requests.post(url, json=payload)
data = response.json()

print("Status:", data.get("status"))
print("Errors:", data.get("errors"))
print("Validation Status:", data.get("context", {}).get("validation_status"))
print("Feedback:", data.get("context", {}).get("feedback"))
