from flask import Flask, render_template, request, jsonify
from mistralai import Mistral  # Import Mistral library
import PyPDF2
import os

# Initialize Flask app
MultiverzAI = Flask(__name__)

# Function to extract system prompt from a PDF
def extract_prompt_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            prompt_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    prompt_text.append(page_text.replace("\n", " "))  
            return " ".join(prompt_text).strip()
    except Exception as e:
        print(f"⚠️ Error reading system prompt: {str(e)}")
        return "You are an AI assistant. Answer questions helpfully."

# Load system prompt from the PDF
pdf_path = "Brainstromming/Brainstorming Agent - System Prompt.pdf"  
system_prompt = extract_prompt_from_pdf(pdf_path)

print("✅ System prompt loaded successfully." if system_prompt else "⚠️ Using default system prompt.")

# System prompt message
system_message = {"role": "system", "content": system_prompt}

# Initialize chat memory (Limit history to prevent excessive memory usage)
memory = []

@MultiverzAI.route("/")
def home():
    return render_template("index.html")

@MultiverzAI.route("/chat", methods=["POST"])
def chat():
    global memory
    data = request.get_json()

    # Validate request data
    if not data or "message" not in data or not data["message"].strip():
        return jsonify({"error": "Message cannot be empty."}), 400

    user_input = data["message"].strip()
    user_name = data.get("user_name", "User").strip()

    memory.append({"role": "user", "content": user_input})

    try:
        # Initialize Mistral client
        api_key = "N2VeTffMFqGYvyVS3D8ZJKgjmlvn7VKZ"  # Replace with your actual API key
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)
        
        # Send chat request
        response = client.chat.complete(
            model=model,
            messages=[system_message] + memory  # Include system prompt + chat history
        )

        ai_response = response.choices[0].message.content if response.choices else "I couldn't understand that."

        # Store AI response in memory
        memory.append({"role": "assistant", "content": ai_response})

        # Limit chat memory to the last 10 exchanges (to avoid infinite growth)
        memory = memory[-10:]

    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return jsonify({"user_name": user_name, "user_message": user_input, "ai_response": ai_response})

if __name__ == "__main__":
    MultiverzAI.run(host="0.0.0.0", port=5000, debug=True)
