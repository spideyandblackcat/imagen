from flask import Flask, render_template, request, jsonify
import requests
import random
import urllib.parse
import os
import uuid  # <--- Added for Unique IDs

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')))

# --- CONFIGURATION ---
IMAGE_KEYS = [
    "sk_3vGIyQxT3L2kDkFtnZ7bhyXQL3F1LhIP", "sk_mFqLuaXFMi6AebTNkNUJ5aIRehqLry6N",
    "sk_6fquwNNLsGpGEcAyqhyXdhFytUEnM41T", "sk_E01cMc0naYu21OCACGdkRgW2XaYjtC8d",
    "sk_EgfvnDsELJDF2dhYiVV4cwS2Mo2zgtLN", "sk_lsxFXgoDW2x3hUYJt4QHQunij6fAXXfT",
    "sk_DyiGwCryiSZzW0qOc1IVhBBY1Bfgsaxo"
]
GEMINI_KEY = "AIzaSyATb6rGD5ngwFejZsrmDOG-jIIOE7FyJPg"

def get_dimensions(ratio, quality):
    if quality == "16K": base = 8192
    elif quality == "8K": base = 4096
    elif quality == "4K": base = 2048
    else: base = 1024

    if ratio == "16:9": return (int(base * 1.77), base)
    elif ratio == "9:16": return (base, int(base * 1.77))
    elif ratio == "4:3": return (int(base * 1.33), base)
    elif ratio == "3:4": return (base, int(base * 1.33))
    elif ratio == "3:2": return (int(base * 1.5), base)
    elif ratio == "2:3": return (base, int(base * 1.5))
    else: return (base, base)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        prompt = request.json.get('prompt')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": f"Rewrite this image prompt to be highly detailed but under 75 words: {prompt}"}]}]}
        res = requests.post(url, json=payload, timeout=8)
        enhanced = res.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"enhanced": enhanced})
    except:
        return jsonify({"error": "Gemini unavailable"}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt', '').strip().replace('\n', ' ')
        negative = data.get('negative', '')
        ratio = data.get('ratio', '1:1')
        quality = data.get('quality', 'HD')
        seed = data.get('seed')
        
        if not seed or str(seed) == "-1":
            seed = random.randint(0, 99999999)

        width, height = get_dimensions(ratio, quality)
        
        # Generate a Unique ID for this specific image
        image_id = str(uuid.uuid4())

        params = {
            "model": "flux",
            "width": width, "height": height,
            "seed": seed, "nologo": "true", "enhance": "true"
        }
        if negative: params["negative"] = negative

        encoded_prompt = urllib.parse.quote(prompt)
        query_string = urllib.parse.urlencode(params)
        
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{query_string}"
        
        return jsonify({
            "id": image_id,           # <--- Return UUID
            "image_url": image_url, 
            "seed": seed, 
            "dimensions": f"{width}x{height}",
            "quality": quality
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
