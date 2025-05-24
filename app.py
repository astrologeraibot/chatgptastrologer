import streamlit as st
import openai
import time

openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

st.set_page_config(page_title="Astrologer Chatbot", page_icon="🔮")
st.title("🔮 Astrologer Chatbot")

# Cooldown settings
MIN_SECONDS_BETWEEN_REQUESTS = 10

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

with st.sidebar.form("birth_details"):
    st.header("Your Birth Details")
    name = st.text_input("Name", value="")
    birth_date = st.date_input("Birth Date")
    birth_time = st.time_input("Birth Time")
    birth_place = st.text_input("Birth Place")
    submit_birth = st.form_submit_button("Save Details")

if submit_birth:
    st.success("Birth details saved!")

with st.form("question_form", clear_on_submit=True):
    question = st.text_area("Ask your astrology question here...")
    submit_question = st.form_submit_button("Ask Astrologer")

now = time.time()
time_since_last = now - st.session_state.last_request_time

if submit_question:
    if time_since_last < MIN_SECONDS_BETWEEN_REQUESTS:
        st.warning(f"Please wait {int(MIN_SECONDS_BETWEEN_REQUESTS - time_since_last)} seconds before asking another question.")
    elif not name or not birth_place:
        st.error("Please enter your name and birth place in the sidebar!")
    elif question.strip() == "":
        st.error("Please enter a question.")
    else:
        user_message = (
            f"My name is {name}. I was born on {birth_date} at {birth_time} in {birth_place}. "
            f"I want to know: {question}"
        )
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.session_state.last_request_time = now

        with st.spinner("Consulting the stars... 🔮"):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.8,
                max_tokens=500,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Astrologer:** {msg['content']}")
