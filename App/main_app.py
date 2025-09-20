import streamlit as st
import time
import streamlit.components.v1 as components
from typing_test.prompt_source import get_random_prompt 
from typing_test.typing_calculate import calc_accuracy_pct, calc_wpm_char5 

st.set_page_config(page_title="Typing Speed Meter", page_icon="⌨️")
st.markdown("<h1>Typing Test Master</h1>", unsafe_allow_html=True)

# --- CSS เล็กน้อย ---
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
div.stButton > button:hover { background-color: #5a5a5a ; }
div.stTextInput, div.stMarkdown { text-align: center; }
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

# --- ฟังก์ชัน submit ---
def submit_typing():
    t_elapsed = time.perf_counter() - st.session_state.start_time
    random_sentence = st.session_state.prompt
    user_input = st.session_state.user_input

    N = max(len(random_sentence), len(user_input))
    correct_count = sum(
        1 for i in range(N)
        if (random_sentence[i] if i < len(random_sentence) else "") ==
           (user_input[i] if i < len(user_input) else "")
    )

    typing_accuracy = calc_accuracy_pct(correct_count, N)
    typing_WPM = calc_wpm_char5(len(user_input), t_elapsed)

    st.session_state.results = {
        "time": t_elapsed,
        "accuracy": typing_accuracy,
        "wpm": typing_WPM
    }
    st.rerun()

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

# --- Main ---
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
            st.text_input(
                "Type here and press Enter when done:",
                key="user_input",
                on_change=submit_typing
            )
            components.html(
                '''
                <script>
                const typingInput = window.parent.document.querySelector("input[aria-label='Type here and press Enter when done:']");
                if (typingInput) {
                    typingInput.focus();
                    typingInput.setSelectionRange(typingInput.value.length, typingInput.value.length);
                }
                </script>
                ''',
                height=0,
            )
