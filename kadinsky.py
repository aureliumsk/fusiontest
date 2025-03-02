import requests
import json
import config
import time
from config import Config
from base64 import b64decode
# from dataclasses import dataclass

URL = "https://api-key.fusionbrain.ai"

# TODO: Create a dataclass for request
# + enum for request types ("GENERATE" is one of them at the very least) 

class Kadinsky:
    def __init__(self, config: Config):
        self.headers = {
            "X-Key": f"Key {config.api_key}",
            "X-Secret": f"Secret {config.client_secret}"
        }
        self.ids: dict[str, int] = {}
        
    def get_model_id(self, name: str = "Kandinsky") -> int:
        if name in self.ids:
            return self.ids[name]
        response = requests.get(URL + "/key/api/v1/models", headers=self.headers)
        response.raise_for_status()
        data = response.json()
        for model in data:
            if model["name"] == name:
                id = model["id"]
                self.ids[name] = id
                return id
            raise Exception("No model with this name!")

    def generate(self, prompt: str) -> str:
        """Возвращает UUID изображения."""
        model_id = self.get_model_id()

        # TODO: Unhardcode this mess
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": 1024,
            "height": 1024,
            "generateParams": {
                "query": prompt
            }
        }
        
        data = {
            "model_id": (None, model_id),
            "params": (None, json.dumps(params), "application/json")
        }

        # Is this multipart? Is this x-www-urlencoded? We don't fucking know!
        
        # "Haha, let's make a stupid quick start article our entire documentation!"
        # "People will enjoy this!"
        # - Some Sber employee probably
    
        response = requests.post(URL + "/key/api/v1/text2image/run", headers=self.headers, files=data)
        
        response.raise_for_status()
    
        uuid = response.json()["uuid"]

        return uuid

    def check_available(self, uuid: str) -> bytes | None:
        """Check if an image is available and return either None or bytes (or raise Exception)"""
        status_url = f"{URL}/key/api/v1/text2image/status/{uuid}"
        response = requests.get(status_url, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "DONE":
            image = b64decode(data["images"][0])
            return image 
            
        if data["status"] == "FAIL":
            raise Exception(
                f"Can't generate the image with given prompt! Error description: {data['errorDescription']}"
            )

        return None

if __name__ == "__main__":
    interface = Kadinsky(config.load())
    uuid = interface.generate("A fluffy cat :3")

