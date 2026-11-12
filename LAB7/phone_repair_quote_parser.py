# Lab 7: Fuzzing for Input Validation Bugs (fixed module)
# Kshitij Gupta | PES1UG24AM915 | Section F
#
# Every function now checks its input before using it and returns None for
# anything it cannot handle, instead of raising an exception.

import re

MAX_QUANTITY = 100

# An IMEI is exactly 15 digits. [0-9] is used instead of \d, which would also
# accept non-ASCII digits such as '٣' or '²'.
_IMEI = re.compile(r"[0-9]{15}")

# One order item: a part name, whitespace, 'x' (or 'X'), then a 1-3 digit quantity.
# Matching the *last* 'x' this way means part names such as 'box' still work.
_ORDER_ITEM = re.compile(r"(?P<part>.+?)\s+[xX]\s*(?P<qty>[0-9]{1,3})")


def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four digits.
    Returns None if imei is not a string holding a 15-digit IMEI.
    """
    if not isinstance(imei, str):
        return None
    digits = imei.replace('-', '').replace(' ', '')
    if not _IMEI.fullmatch(digits):
        return None
    return '*' * (len(digits) - 4) + digits[-4:]


def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a {part: quantity} dictionary.
    Blank items (such as after a trailing ';') are skipped, part names are
    lower-cased, and a part listed twice has its quantities added together.
    Returns None if text is not a string, contains no items, or any item is
    not 'part xQTY' with a letter in the part name and a total of 1-100.
    """
    if not isinstance(text, str):
        return None
    order = {}
    for item in text.split(';'):
        item = item.strip()
        if not item:
            continue
        match = _ORDER_ITEM.fullmatch(item)
        if match is None:
            return None
        part = ' '.join(match['part'].split()).lower()
        if not any(ch.isalpha() for ch in part):
            return None
        order[part] = order.get(part, 0) + int(match['qty'])
        if not 1 <= order[part] <= MAX_QUANTITY:
            return None
    return order or None


def parse_model(text):
    """
    Splits 'Brand Model name' into a (brand, model) tuple.
    Any run of whitespace (spaces, tabs) separates the words.
    Returns None if text is not a string, has fewer than two words,
    or the brand contains no letters.
    """
    if not isinstance(text, str):
        return None
    words = text.split()
    if len(words) < 2 or not any(ch.isalpha() for ch in words[0]):
        return None
    return words[0].title(), ' '.join(words[1:])


def ask(prompt):
    """input() that treats a closed input stream (Ctrl-D, empty pipe) as a blank answer."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return ''


def main():
    print("==== Running mask_imei ====")
    value = ask("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    result = mask_imei(value)
    print("Masked IMEI:", result if result is not None else "invalid, an IMEI must be 15 digits")

    print("\n==== Running parse_parts_order ====")
    value = ask("Enter parts and quantities as PART xQTY separated by ; (e.g. screen x1; battery x2): ")
    result = parse_parts_order(value)
    print("Parts order:", result if result is not None
          else f"invalid, use PART xQTY with a quantity from 1 to {MAX_QUANTITY}")

    print("\n==== Running parse_model ====")
    value = ask("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    result = parse_model(value)
    print("Brand and model:", result if result is not None
          else "invalid, enter a brand followed by a model")


if __name__ == "__main__":
    main()
