from __future__ import annotations

import time
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from typing_test.prompt_source import get_random_prompt
from typing_test.typing_calculate import calc_accuracy_pct, calc_wpm_char5
from typing_test.metrics import compute_metrics
from typing_test.stats_store import (
    append_stat,
    create_stat_record,
    load_stats,
    recent_stats,
    summarize_stats,
)

CHALLENGE_TIME_LIMIT = 30.0  # seconds

st.set_page_config(page_title="Typing Speed Meter", page_icon="⌨️")
st.markdown("<h1>Typing Test Master</h1>", unsafe_allow_html=True)

st.markdown(
    """
<style>
div.stButton > button {
    display: block;
    margin: 8px auto;
    background-color: grey;
    color: white;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}
div.stButton > button:hover { background-color: #5a5a5a; }
div.stTextInput, div.stMarkdown { text-align: center; }
</style>
""",
    unsafe_allow_html=True,
)


def _format_timestamp(value: str | None) -> str:
    if not value:
        return "-"
    try:
        dt = datetime.fromisoformat(value)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return value


# --- session state ---
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "mode" not in st.session_state:
    st.session_state.mode = "standard"
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "results" not in st.session_state:
    st.session_state.results = None


def _reset_prompt(prompt: str, mode: str) -> None:
    st.session_state.prompt = prompt
    st.session_state.mode = mode
    st.session_state.start_time = None
    st.session_state.user_input = ""
    st.session_state.results = None


def _handle_new_prompt() -> None:
    prompt = get_random_prompt()
    st.session_state.last_prompt = prompt
    _reset_prompt(prompt, "standard")
    st.rerun()


def _handle_challenge_prompt() -> None:
    prompt = st.session_state.last_prompt
    if not prompt:
        return
    _reset_prompt(prompt, "challenge")
    st.rerun()


def submit_typing() -> None:
    if st.session_state.start_time is None:
        return

    elapsed = time.perf_counter() - st.session_state.start_time
    prompt = st.session_state.prompt
    user_input = st.session_state.user_input
    mode = st.session_state.mode

    metrics = compute_metrics(prompt, user_input)
    accuracy = calc_accuracy_pct(metrics["word_correct"], metrics["word_total"])
    wpm = calc_wpm_char5(len(user_input), elapsed)

    result = {
        "time": elapsed,
        "accuracy": accuracy,
        "wpm": wpm,
        "metrics": metrics,
        "mode": mode,
        "saved": True,
        "message": "",
    }

    time_limit = CHALLENGE_TIME_LIMIT if mode == "challenge" else None
    if time_limit is not None and elapsed > time_limit:
        result["saved"] = False
        result["message"] = f"หมดเวลา {int(time_limit)} วินาทีจึงไม่ได้บันทึกผล"
    else:
        record = create_stat_record(
            duration_sec=elapsed,
            accuracy_pct=accuracy,
            wpm=wpm,
            prompt_length=len(prompt),
            input_length=len(user_input),
            correct_chars=metrics["char_correct"],
            char_total=metrics["char_total"],
            incorrect_chars=metrics["char_incorrect"],
            prompt=prompt,
            mode=mode,
            correct_words=metrics["word_correct"],
            incorrect_words=metrics["word_incorrect"],
            word_total=metrics["word_total"],
            prompt_word_count=metrics["prompt_word_count"],
            input_word_count=metrics["input_word_count"],
        )
        append_stat(record)
        if mode == "standard":
            st.session_state.last_prompt = prompt

    st.session_state.results = result
    st.session_state.start_time = None
    st.session_state.user_input = ""
    st.rerun()


typing_tab, stats_tab = st.tabs(["Typing", "Statistics"])

