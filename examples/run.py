"""Minimal example: run the latam-jobs-bumeran-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "countries": ["argentina", "chile"],
    "keywords": "desarrollador",
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": True,
}

run = client.actor("bibian/latam-jobs-bumeran-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('companyName') or 'confidential'} | {item.get('location')} | {item.get('country')}")
print(f"{count} results")
