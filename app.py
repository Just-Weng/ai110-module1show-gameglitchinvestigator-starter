import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, validate_guess_range

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"Guess a number between {low} and {high}.")
with col2:
    attempts_placeholder = st.empty()

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

with st.form("guess_form"):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

new_game = st.button("New Game 🔁")
show_hint = st.checkbox("Show hint", value=True)


def get_hint_style(guess: int, secret: int, low: int, high: int):
    """
    Returns (bg_color, text_color, emoji, intensity_label) based on how
    close the guess is to the secret. Warm = too high, cool = too low.
    """
    total_range = high - low
    distance = abs(guess - secret)
    pct = distance / total_range  # 0.0 = exact, 1.0 = opposite end

    if pct <= 0.08:
        return "#FF2200", "#fff", "🔥🔥🔥", "Burning!"
    elif pct <= 0.17:
        return "#FF6600", "#fff", "🔥🔥", "Hot!"
    elif pct <= 0.33:
        return "#FFC300", "#333", "🔥", "Warm"
    elif pct <= 0.50:
        return "#87CEEB", "#333", "🧊", "Cool"
    elif pct <= 0.75:
        return "#1E90FF", "#fff", "🧊🧊", "Cold!"
    else:
        return "#00008B", "#fff", "🧊🧊🧊", "Freezing!"


def show_hint_box(message: str, guess: int, secret: int, low: int, high: int):
    bg, fg, emoji, label = get_hint_style(guess, secret, low, high)
    st.markdown(
        f"""
        <div style="
            background-color: {bg};
            color: {fg};
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 8px;
        ">
            {emoji} {label} — {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


if new_game:
    for key in ["secret", "attempts", "score", "status", "history"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        in_range, range_err = validate_guess_range(guess_int, low, high)
        if not in_range:
            st.session_state.history.append(guess_int)
            st.error(range_err)
        elif guess_int in st.session_state.history:
            st.warning(f"⚠️ You already guessed {guess_int}!")
            if show_hint:
                outcome, message = check_guess(guess_int, st.session_state.secret)
                show_hint_box(
                    message,
                    guess=guess_int,
                    secret=st.session_state.secret,
                    low=low,
                    high=high,
                )
            st.session_state.attempts -= 1  # don't penalise for duplicate
        else:
            st.session_state.history.append(guess_int)
            outcome, message = check_guess(guess_int, st.session_state.secret)

            if show_hint and outcome != "Win":
                show_hint_box(
                    message,
                    guess=guess_int,
                    secret=st.session_state.secret,
                    low=low,
                    high=high,
                )

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )
            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )

st.divider()
attempts_placeholder.metric("Attempts Left", attempt_limit - st.session_state.attempts)