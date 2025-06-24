unified_iframe_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artifact Preview</title>
    <style>
        .iframe-container {{
            position: relative;
            width: 100%;
            height: 800px;
        }}
        .address-bar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 5px 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1000;
        }}
        .address-display {{
            flex: 1;
            max-width: 70%; /* Limit the address bar width to 70% */
            padding: 5px 10px;
            font-size: 14px;
            background-color: #e9ecef;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }}
        .action-buttons {{
            display: flex;
            gap: 5px;
        }}
        .action-button {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            color: #007bff;
            padding: 5px 10px;
            border-radius: 4px;
        }}
        .action-button:hover {{
            color: #0056b3;
            background-color: #e9ecef;
        }}
        .preview-iframe {{
            width: 100%;
            height: calc(100% - 40px); /* Adjust height to account for the address bar */
            border: none;
            margin-top: 40px; /* Push content below the address bar */
        }}
    </style>
</head>
<body>
    <div class="address-bar">
        <div id="address-display" class="address-display"></div>
        <div class="action-buttons">
            <button id="open-button" class="action-button" title="Open in New Tab">⚡️</button>
            <button id="refresh-button" class="action-button" title="Refresh">🔄</button>
            <button id="fullscreen-button" class="action-button" title="Fullscreen">⛶</button>
        </div>
    </div>
    <div class="iframe-container">
        <iframe id="preview-frame" class="preview-iframe" src="{src}" frameborder="0"
                sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-presentation"
                allowfullscreen></iframe>
    </div>

    <script>
        // Get references to elements
        const iframe = document.getElementById('preview-frame');
        const addressDisplay = document.getElementById('address-display');
        const openButton = document.getElementById('open-button');
        const refreshButton = document.getElementById('refresh-button');
        const fullscreenButton = document.getElementById('fullscreen-button');

        // Set the initial URL in the address bar
        addressDisplay.textContent = iframe.src;

        // Update the address bar when the iframe URL changes
        iframe.addEventListener('load', function() {{
            addressDisplay.textContent = iframe.contentWindow.location.href;
        }});

        // Open button functionality
        openButton.addEventListener('click', function() {{
            window.open(addressDisplay.textContent, '_blank');
        }});

        // Refresh button functionality
        refreshButton.addEventListener('click', function() {{
            iframe.src = iframe.src; // Reload the iframe content
        }});

        // Fullscreen button functionality
        fullscreenButton.addEventListener('click', function() {{
            if (iframe.requestFullscreen) {{
                iframe.requestFullscreen();
            }} else if (iframe.webkitRequestFullscreen) {{
                iframe.webkitRequestFullscreen();
            }} else if (iframe.msRequestFullscreen) {{
                iframe.msRequestFullscreen();
            }}
        }});
    </script>
</body>
</html>
"""
