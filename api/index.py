from flask import Flask, render_template, request, jsonify
import requests
import random
import urllib.parse
import os
import uuid

app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')))

# --- CONFIGURATION ---
GEMINI_KEY = "AIzaSyATb6rGD5ngwFejZsrmDOG-jIIOE7FyJPg"

def get_dimensions(ratio, quality):
    # Base sizes
    if quality == "16K": base = 8192
    elif quality == "8K": base = 4096
    elif quality == "4K": base = 2048
    else: base = 1024 # HD

    # Aspect Ratios
    if ratio == "16:9": return (int(base * 1.777), base)
    elif ratio == "9:16": return (base, int(base * 1.777))
    elif ratio == "4:3": return (int(base * 1.333), base)
    elif ratio == "3:4": return (base, int(base * 1.333))
    elif ratio == "3:2": return (int(base * 1.5), base)
    elif ratio == "2:3": return (base, int(base * 1.5))
    else: return (base, base) # 1:1

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
        raw_prompt = data.get('prompt', '')
        
        # --- EXPERT URL HANDLING START ---
        # 1. Sanitize: Remove newlines, tabs, and collapse multiple spaces into one.
        clean_prompt = " ".join(raw_prompt.split())
        
        # 2. Encode: Turn "A Red Cat" into "A%20Red%20Cat". NO SPACES allowed in URL.
        encoded_prompt = urllib.parse.quote(clean_prompt)
        # --- EXPERT URL HANDLING END ---

        negative = data.get('negative', '')
        ratio = data.get('ratio', '1:1')
        quality = data.get('quality', 'HD')
        seed = data.get('seed')
        
        if not seed or str(seed) == "-1":
            seed = random.randint(0, 99999999)

        width, height = get_dimensions(ratio, quality)
        image_id = str(uuid.uuid4())

        params = {
            "model": "zimage",  # <--- STRICTLY ZIMAGE
            "width": width, 
            "height": height,
            "seed": seed, 
            "nologo": "true", 
            "enhance": "true"
        }
        if negative: 
            params["negative"] = negative

        # Construct Query String
        query_string = urllib.parse.urlencode(params)
        
        # Final URL (Guaranteed no spaces)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{query_string}"
        
        return jsonify({
            "id": image_id,
            "image_url": image_url, 
            "seed": seed, 
            "dimensions": f"{width}x{height}",
            "quality": quality
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
