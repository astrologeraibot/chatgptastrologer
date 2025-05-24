import streamlit as st
import openai
from datetime import datetime

# Optional: replace with your actual OpenAI API key for local testing
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-xxx")

st.set_page_config(page_title="Astrologer Chatbot", page_icon="🔮")
st.title("🔮 Ask the Astrologer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input form
with st.form("astro_form"):
    name = st.text_input("Your Name")
    birth_date = st.date_input("Birth Date")
    birth_time = st.time_input("Birth Time")
    birth_place = st.text_input("Birth Place")
    question = st.text_area("What would you like to ask?")
    submitted = st.form_submit_button("Ask")

if submitted:
    # Format user input
    user_message = (
        f"My name is {name}. I was born on {birth_date} at {birth_time} in {birth_place}. "
        f"{question}"
    )

    st.session_state.messages.append({"role": "user", "content": user_message})

    # Call OpenAI GPT model
    with st.spinner("Astrologer is thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
        )
        reply = response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Astrologer:** {msg['content']}")
