import asyncio
import requests
import base64
import json
from engine import SGlangEngine
from utils import process_response
import runpod
import os

# Initialize the engine
engine = SGlangEngine()
engine.start_server()
engine.wait_for_server()


def get_max_concurrency(default=300):
    """
    Returns the maximum concurrency value.
    By default, it uses 50 unless the 'MAX_CONCURRENCY' environment variable is set.

    Args:
        default (int): The default concurrency value if the environment variable is not set.

    Returns:
        int: The maximum concurrency value.
    """
    return int(os.getenv("MAX_CONCURRENCY", default))


def process_image_content(content):
    """
    Process image content in messages to handle both URL and base64 encoded images.
    This function ensures that images are properly formatted for SGLang.
    """
    if isinstance(content, list):
        processed_content = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "image_url":
                    # Handle image_url format
                    image_url = item["image_url"]
                    if isinstance(image_url, dict):
                        url = image_url.get("url", "")
                        # Check if it's a base64 encoded image
                        if url.startswith("data:image"):
                            # Already in base64 format, keep as is
                            processed_content.append(item)
                        else:
                            # Regular URL, keep as is
                            processed_content.append(item)
                    else:
                        # Direct URL string
                        processed_content.append({
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        })
                elif item.get("type") == "text":
                    # Handle text content
                    processed_content.append(item)
                else:
                    # Keep other content types as is
                    processed_content.append(item)
            else:
                # If it's not a dict, treat it as text
                processed_content.append({
                    "type": "text",
                    "text": str(item)
                })
        return processed_content
    elif isinstance(content, str):
        # If content is just a string, return it as text type
        return [{"type": "text", "text": content}]
    else:
        # For any other type, convert to string
        return [{"type": "text", "text": str(content)}]


async def async_handler(job):
    """Handle the requests asynchronously."""
    job_input = job["input"]

    # Case 1: full OpenAI style payload where caller already specifies the route.
    if job_input.get("openai_route"):
        openai_route, openai_input = job_input.get("openai_route"), job_input.get(
            "openai_input"
        )

        # Process images in messages if present
        if "messages" in openai_input:
            for message in openai_input["messages"]:
                if "content" in message:
                    message["content"] = process_image_content(message["content"])

        openai_url = f"{engine.base_url}" + openai_route
        headers = {"Content-Type": "application/json"}

        response = requests.post(openai_url, headers=headers, json=openai_input)
        # Process the streamed response
        if openai_input.get("stream", False):
            for formated_chunk in process_response(response):
                yield formated_chunk
        else:
            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode("utf-8")
                    yield decoded_chunk

    # Case 2: payload looks like OpenAI chat/completions but omits the wrapper.
    elif "messages" in job_input:
        openai_url = f"{engine.base_url}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        # Process images in messages if present
        for message in job_input["messages"]:
            if "content" in message:
                message["content"] = process_image_content(message["content"])

        # Make sure model is set; fall back to default.
        if "model" not in job_input:
            job_input["model"] = engine.model or "default"

        response = requests.post(openai_url, headers=headers, json=job_input)

        if job_input.get("stream", False):
            for formated_chunk in process_response(response):
                yield formated_chunk
        else:
            for chunk in response.iter_lines():
                if chunk:
                    yield chunk.decode("utf-8")

    # Case 3: assume user meant the native /generate endpoint.
    else:
        generate_url = f"{engine.base_url}/generate"
        headers = {"Content-Type": "application/json"}
        # Directly pass `job_input` to `json`. Can we tell users the possible fields of `job_input`?
        response = requests.post(generate_url, json=job_input, headers=headers)

        if response.status_code == 200:
            yield response.json()
        else:
            yield {
                "error": f"Generate request failed with status code {response.status_code}",
                "details": response.text,
            }


runpod.serverless.start(
    {
        "handler": async_handler,
        "concurrency_modifier": get_max_concurrency,
        "return_aggregate_stream": True,
    }
)
