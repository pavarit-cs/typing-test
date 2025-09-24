from __future__ import annotations

from typing import Any, Dict


def compute_metrics(prompt: str, user_input: str) -> Dict[str, Any]:
    """Compare prompt and user input at character and word levels."""
    prompt_chars = list(prompt)
    input_chars = list(user_input)
    char_total = max(len(prompt_chars), len(input_chars))
    char_correct = 0
    char_incorrect = 0

    for i in range(char_total):
        p_char = prompt_chars[i] if i < len(prompt_chars) else ""
        u_char = input_chars[i] if i < len(input_chars) else ""
        if p_char == u_char:
            char_correct += 1
        else:
            char_incorrect += 1

    prompt_words = prompt.split()
    input_words = user_input.split()
    word_total = max(len(prompt_words), len(input_words))
    word_correct = 0
    word_incorrect = 0
    for i in range(word_total):
        p_word = prompt_words[i] if i < len(prompt_words) else ""
        u_word = input_words[i] if i < len(input_words) else ""
        if p_word == u_word:
            word_correct += 1
        else:
            word_incorrect += 1

    return {
        "char_correct": char_correct,
        "char_incorrect": char_incorrect,
        "char_total": char_total,
        "word_correct": word_correct,
        "word_incorrect": word_incorrect,
        "word_total": word_total,
        "prompt_word_count": len(prompt_words),
        "input_word_count": len(input_words),
    }
