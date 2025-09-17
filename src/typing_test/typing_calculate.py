MIN_DURATION = 0.2  # minimum duration in seconds to avoid unrealistic WPM

def calc_accuracy_pct(correct: int, total_positions: int) -> float:
    """Calculate typing accuracy percentage.

    Args:
        correct (int): Number of correctly typed characters.
        total_positions (int): Maximum length between prompt and input.

    Returns:
        float: Accuracy percentage (0–100), rounded to two decimals.
    """
    if total_positions <= 0:
        return 0.0
    return round(correct * 100.0 / total_positions, 2)


def calc_wpm_char5(total_chars: int, duration_sec: float) -> float:
    """Calculate Words Per Minute (WPM) using the 5-characters-per-word standard.

    Formula:
        WPM = (total_chars / 5) / (duration_sec / 60)

    Args:
        total_chars (int): Number of characters typed by the user.
        duration_sec (float): Time spent typing in seconds.

    Returns:
        float: Words per minute, rounded to two decimals.
    """
    duration_min = max(duration_sec / 60.0, MIN_DURATION / 60.0)
    
    
    return round((total_chars / 5.0) / duration_min, 2)

