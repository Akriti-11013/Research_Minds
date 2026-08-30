#!/usr/bin/env python
"""Test script to verify the API works correctly."""

import sys
sys.path.insert(0, '/Users/akrit/Downloads/ai_project/backend')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test health endpoint
print("Testing /health endpoint...")
response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test research endpoint
print("Testing /api/research endpoint...")
request_data = {
    "topic": "Impact of Generative AI on software development",
    "depth": "quick"
}
response = client.post("/api/research", json=request_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Topic: {data['topic']}")
    print(f"Depth: {data['depth']}")
    print(f"Report sections: {list(data['report'].keys())}")
    print(f"Markdown length: {len(data['markdown'])} chars")
    print()
    print("📄 Markdown Output Sample (first 300 chars):")
    print(data['markdown'][:300])
else:
    print(f"Error: {response.text}")