with typing_tab:
    st.subheader("โหมดทดสอบ")
    col1, col2 = st.columns(2)
    if col1.button("สุ่มประโยคใหม่"):
        _handle_new_prompt()
    if col2.button("โหมดทำลายสถิติ 30 วิ", disabled=not st.session_state.last_prompt):
        _handle_challenge_prompt()

    if st.session_state.results:
        result = st.session_state.results
        metrics = result["metrics"]
        st.success("บันทึกผลเรียบร้อย" if result["saved"] else "การทดลองเสร็จสิ้น")
        st.write(f"**โหมด**: {'มาตรฐาน' if result['mode'] == 'standard' else 'ทำลายสถิติ 30 วินาที'}")
        st.write(f"**เวลา**: {result['time']:.2f} วินาที")
        st.write(f"**ความแม่นยำ (เทียบคำ)**: {result['accuracy']} %")
        st.write(f"**ความเร็ว**: {result['wpm']} WPM")
        st.write(
            f"**คำที่ตรงกัน**: {metrics['word_correct']} / {metrics['word_total']}"
        )
        if not result["saved"] and result["message"]:
            st.warning(result["message"])

        col_retry, col_challenge = st.columns(2)
        if col_retry.button("เริ่มใหม่"):
            st.session_state.results = None
            st.session_state.prompt = ""
            st.session_state.start_time = None
            st.session_state.user_input = ""
            st.rerun()
        if (
            result["saved"]
            and result["mode"] == "standard"
            and st.session_state.last_prompt
            and col_challenge.button("ลองโหมด 30 วิ ด้วยประโยคนี้")
        ):
            _handle_challenge_prompt()

    else:
        if st.session_state.prompt:
            mode_label = (
                "มาตรฐาน (สุ่มประโยค)"
                if st.session_state.mode == "standard"
                else "ทำลายสถิติ 30 วินาที"
            )
            st.info(f"Prompt ({mode_label})")
            st.write(st.session_state.prompt)

            if st.session_state.start_time is None:
                start_label = "เริ่มจับเวลา"
                if st.button(start_label):
                    st.session_state.start_time = time.perf_counter()
                    st.rerun()
            else:
                st.subheader("พิมพ์ข้อความ")
                st.text_area(
                    "พิมพ์ประโยคและกด Enter / Ctrl+Enter เมื่อเสร็จ:",
                    key="user_input",
                    on_change=submit_typing,
                    height=180,
                )
                components.html(
                    """<script>
const typingArea = window.parent.document.querySelector("textarea[aria-label='พิมพ์ประโยคและกด Enter / Ctrl+Enter เมื่อเสร็จ:']");
if (typingArea) {
    typingArea.focus();
    typingArea.selectionStart = typingArea.value.length;
    typingArea.selectionEnd = typingArea.value.length;
}
</script>""",
                    height=0,
                )
        else:
            st.info("กดปุ่ม \"สุ่มประโยคใหม่\" เพื่อเริ่มต้น")

with stats_tab:
    st.subheader("สถิติทั้งหมด")
    stats = load_stats()
    if not stats:
        st.info("ยังไม่มีข้อมูลสถิติ ลองทำแบบทดสอบสักครั้งก่อนนะ!")
    else:
        summary = summarize_stats(stats)
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("จำนวนครั้ง", summary["total_sessions"])
        col_b.metric("ค่าเฉลี่ย WPM", summary["avg_wpm"])
        col_c.metric("ค่าเฉลี่ย Accuracy", f"{summary['avg_accuracy']} %")

        if summary["best_wpm"] is not None:
            st.caption(
                f"🟢 สถิติ WPM สูงสุด {summary['best_wpm']} เมื่อ {_format_timestamp(summary['best_wpm_timestamp'])}"
            )
        if summary["best_accuracy"] is not None:
            st.caption(
                f"🟣 สถิติ Accuracy สูงสุด {summary['best_accuracy']}% เมื่อ {_format_timestamp(summary['best_accuracy_timestamp'])}"
            )

        st.markdown("### ผลล่าสุด")
        recent_entries = list(reversed(recent_stats(stats, limit=8)))
        for entry in recent_entries:
            ts = _format_timestamp(entry.get("timestamp"))
            mode = (entry.get("mode") or "standard").capitalize()
            wpm = entry.get("wpm")
            accuracy = entry.get("accuracy_pct")
            duration = entry.get("duration_sec")
            total_words = entry.get("word_total")
            correct_words = entry.get("correct_words")
            if total_words is None and correct_words is not None:
                total_words = (correct_words or 0) + (entry.get("incorrect_words") or 0)
            stats_line = (
                f"{ts} · โหมด {mode} · WPM {wpm} · Accuracy {accuracy}% · เวลา {duration:.2f}s"
            )
            if total_words and correct_words is not None:
                stats_line += f" · คำตรง {int(correct_words)}/{int(total_words)}"
            st.write(stats_line)

        st.markdown("---")
        st.caption("คุณสามารถลบไฟล์ `stats.json` หากต้องการรีเซ็ตสถิติทั้งหมด")
