import streamlit as st
import time
import sys
#sys.path.append(r"C:\Users\user\Desktop\673380278-9\My project\Typing-Test-CLI\src\typing_test")
from typing_test.prompt_source import get_random_prompt 
from typing_test.typing_calculate import calc_accuracy_pct, calc_wpm_char5 

st.set_page_config(page_title="Typing Speed Meter", page_icon="⌨️")
st.markdown("<h1>Typing Test Master</h1>", unsafe_allow_html=True)
st.markdown("""
<style>
div.stButton > button {
    display: block ;
    margin: 10px auto ;
    background-color: grey ;
    color: white ;
    padding: 10px 25px ;
    border-radius: 8px ;
    font-size: 16px ;
    cursor: pointer ;
}

/* hover effect สวยๆ */
div.stButton > button:hover {
    background-color: #5a5a5a ;
}

div.stTextInput, div.stTextArea, div.stMarkdown {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- session state ---
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "results" not in st.session_state:
    st.session_state.results = None

# --- Show Result ---
if st.session_state.results:
    st.subheader("📊 Result")
    st.write(f"⏱ Time: **{st.session_state.results['time']:.2f} s**")
    st.write(f"🎯 Accuracy: **{st.session_state.results['accuracy']} %**")
    st.write(f"⌨️ Speed (WPM): **{st.session_state.results['wpm']}**")

    if st.button("🔁 Try Again"):
        st.session_state.prompt = ""
        st.session_state.start_time = None
        st.session_state.user_input = ""
        st.session_state.results = None
        st.rerun()

# --- show Main ---
else:
    if st.button("Get Prompt"):
        st.session_state.prompt = get_random_prompt()
        st.session_state.start_time = None
        st.session_state.user_input = ""
        st.session_state.results = None

    if st.session_state.prompt:
        st.subheader("Prompt")
        st.info(st.session_state.prompt)

        if st.session_state.start_time is None:
            if st.button("Start"):
                st.session_state.start_time = time.perf_counter()
                st.rerun()
        else:
            st.subheader("Typing here")
            st.session_state.user_input = st.text_area(
                "",
                value=st.session_state.user_input,
                height=100,
                placeholder="Start typing..."
            )

            if st.button("Submit"):
                t_elapsed = time.perf_counter() - st.session_state.start_time
                random_sentence = st.session_state.prompt
                user_input = st.session_state.user_input

                correct_count, incorrect_count = 0, 0
                length_prompt = len(random_sentence)
                length_user_input = len(user_input)
                N = max(length_prompt, length_user_input)

                for i in range(N):
                    p_char = random_sentence[i] if i < length_prompt else ""
                    u_char = user_input[i] if i < length_user_input else ""
                    if p_char == u_char:
                        correct_count += 1
                    else:
                        incorrect_count += 1

                typing_accuracy = calc_accuracy_pct(correct_count, N)
                typing_WPM = calc_wpm_char5(length_user_input, t_elapsed)

                st.session_state.results = {
                    "time": t_elapsed,
                    "accuracy": typing_accuracy,
                    "wpm": typing_WPM
                }
                st.rerun()