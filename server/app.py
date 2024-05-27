from flask import Flask, request, render_template
import subprocess
import shutil
import threading
import os
import configparser

app = Flask(__name__, template_folder='templates')

HOSTNAME = os.environ.get('HOSTNAME', '127.0.0.1')
PORT = 5000

@app.route("/chat", methods=["POST"])
def chat():
    print("Received JSON:", request.json)

    config = configparser.ConfigParser()
    config.read('config.properties')

    instructions = config['DEFAULT']['gptscript.instructions']
    user_message = instructions+" USER: "+request.json["message"]
    backup_file_path = "/tmp/script_bak.gpt"
    custom_tools_file_path = "/tmp/custom-tools.txt"

    # Clone script.gpt to script_bak.gpt in /tmp
    shutil.copyfile("/app/script.gpt", backup_file_path)
    shutil.copyfile("/app/custom-tools.txt", custom_tools_file_path)

    # Read backup file
    with open(backup_file_path, "r") as f:
        template = f.read()


    tools = config['DEFAULT']['gptscript.tools']
    model = config['DEFAULT']['gptscript.model']

    # Replace placeholder and write back to back up file
    with open(custom_tools_file_path, "r") as f:
        custom_tools_file_path_content = f.read()

    updated_script = template.replace("<EXTRA-TOOLS>", tools).replace("<MESSAGE>", user_message) \
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
    return render_template(
        "index.html",
        message_content=message_content,
        response_content=response_content
    )

# --- Flask Routes ---
@app.route("/", methods=["GET"])
def index():
    return generate_html()

# --- Threading and Main Execution ---

if __name__ == "__main__":
    # Start Flask app in a separate thread
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()