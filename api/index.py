from flask import Flask, render_template, request, jsonify
import requests
import random
import urllib.parse
import os

# This line is the fix: it tells Flask exactly where to find the templates folder
app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')),
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../static')))

# CONFIGURATION
IMAGE_KEYS = [
    "sk_3vGIyQxT3L2kDkFtnZ7bhyXQL3F1LhIP", "sk_mFqLuaXFMi6AebTNkNUJ5aIRehqLry6N",
    "sk_6fquwNNLsGpGEcAyqhyXdhFytUEnM41T", "sk_E01cMc0naYu21OCACGdkRgW2XaYjtC8d",
    "sk_EgfvnDsELJDF2dhYiVV4cwS2Mo2zgtLN", "sk_lsxFXgoDW2x3hUYJt4QHQunij6fAXXfT",
    "sk_DyiGwCryiSZzW0qOc1IVhBBY1Bfgsaxo"
]
GEMINI_KEY = "AIzaSyATb6rGD5ngwFejZsrmDOG-jIIOE7FyJPg"

def get_dimensions(ratio, quality):
    if quality == "16K":
        dims = {"1:1": (8192, 8192), "16:9": (15360, 8640), "9:16": (8640, 15360), "4:3": (10240, 7680)}
        return dims.get(ratio, (8192, 8192))
    if quality == "8K":
        dims = {"1:1": (4096, 4096), "16:9": (7680, 4320), "9:16": (4320, 7680)}
        return dims.get(ratio, (4096, 4096))
    if quality == "4K":
        dims = {"1:1": (2048, 2048), "16:9": (3840, 2160), "9:16": (2160, 3840)}
        return dims.get(ratio, (2048, 2048))
    if quality == "HD":
        dims = {"1:1": (1280, 1280), "16:9": (1536, 864), "9:16": (864, 1536)}
        return dims.get(ratio, (1280, 1280))
    return (1024, 1024)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        prompt = request.json.get('prompt')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": f"Rewrite for Stable Diffusion, detailed, under 100 words: {prompt}"}]}]}
        res = requests.post(url, json=payload, timeout=10)
        return jsonify({"enhanced": res.json()['candidates'][0]['content']['parts'][0]['text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt')
        negative = data.get('negative', '')
        ratio = data.get('ratio', '1:1')
        quality = data.get('quality', 'HD')
        seed = data.get('seed') if data.get('seed') != "-1" else random.randint(0, 99999999)

        width, height = get_dimensions(ratio, quality)
        
        # Build URL
        params = {
            "model": "zimage",
            "width": width, "height": height,
            "seed": seed, "nologo": "true",
            "enhance": "true", "negative": negative
        }
        
        encoded_prompt = urllib.parse.quote(prompt)
        query_string = urllib.parse.urlencode(params)
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?{query_string}"
        
        return jsonify({"image_url": image_url, "seed": seed, "dimensions": f"{width}x{height}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# VERY IMPORTANT: Vercel needs the app object to be named 'app'
# We do not need a handler function for standard Flask deployments
