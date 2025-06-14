import os

HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0  # If file is empty or corrupted
    return 0  # No file yet

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

