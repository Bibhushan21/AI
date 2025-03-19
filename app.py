from flask import Flask, render_template, request, jsonify
import requests
import PyPDF2
import os

# Initialize Flask app
MultiverzAI = Flask(__name__)

# ✅ Correct Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

# ✅ Function to extract system prompt from a PDF
def extract_prompt_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            prompt_text = " ".join(page.extract_text().replace("\n", " ") for page in reader.pages if page.extract_text())
            return prompt_text.strip()
    except Exception as e:
        print(f"⚠️ Error reading system prompt: {str(e)}")
        return ""

# ✅ Load system prompt from PDF
pdf_path = os.path.join("Brainstorming Agent - System Prompt.pdf")
system_prompt = extract_prompt_from_pdf(pdf_path)

if not system_prompt:
    print("⚠️ Warning: System prompt not loaded correctly.")
else:
    print("✅ System prompt loaded successfully.")

# ✅ System message to guide AI behavior
system_message = {"role": "system", 
                  "content"
                  : 
                      system_prompt
                  }

# ✅ Initialize chat memory (Limited to last 10 messages for better performance)
memory = [system_message]

@MultiverzAI.route("/")
def home():
    return render_template("index.html")

@MultiverzAI.route("/chat", methods=["POST"])
def chat():
    global memory
    data = request.json
    user_name = data.get("user_name", "").strip()
    user_input = data.get("message", "").strip()

    if not user_name or not user_input:
        return jsonify({"error": "User name and message are required"}), 400

    # ✅ Add user input to memory
    memory.append({"role": "user", "content": user_input})

    # ✅ Keep only the last 10 exchanges (better context, avoids memory overload)
    if len(memory) > 10:
        memory = memory[-10:]

    try:
        # ✅ Make API call to Ollama with conversation history
        payload = {
            "model": "llama3.2:latest",  # ✅ Change to "llama3.2:latest" if needed
            "messages": memory
        }
        response = requests.post(OLLAMA_API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()

            # ✅ Fix response parsing
            ai_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No content received.")

            # ✅ Store AI response in memory
            memory.append({"role": "assistant", "content": ai_response})

        else:
            ai_response = f"⚠️ Error: Ollama API returned {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        ai_response = "⚠️ Error: Could not connect to Ollama. Ensure it is running locally."

    except Exception as e:
        ai_response = f"⚠️ Unexpected error: {str(e)}"

    return jsonify({"user_name": user_name, "user_message": user_input, "ai_response": ai_response})

if __name__ == "__main__":
    MultiverzAI.run(host="0.0.0.0", port=5000, debug=True)
