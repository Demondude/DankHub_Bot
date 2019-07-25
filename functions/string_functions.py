def fix_user_answer(string):
    first_letter = string[0]
    other_letters = string[1:]
    return first_letter.upper() + other_letters.lower()
