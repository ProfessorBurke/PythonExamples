"""
    Text version of wordle.
"""

def get_word() -> str:
    return "sighs"

def get_user_word() -> str:
    """Obtain a guess from the user."""
    word: str = input("What is your guess? ")
    return word[:5]

def word_to_ordered_pairs(word: str) -> set:
    """Return the word as a set of ordered pairs of
       tuples of (letter, index)."""
    i: int = 0
    letter: str
    result: list = []
    for letter in word:
        result.append((i, letter))
        i += 1
    return set(result)
        

def result(word: set, user_guess: set) -> tuple:
    """Compare user guess to word and return a string for
       the user and True if they've won."""
    won: bool = False
    # Intersect the sets to find letters in the correct place,
    # then sort the sets (converted to lists) by index to put
    # them in word order
    green_letters: set = word & user_guess
    other_letters: set = user_guess - green_letters
    green_letters_ordered: list = list(green_letters)
    green_letters_ordered.sort()
    other_letters_ordered: list = list(other_letters)
    other_letters_ordered.sort()

    # Create a result of letters that are in the right place.
    result: list = []
    for pair in green_letters_ordered:
        result.append("*" + pair[1] + "*")

    # If there are other letters, find which ones
    # are in the word but in the wrong place
    # and add to the result.
    if len(other_letters_ordered) > 0:
        answer_word: list = []
        remaining_letters_word: set = word - green_letters
        for pair in remaining_letters_word:
            answer_word.append(pair[1])
        for pair in other_letters_ordered:
            if pair[1] in answer_word:
                result.insert(pair[0], "_" + pair[1]+ "_")
                answer_word.remove(pair[1])
            else:
                result.insert(pair[0], pair[1])
            other_letters_ordered = other_letters_ordered[1:]
    else:
        won = True
    
    return result, won
    

def main() -> None:
##    word: str = get_word()
##    winning_word_set: set = word_to_ordered_pairs(word)
##    won: bool = False
##    i: int = 0
##    user_guess_set: set
##    while i < 6 and not won:
##        user_word = get_user_word()
##        user_guess_set = word_to_ordered_pairs(user_word)
##        result_str, won = result(winning_word_set, user_guess_set)
##        print(result_str)
##        i += 1

    # Test the result function
    word_set: set = {(0, "a"), (1, "a"), (2, "a"), (3, "a"),(4, "a")}
    guess: set
    result_list: list
    won: bool

    # Winning word
    guess = {(0, "a"), (1, "a"), (2, "a"), (3, "a"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert won 
    assert result_list ==['*a*', '*a*', '*a*', '*a*', '*a*']

    # All but one correct
    guess = {(0, "a"), (1, "a"), (2, "a"), (3, "a"),(4, "b")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['*a*', '*a*', '*a*', '*a*', 'b']
    guess = {(0, "a"), (1, "a"), (2, "a"), (3, "b"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['*a*', '*a*', '*a*', 'b', '*a*']
    guess = {(0, "a"), (1, "a"), (2, "b"), (3, "a"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['*a*', '*a*', 'b', '*a*', '*a*']
    guess = {(0, "a"), (1, "b"), (2, "a"), (3, "a"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['*a*', 'b', '*a*', '*a*', '*a*']
    guess = {(0, "b"), (1, "a"), (2, "a"), (3, "a"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['b', '*a*', '*a*', '*a*', '*a*']

    # All letters correct; wrong order
    word_set = {(0, "s"), (1, "t"), (2, "a"), (3, "r"),(4, "e")}
    guess = {(0, "t"), (1, "a"), (2, "r"), (3, "e"),(4, "s")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['_t_', '_a_', '_r_', '_e_', '_s_']

    # Multiple same letter; wrong order
    # Multiple same letter not in word
    word_set = {(0, "s"), (1, "n"), (2, "i"), (3, "f"),(4, "f")}
    guess = {(0, "f"), (1, "a"), (2, "f"), (3, "s"),(4, "a")}
    result_list, won = result(word_set, guess)
    assert not won 
    assert result_list ==['_f_', 'a', '_f_', '_s_', 'a']

main()
