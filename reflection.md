# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  1) The first bug that I noticed was that the hints was backwards. It would prompt to go lower when it meant to go higher, and vice versa.

  2) There was no boundary checking for whether the user input was out of range. So it was possible to enter values above or below the range (0-100).

  3) Some user guesses do not generate a hint. Regardless of whether the hint checkbox is checked.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude for this project:

One example of a suggestion that was correct was that the st.session_state.attempts was initialized to 1 than 0, which led to one less attempt that was given. I verified the result by manually inputting guesses and checking the history under Developer Debug Info. I then tried to set it to 0 and rerunning, and it fixed the issue.

One incorrect suggestion that Claude made was that every entry was stored in history. This was false because I tested manually guessing (1-11) and checked Developer Debug Info. Only 1,3,6,7,9,10 showed up in history.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
One test I ran was a pytest that tested pre-populated values through a sequential guess array and it passed after some modifications to logic_utils.py. AI did not really design the test, because I asked about the test when I manually entered it. Instead it helped with the setup of the tests directly into the editor instead of manually testing the values.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?
1) The secret number changes because every time Streamlit reran the script everytime there was interaction with widgets.

2) Streamlit reran the script on button press but to solve it forgetting the secret, it needed to use the st.session_state to preserve the secret and check if the secret already exists

3) The change was the check if the secret was in st.session_state.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit was asking why the AI decided to do this, and If something broke, what broke, and how to fix it. I would prompt, then test the fix, and ask again if it did not truly fix the bug.

One thing that I would do differently is to instead of asking Copilot to immediately fix the change when I had the errors in the pytest, to instead explain the process out and fix them manually.

This project changed my outlook on AI generated code. The process of debugging broken code is much harder than creating code from scratch. You need to find out what is broken, what caused it, and what can fix it.