import streamlit as st
import webbrowser
import datetime
import requests
import json
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.title("🤖 JARVIS AI (Streamlit Edition)")
st.write("Your Smart AI Assistant 🚀")

MEMORY_FILE = "memory.json"

# -------------------------------
# MEMORY FUNCTIONS
# -------------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------------
# AI RESPONSE (FREE API)
# -------------------------------
def ai_response(prompt):
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": prompt, "format": "json"}
        res = requests.get(url, params=params)
        data = res.json()
        return data.get("AbstractText", "I couldn't find a direct answer.")
    except:
        return "Error connecting to AI service."

# -------------------------------
# COMMAND PROCESSOR
# -------------------------------
def process_command(command):
    command = command.lower()
    memory = load_memory()

    # TIME
    if "time" in command:
        return datetime.datetime.now().strftime("Time: %H:%M:%S")

    # DATE
    elif "date" in command:
        return datetime.datetime.now().strftime("Date: %d-%m-%Y")

    # OPEN WEBSITES
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    elif "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub"

    # SEARCH
    elif "search" in command:
        query = command.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query}"

    # MEMORY
    elif "remember" in command:
        data = command.replace("remember", "").strip()
        memory["note"] = data
        save_memory(memory)
        return f"I will remember: {data}"

    elif "what do you remember" in command:
        return str(memory)

    # NOTES
    elif "save note" in command:
        note = command.replace("save note", "")
        memory["note"] = note
        save_memory(memory)
        return "Note saved"

    # DEFAULT AI
    else:
        return ai_response(command)

# -------------------------------
# SESSION CHAT
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# INPUT
# -------------------------------
st.subheader("💬 Chat")

user_input = st.text_input("Type your command")

if st.button("Run"):
    if user_input:
        response = process_command(user_input)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Jarvis", response))

# -------------------------------
# DISPLAY CHAT
# -------------------------------
st.subheader("📜 Conversation")

for role, text in st.session_state.history[::-1]:
    if role == "You":
        st.markdown(f"**🧑 You:** {text}")
    else:
        st.markdown(f"**🤖 Jarvis:** {text}")

# -------------------------------
# QUICK ACTIONS
# -------------------------------
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏰ Time"):
        st.success(process_command("time"))

with col2:
    if st.button("🌐 YouTube"):
        st.success(process_command("open youtube"))

with col3:
    if st.button("🔍 Google"):
        st.success(process_command("open google"))

# -------------------------------
# NOTES SECTION
# -------------------------------
st.subheader("📝 Notes")

note_input = st.text_area("Write a note")

if st.button("Save Note"):
    memory = load_memory()
    memory["note"] = note_input
    save_memory(memory)
    st.success("Note saved!")

if st.button("Show Notes"):
    st.info(load_memory())

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Features")

st.sidebar.markdown("""
### ✅ Features:
- AI Chat
- Memory
- Notes
- Web Automation
- Search Engine

### 🚀 Upgrade Ideas:
- Add OpenAI API
- Voice input
- WhatsApp automation
- Database storage
""")
