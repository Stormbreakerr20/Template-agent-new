import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class TemplateRenderer:
    """Utility class to interact with the Templated.io API for poster generation"""
    
    def __init__(self, template_version: int = 0):
        self.template_version = template_version
        self.api_key = os.getenv('TEMPLATED_API_KEY')  # for versions 1,2,3
        self.api_key2 = os.getenv('TEMPLATED_API_KEY2')  # for version 0

        # Use different template IDs
        self.template_id0 = os.getenv('TEMPLATED_TEMPLATE_ID0')
        self.template_id1 = os.getenv('TEMPLATED_TEMPLATE_ID1')
        self.template_id2 = os.getenv('TEMPLATED_TEMPLATE_ID2')
        self.template_id3 = os.getenv('TEMPLATED_TEMPLATE_ID3')

        self.url = 'https://api.templated.io/v1/render'

    def get_api_key(self) -> str:
        """Return appropriate API key depending on template version"""
        return self.api_key2 if self.template_version == 0 else self.api_key

    def get_template_id(self) -> str:
        """Get the template ID for the current template version"""
        if self.template_version == 0:
            return self.template_id0
        elif self.template_version == 1:
            return self.template_id1
        elif self.template_version == 2:
            return self.template_id2
        elif self.template_version == 3:
            return self.template_id3
        else:
            return self.template_id0  # default to version 0

    def get_template_structure(self) -> Dict[str, Any]:
        """Get the expected structure of the template based on version"""
        if self.template_version == 0:
            return {
                "image_url1": {"image_url": ""},
                "image_url2": {"image_url": ""},
                "image_url3": {"image_url": ""},
                "image_url4": {"image_url": ""},
                "text1": {"text": "", "color": "#000000"},
                "text2": {"text": "", "color": "#000000"},
                "text3": {"text": "", "color": "#000000"},
                "text4": {"text": "", "color": "#000000"}
            }
        elif self.template_version == 1:
            return {
                'image-1': {'image_url': ''},
                'bg-website': {},
                'website': {'text': 'www.house4you.com', 'color': '#FFFFFF'},
                'shape-bg': {},
                'modern': {'text': 'MODERN', 'color': 'rgb(171, 102, 49)'},
                'home': {'text': 'HOME', 'color': 'rgb(59, 59, 59)'},
                'for sale': {'text': 'FOR SALE', 'color': 'rgb(59, 59, 59)'},
                'start from': {'text': 'START FROM', 'color': 'rgb(59, 59, 59)'},
                'price': {'text': '$0', 'color': 'rgb(59, 59, 59)'},
                'button-cta': {'text': 'BUY NOW', 'color': 'rgb(228, 228, 222)'}
            }
        elif self.template_version == 2:
            return {
                'image-top': {'image_url': ''},
                'photo-1': {'image_url': ''},
                'photo-2': {'image_url': ''},
                'photo-3': {'image_url': ''},
                'shape-1': {},
                'title-1': {'text': 'THE BEST HOME', 'color': 'rgb(239, 233, 226)'},
                'title-2': {'text': 'FOR SALE', 'color': 'rgb(239, 233, 226)'},
                'button-cta': {'text': 'I WANT', 'color': 'rgb(255, 255, 255)'},
                'info': {'text': 'For more info, contact us', 'color': 'rgb(126, 103, 76)'},
                'website': {'text': 'www.housesforyou.com', 'color': 'rgb(0, 0, 0)'}
            }
        else:
            return self.get_template_structure(0)

    def set_template_version(self, version: int) -> None:
        self.template_version = version if version in [0, 1, 2, 3] else 0

    def render_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        template_id = self.get_template_id()
        api_key = self.get_api_key()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        if not api_key or not template_id:
            raise ValueError("Missing API key or template ID. Please check your .env file.")

        print(f"Rendering template version: {self.template_version}")
        print(f"Using template ID: {template_id}")

        if "your_templated_api_key_here" in api_key or "your_template_id_here" in template_id:
            print("Mocking response in development mode.")
            return {
                "url": "https://example.com/poster-preview.jpg",
                "status": "success",
                "template_id": template_id,
                "template_version": self.template_version,
                "mock_generation": True
            }

        data = {
            'template': template_id,
            'layers': template_data
        }

        try:
            response = requests.post(self.url, json=data, headers=headers)
            print(f"Templated.io API status: {response.status_code}")

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Templated.io error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error rendering template: {str(e)}")
            raise
