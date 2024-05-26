from flask import Flask, request, render_template_string
import subprocess
import shutil
import threading
import os
import configparser

app = Flask(__name__)

HOSTNAME = os.environ.get('HOSTNAME', '127.0.0.1')
PORT = 5000

@app.route("/chat", methods=["POST"])
def chat():
    print("Received JSON:", request.json)
    user_message = request.json["message"]
    backup_file_path = "/tmp/script_bak.gpt"
    custom_tools_file_path = "/tmp/custom-tools.txt"


# Clone script.gpt to script_bak.gpt in /tmp
    shutil.copyfile("/app/script.gpt", backup_file_path)
    shutil.copyfile("/app/custom-tools.txt", custom_tools_file_path)

    # Read backup file
    with open(backup_file_path, "r") as f:
        template = f.read()

    config = configparser.ConfigParser()
    config.read('config.properties')

    tools = config['DEFAULT']['gptscript.tools']
    model = config['DEFAULT']['gptscript.model']

    # Replace placeholder and write back to back up file
    with open(custom_tools_file_path, "r") as f:
        custom_tools_file_path_content = f.read()

    updated_script = template.replace("<EXTRA-TOOLS>", tools).replace("<MESSAGE>", user_message)\
        .replace("<CUSTOM-TOOLS>", custom_tools_file_path_content).replace("<MODEL-NAME>", model)
    with open(backup_file_path, "w") as f:
        f.write(updated_script)

    try:
        # Execute GPT script (use the backup file)
        result = subprocess.run(
            ["/usr/local/bin/gptscript", backup_file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        gpt_response = result.stdout
    except subprocess.CalledProcessError as e:
        gpt_response = f"Error executing GPT script: {e.stderr}"  # Use stderr for more details
    except FileNotFoundError as e:
        gpt_response = f"FileNotFoundError: {e}"
    else:
        # Print backup file path only on successful execution
        print(backup_file_path)

    return {"response": gpt_response}


@app.route('/healthz')
def healthz():
    # Perform basic health checks here (e.g., check database connection)
    return 'OK', 200  # Return 200 if healthy

@app.route('/readyz')
def readyz():
    # Perform readiness checks here (e.g., ensure dependencies are initialized)
    return 'Ready', 200  # Return 200 if ready


def generate_html(message_content=None, response_content=None):
    html = f"""
    <html>
    <head>
        <style>
            #progress-bar {{
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid #3498db;
                border-radius: 50%;
                animation: spin 2s linear infinite;
                display: none; /* Hide initially */
            }}

            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <h1>Chat with K8s Poly GPT</h1>
        <form id="chat-form">
            <label for="message">Enter your message:</label><br>
            <textarea id="message" name="message" rows="5" cols="50">{message_content or ''}</textarea><br><br>
            <button type="submit">Send</button>
        </form>
        <div id="progress-bar"></div> <div id="response">{response_content or ''}</div>
        <script>
            const form = document.getElementById('chat-form');
            const progressBar = document.getElementById('progress-bar');

            form.addEventListener('submit', (event) => {{
                event.preventDefault();
                const messageInput = document.getElementById('message');
                const responseDiv = document.getElementById('response');
                const message = messageInput.value;

                // Show progress bar when submitting
                progressBar.style.display = 'block';

                fetch('/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{message: message}})
                }})
                .then(response => response.json())
                .then(data => {{
                    responseDiv.textContent = data.response;
                    messageInput.value = '';
                    // Hide progress bar after receiving response
                    progressBar.style.display = 'none';
                }})
                .catch(error => {{
                    responseDiv.textContent = 'Error: ' + error;
                    progressBar.style.display = 'none';
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html

# --- Flask Routes ---
@app.route("/ui", methods=["GET"])
def index():
    print("Request received")
    return render_template_string(generate_html())

# --- Threading and Main Execution ---

if __name__ == "__main__":
    # Start Flask app in a separate thread
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
