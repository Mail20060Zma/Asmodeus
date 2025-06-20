import requests

url = "https://openrouter.ai/api/v1/keys"
payload = { "name": "name" }
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())