<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ZImage Mobile</title>
    <style>
        :root {
            --bg: #09090b;
            --card: #18181b;
            --input: #27272a;
            --accent: #7c3aed; /* Violet */
            --accent-glow: rgba(124, 58, 237, 0.3);
            --text: #e4e4e7;
            --subtext: #a1a1aa;
            --danger: #ef4444;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* HEADER */
        header {
            padding: 15px 20px;
            background: rgba(9, 9, 11, 0.9);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { margin: 0; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; color: white; }
        h1 span { color: var(--accent); }

        /* MAIN CONTENT */
        .container {
            flex: 1;
            padding: 20px;
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }

        /* IMAGE PREVIEW AREA */
        .preview-box {
            width: 100%;
            aspect-ratio: 1/1; /* Default square placeholder */
            background: var(--card);
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            border: 1px solid #333;
            transition: all 0.3s ease;
        }
        
        .preview-box.loaded { border-color: var(--accent); aspect-ratio: auto; min-height: 300px;}
        
        #mainImage {
            width: 100%;
            height: auto;
            display: none; /* Hidden until loaded */
            object-fit: contain;
        }

        .placeholder-text { color: var(--subtext); font-size: 14px; text-align: center; padding: 20px; }
        .loader {
            width: 40px; height: 40px;
            border: 3px solid var(--input);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            display: none;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* INPUTS */
        .input-group { position: relative; margin-bottom: 15px; }
        
        textarea {
            width: 100%;
            background: var(--input);
            color: white;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 15px;
            font-size: 16px;
            resize: none;
            outline: none;
            transition: 0.2s;
        }
        textarea:focus { border-color: var(--accent); }

        .btn-enhance {
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(124, 58, 237, 0.2);
            color: #d8b4fe;
            border: none;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
        }

        /* SETTINGS ACCORDION */
        .settings-toggle {
            background: transparent;
            color: var(--subtext);
            border: 1px solid #333;
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
        }
        
        .settings-panel {
            display: none;
            background: var(--card);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
        }
        .settings-panel.open { display: block; }
        
        .control-row { display: flex; gap: 10px; margin-bottom: 12px; }
        .control-col { flex: 1; }
        
        label { display: block; font-size: 11px; color: var(--subtext); margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        select, input[type="text"] {
            width: 100%;
            background: var(--input);
            border: none;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 14px;
            appearance: none;
        }

        /* MAIN BUTTON */
        .btn-generate {
            width: 100%;
            background: var(--accent);
            color: white;
            border: none;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 15px var(--accent-glow);
            transition: transform 0.1s;
        }
        .btn-generate:active { transform: scale(0.98); }
        .btn-generate:disabled { opacity: 0.5; cursor: wait; }

        /* HISTORY SECTION */
        .history-title {
            margin-top: 40px;
            font-size: 14px;
            font-weight: bold;
            color: var(--subtext);
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
        }
        .clear-history { color: var(--danger); cursor: pointer; }

        .history-list {
            margin-top: 15px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .history-item {
            background: var(--card);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            height: 80px;
            border: 1px solid #333;
        }
        
        .history-thumb {
            width: 80px;
            height: 100%;
            object-fit: cover;
            background: #000;
        }

        .history-info {
            flex: 1;
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
            cursor: pointer;
        }

        .history-prompt {
            font-size: 13px;
            color: white;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-bottom: 4px;
        }
        
        .history-meta { font-size: 10px; color: var(--subtext); }

        .history-actions {
            display: flex;
            align-items: center;
            padding-right: 15px;
        }
        .btn-del { color: var(--subtext); font-size: 18px; padding: 10px; cursor: pointer; }
        .btn-del:hover { color: var(--danger); }

    </style>
</head>
<body>

    <header>
        <h1>ZImage <span>M</span></h1>
    </header>

    <div class="container">
        
        <!-- Preview -->
        <div class="preview-box" id="previewBox">
            <div id="placeholder" class="placeholder-text">Enter a prompt and hit Generate.<br>Long press to save image.</div>
            <div id="loader" class="loader"></div>
            <img id="mainImage" src="" alt="Generated Image">
        </div>

        <!-- Controls -->
        <div class="input-group">
            <textarea id="prompt" rows="3" placeholder="What can you imagine?"></textarea>
            <button class="btn-enhance" onclick="enhancePrompt()">✨ Enhance</button>
        </div>

        <button class="settings-toggle" onclick="toggleSettings()">
            <span>🛠 Adjustments (Ratio, Quality)</span>
            <span>▼</span>
        </button>

        <div class="settings-panel" id="settingsPanel">
            <div class="control-row">
                <div class="control-col">
                    <label>Quality</label>
                    <select id="quality">
                        <option value="HD">HD (Fast)</option>
                        <option value="4K">4K (Detailed)</option>
                        <option value="8K">8K (Slow)</option>
                    </select>
                </div>
                <div class="control-col">
                    <label>Aspect Ratio</label>
                    <select id="ratio">
                        <option value="1:1">1:1 Square</option>
                        <option value="9:16">9:16 Story</option>
                        <option value="16:9">16:9 Landscape</option>
                        <option value="4:3">4:3 Photo</option>
                    </select>
                </div>
            </div>
            <div class="control-row">
                <div class="control-col">
                    <label>Seed (-1 = Random)</label>
                    <input type="text" id="seed" value="-1">
                </div>
            </div>
            <label>Negative Prompt</label>
            <input type="text" id="negative" value="ugly, blurry, low quality, text, watermark" style="width:100%">
        </div>

        <button class="btn-generate" id="genBtn" onclick="generateImage()">GENERATE IMAGE</button>

        <!-- History -->
        <div class="history-title">
            <span>Recent History</span>
            <span class="clear-history" onclick="clearHistory()">Clear All</span>
        </div>
        <div class="history-list" id="historyList">
            <!-- Items injected by JS -->
        </div>

    </div>

    <script>
        // Load history from LocalStorage
        let historyData = JSON.parse(localStorage.getItem('zimage_history') || '[]');

        function toggleSettings() {
            document.getElementById('settingsPanel').classList.toggle('open');
        }

        async function enhancePrompt() {
            const txt = document.getElementById('prompt');
            if(!txt.value) return;
