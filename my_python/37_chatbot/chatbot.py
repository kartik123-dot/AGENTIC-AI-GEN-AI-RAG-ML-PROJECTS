
import streamlit as st
from nltk.chat.util import Chat, reflections

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="NEURO | AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- FUTURISTIC CSS ----------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top left, #142447 0%, transparent 45%),
        radial-gradient(ellipse at bottom right, #24133f 0%, transparent 45%),
        #080d18;
    color: #eaf4ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #f4f8ff;
}

.hero {
    text-align: center;
    padding: 25px 10px;
    border: 1px solid rgba(0, 225, 255, 0.25);
    border-radius: 22px;
    background: rgba(15, 27, 48, 0.75);
    box-shadow: 0 0 30px rgba(0, 225, 255, 0.08);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 5px;
    background: linear-gradient(90deg, #00e5ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #a9bbd4;
    font-size: 14px;
    letter-spacing: 2px;
}

.status {
    color: #48f5b0;
    font-size: 13px;
}

section[data-testid="stSidebar"] {
    background: rgba(9, 16, 30, 0.98);
    border-right: 1px solid rgba(0, 225, 255, 0.2);
}

div[data-testid="stChatMessage"] {
    background: rgba(18, 30, 52, 0.78);
    border: 1px solid rgba(130, 170, 255, 0.13);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
}

div[data-testid="stChatInput"] {
    border: 1px solid #00cfe8;
    border-radius: 16px;
    box-shadow: 0 0 15px rgba(0, 207, 232, 0.12);
}

.stButton > button {
    width: 100%;
    border: 1px solid #00d9ff;
    background: #101d32;
    color: #eafaff;
    border-radius: 12px;
    transition: 0.25s;
}

.stButton > button:hover {
    background: #12374b;
    border-color: #a78bfa;
    color: white;
    box-shadow: 0 0 15px rgba(0, 225, 255, 0.25);
}

div[data-testid="stMetric"] {
    background: rgba(19, 33, 56, 0.8);
    border: 1px solid rgba(0, 225, 255, 0.18);
    padding: 14px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CHATBOT RULES ----------------
pairs = [
    [
        r"(.*)my name is (.*)",
        ["Hello %2, how are you today?"]
    ],
    [
        r"(.*)help(.*)",
        ["I can help you. What would you like to know?"]
    ],
    [
        r"(.*)your name(.*)",
        ["My name is Neuro, your Python-powered chatbot."]
    ],
    [
        r"how are you(.*)",
        ["I'm doing very well!", "I'm great! How about you?"]
    ],
    [
        r"sorry(.*)",
        ["It's alright.", "No worries, never mind that."]
    ],
    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Nice to hear that!", "Alright, great!"]
    ],
    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello!", "Hey there!", "Hi! How can I help?"]
    ],
    [
        r"what(.*)want(.*)",
        ["Make me an offer I can't refuse!"]
    ],
    [
        r"(.*)created(.*)",
        ["I was created using Python and the NLTK library."]
    ],
    [
        r"(.*)(location|city)(.*)",
        ["My original chatbot script mentions Hyderabad, India."]
    ],
    [
        r"(.*)raining in (.*)",
        ["I cannot check live weather yet, but I can chat about it!"]
    ],
    [
        r"how(.*)health(.*)",
        ["Health is important! I'm a computer, so I don't need to worry about mine."]
    ],
    [
        r"(.*)(sports|game|sport)(.*)",
        ["I'm a big fan of cricket!"]
    ],
    [
        r"(.*)(cricketer|batsman)(.*)",
        ["Virat Kohli!"]
    ],
    [
        r"quit",
        ["Goodbye! See you soon."]
    ],
    [
        r"(.*)",
        ["I'm still learning! Could you ask me another way?"]
    ]
]

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm Neuro, your personal chatbot. "
                "How can I help you today?"
            )
        }
    ]

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chat(pairs, reflections)

if "user_count" not in st.session_state:
    st.session_state.user_count = 0

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🤖 NEURO")
    st.caption("PERSONAL AI INTERFACE")
    st.markdown("---")

    st.markdown("### SYSTEM STATUS")
    st.markdown(
        '<p class="status">● ONLINE</p>',
        unsafe_allow_html=True
    )
    st.caption("Engine: Python + NLTK")
    st.caption("Mode: Rule-based chatbot")

    st.markdown("---")
    st.markdown("### QUICK PROMPTS")

    prompts = [
        "Hello",
        "What is your name?",
        "Who created you?",
        "Tell me about cricket",
        "I need help"
    ]

    for prompt in prompts:
        if st.button(prompt, key="prompt_" + prompt):
            st.session_state.pending_prompt = prompt

    st.markdown("---")
    st.metric("Messages sent", st.session_state.user_count)

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation cleared. What shall we talk about?"
            }
        ]
        st.session_state.user_count = 0
        st.session_state.chatbot = Chat(pairs, reflections)
        st.session_state.pop("pending_prompt", None)
        st.rerun()

    st.markdown("---")
    st.caption("Built with Python, NLTK & Streamlit")

# ---------------- MAIN HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="hero-title">NEURO AI</div>
    <div class="hero-subtitle">
        NEXT-GENERATION CONVERSATIONAL INTERFACE
    </div>
    <br>
    <div class="status">● SYSTEM ONLINE &nbsp; | &nbsp; READY TO CHAT</div>
</div>
""", unsafe_allow_html=True)

# ---------------- CHAT HISTORY ----------------
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- PROCESS MESSAGE ----------------
def process_message(user_text):
    user_text = user_text.strip()

    if not user_text:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    st.session_state.user_count += 1

    if user_text.lower() in ["quit", "exit", "bye"]:
        response = "Goodbye! It was nice talking to you. 👋"
    else:
        response = st.session_state.chatbot.respond(user_text)

        if not response:
            response = "I'm still learning! Try asking me something else."

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# Handle quick prompt buttons
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")
    process_message(prompt)
    st.rerun()

# Chat input
user_input = st.chat_input("Message Neuro AI...")

if user_input:
    process_message(user_input)
    st.rerun()
