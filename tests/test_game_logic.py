import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_sequential_guesses():
    # Test that sequential guesses are processed correctly without being skipped
    secret = 50
    sequential_guesses = [10, 20, 30, 40, 45, 49, 50]
    expected_outcomes = [
        "Too Low",   # 10 < 50
        "Too Low",   # 20 < 50
        "Too Low",   # 30 < 50
        "Too Low",   # 40 < 50
        "Too Low",   # 45 < 50
        "Too Low",   # 49 < 50
        "Win",       # 50 == 50
    ]
    
    for guess, expected in zip(sequential_guesses, expected_outcomes):
        outcome, message = check_guess(guess, secret)
        assert outcome == expected, f"Guess {guess} should result in {expected}, but got {outcome}"

def test_parse_sequential_string_inputs():
    # Test that sequential string inputs are parsed correctly
    sequential_inputs = ["1", "2", "3", "4", "5"]
    expected_values = [1, 2, 3, 4, 5]
    
    for input_str, expected_value in zip(sequential_inputs, expected_values):
        ok, parsed_value, error = parse_guess(input_str)
        assert ok is True, f"Input {input_str} should parse successfully"
        assert parsed_value == expected_value, f"Input {input_str} should parse to {expected_value}, but got {parsed_value}"
        assert error is None, f"Input {input_str} should not have an error"
