from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any
from template_renderer import TemplateRenderer

#fastapi app instance
app = FastAPI()

# Store user_id -> list of generated poster URLs
user_templates: Dict[str, List[str]] = {}

class RenderRequest(BaseModel):
    template_version: int = Field(..., ge=1, le=3)
    user_id: str
    parameters: Dict[str, Any]

@app.post("/generate-template/")
def generate_template(body: RenderRequest):
    try:
        renderer = TemplateRenderer(template_version=body.template_version)
        response = renderer.render_template(template_data=body.parameters)
        image_url = response.get("url")

        if not image_url:
            raise HTTPException(status_code=500, detail="Template generation failed")

        # Store the URL in the list for this user_id
        if body.user_id not in user_templates:
            user_templates[body.user_id] = []

        user_templates[body.user_id].append(image_url)

        return {
            "status": "success",
            "user_id": body.user_id,
            "template_version": body.template_version,
            "generated_url": image_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-template-urls/")
def get_template_urls(user_id: str):
    if user_id in user_templates:
        return {
            "user_id": user_id,
            "generated_urls": user_templates[user_id]
        }
    else:
        raise HTTPException(status_code=404, detail="No templates found for given user ID")
