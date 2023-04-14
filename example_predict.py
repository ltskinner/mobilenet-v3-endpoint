import base64
import json

import requests

api = "http://127.0.0.1:8080/predict"
image_file = "./data/pheasant.jpg"


with open(image_file, "rb") as f:
    im_bytes = f.read()

im_b64 = base64.b64encode(im_bytes).decode("utf8")

headers = {"Content-type": "application/json", "Accept": "text/plain"}

payload = json.dumps(
    {
        "image_b64": im_b64,  # required: b64 encoded image
    }
)

response = requests.post(api, data=payload, headers=headers, timeout=60)
data = response.json()
print(data)


"""
{
    'classifications': [
        [
            {
                'category_name': 'prairie chicken',
                'display_name': '',
                'index': 84,
                'score': 8.029284477233887,
            },
            ...
        ],
    ]
}
"""
