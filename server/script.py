def complex_processing(user_input):
    # Example: Reverse the string and count characters
    reversed_text = user_input[::-1]
    char_count = len(user_input)

    # Return a formatted result
    return {
        "original": user_input,
        "reversed": reversed_text,
        "char_count": char_count
    }
