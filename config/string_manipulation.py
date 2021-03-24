def to_snake_case(str):
    stripped_string = str.strip()
    lower_string = stripped_string.lower()
    hyph_string = lower_string.replace(' ', '-')
    return hyph_string


def from_snake_case(str):
    return str.replace('-', ' ')


def detag_submission_title(submission_title):
    while True:
        if ']' in submission_title[:10]:
            target_index = submission_title.index(']')
            submission_title = submission_title[target_index + 1:]
        elif ')' in submission_title[:10]:
            target_index = submission_title.index(')')
            submission_title = submission_title[target_index + 1:]
        else:
            return submission_title
