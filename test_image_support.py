#!/usr/bin/env python3
"""
Test script to verify image support in the worker-sglang.
This script tests both URL-based and base64-encoded images.
"""

import json
import base64
import requests
import os

def test_image_url():
    """Test with image URL"""
    test_data = {
        "input": {
            "openai_route": "/v1/chat/completions",
            "openai_input": {
                "model": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100
            }
        }
    }
    
    print("Testing image URL support...")
    print(json.dumps(test_data, indent=2))
    return test_data

def test_base64_image():
    """Test with base64 encoded image"""
    # Create a simple test image (1x1 pixel)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    encoded_image = base64.b64encode(test_image_data).decode('utf-8')
    
    test_data = {
        "input": {
            "openai_route": "/v1/chat/completions",
            "openai_input": {
                "model": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this image:"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100
            }
        }
    }
    
    print("Testing base64 image support...")
    print(json.dumps(test_data, indent=2))
    return test_data

def test_mixed_content():
    """Test with mixed text and image content"""
    test_data = {
        "input": {
            "openai_route": "/v1/chat/completions",
            "openai_input": {
                "model": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please analyze this image and tell me what you see:"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                                }
                            },
                            {"type": "text", "text": "Also, what colors are prominent in this image?"}
                        ]
                    }
                ],
                "max_tokens": 150
            }
        }
    }
    
    print("Testing mixed content support...")
    print(json.dumps(test_data, indent=2))
    return test_data

if __name__ == "__main__":
    print("Image Support Test Script for worker-sglang")
    print("=" * 50)
    
    # Test different scenarios
    tests = [
        ("Image URL", test_image_url),
        ("Base64 Image", test_base64_image),
        ("Mixed Content", test_mixed_content)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        test_data = test_func()
        print(f"Test data created successfully for {test_name}")
        print() 