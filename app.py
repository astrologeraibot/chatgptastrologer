import streamlit as st
import openai
from datetime import datetime

# Load your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

st.set_page_config(page_title="Astrologer Chatbot", page_icon="🔮")
st.title("🔮 Astrologer Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar form for birth details
with st.sidebar.form("birth_details"):
    st.header("Your Birth Details")
    name = st.text_input("Name", value="")
    birth_date = st.date_input("Birth Date")
    birth_time = st.time_input("Birth Time")
    birth_place = st.text_input("Birth Place")
    submit_birth = st.form_submit_button("Save Details")

if submit_birth:
    st.success("Birth details saved!")

# Main form for astrology question
with st.form("question_form", clear_on_submit=True):
    question = st.text_area("Ask your astrology question here...")
    submit_question = st.form_submit_button("Ask Astrologer")

if submit_question:
    if not name or not birth_place:
        st.error("Please enter your name and birth place in the sidebar!")
    else:
        # Format user message combining birth details + question
        user_message = (
            f"My name is {name}. I was born on {birth_date} at {birth_time} in {birth_place}. "
            f"I want to know: {question}"
        )
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Call OpenAI ChatCompletion with new SDK syntax
        with st.spinner("Consulting the stars... 🔮"):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.8,
                max_tokens=500,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Display the chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Astrologer:** {msg['content']}")
