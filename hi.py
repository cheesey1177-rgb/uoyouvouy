
from flask import Flask, request, render_template_string
from urllib.parse import urlparse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OpenGate Web Viewer</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
        }
        header {
            padding: 18px;
            background: #1f2937;
            text-align: center;
        }
        h1 { margin: 0 0 14px; font-size: 25px; }
        form {
            display: flex;
            gap: 8px;
            max-width: 900px;
            margin: auto;
        }
        input {
            flex: 1;
            min-width: 0;
            padding: 13px;
            border-radius: 8px;
            border: 1px solid #4b5563;
            background: #111827;
            color: white;
        }
        button {
            padding: 12px 18px;
            border: 0;
            border-radius: 8px;
            background: #6366f1;
            color: white;
            cursor: pointer;
        }
        main { padding: 16px; }
        iframe {
            display: block;
            width: 100%;
            height: calc(100vh - 155px);
            min-height: 400px;
            background: white;
            border: 0;
            border-radius: 10px;
        }
        .message { color: #d1d5db; text-align: center; }
    </style>
</head>
<body>
    <header>
        <h1>OpenGate</h1>
        <form method="GET">
            <input name="url" type="text"
                   placeholder="Enter a website URL..."
                   value="{{ url }}"
                   autocomplete="url" required>
            <button type="submit">Go</button>
        </form>
    </header>
    <main>
        {% if url %}
            <iframe src="{{ url }}"
                    title="Website viewer"
                    referrerpolicy="no-referrer"></iframe>
            <p class="message">
                If the page is blank, the website may block embedding.
            </p>
        {% else %}
            <p class="message">
                Enter a website above to get started.
            </p>
        {% endif %}
    </main>
</body>
</html>
"""

@app.route("/")
def home():
    raw_url = request.args.get("url", "").strip()
    safe_url = ""

    if raw_url:
        if "://" not in raw_url:
            raw_url = "https://" + raw_url

        parsed = urlparse(raw_url)

        if (
            parsed.scheme in ("http", "https")
            and parsed.hostname
            and not parsed.username
            and not parsed.password
        ):
            safe_url = raw_url

    return render_template_string(HTML, url=safe_url)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
