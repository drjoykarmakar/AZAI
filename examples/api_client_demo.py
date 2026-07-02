"""Tiny AZAI API client demo.

Run the API first:
    uvicorn azai.api.main:app --reload

Then run:
    python examples/api_client_demo.py
"""

from __future__ import annotations

import json
import urllib.request

payload = json.dumps({"smiles": "CC1=Nc2ccccc2SC1(C)C", "label": "example"}).encode()
request = urllib.request.Request(
    "http://127.0.0.1:8000/molecule/analyze",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(request, timeout=10) as response:  # noqa: S310 - local demo endpoint
    print(response.read().decode())
