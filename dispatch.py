# begin dispatch.py
import logging
import os
import sys

import requests


logging.basicConfig(level=logging.INFO)


repository = os.environ["GITHUB_REPOSITORY"]
assert repository.strip(), "GITHUB_REPOSITORY is not set"


q_repo = os.getenv('Q_REPO', "")
if not q_repo.strip():
    q_repo = repository.replace('pytest', 'homework')


url = f"https://api.github.com/repos/{q_repo}/dispatches"
logging.info(f"Dispatching to {url}")


token = os.environ['TOKEN']
image_url = os.environ['IMAGE_URL']
logging.info(f"Use image at {image_url}")

# Headers
headers = {
    "Accept": "application/vnd.github+json",  # Updated from everest-preview
    "Authorization": f"Bearer {token}",
}

assert repository.strip(), "please set repository"
assert image_url.strip(), "please set IMAGE_URL"

# Payload
payload = {
    "event_type": "test dispatch",
    "client_payload": {
        "repository": repository,
        "image_url": image_url,
    },
}

# Send the request
response = requests.post(url, headers=headers, json=payload)

assert response.ok, response.text

# Check result
if response.status_code == 204:
    logging.info("Dispatch succeeded!")
else:
    logging.error(f"Dispatch failed with status {response.status_code}: {response.text}")
    sys.exit(1)  # Fail the workflow
# end dispatch.py
