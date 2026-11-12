# Lab 7: Fuzzing for Input Validation Bugs
# Kshitij Gupta | PES1UG24AM915 | Section F

from hypothesis import given, settings, strategies as st
from phone_repair_quote_parser import mask_imei, parse_parts_order, parse_model

# Purely random text almost never looks like an IMEI, a parts order or a phone
# model, so it rarely gets past the first line of each function. Each test also
# mixes in "near-valid" text built only from characters that real inputs use,
# which drives Hypothesis into the actual parsing logic.
IMEI_LIKE = st.text(alphabet="0123456789- ", max_size=25)
ORDER_LIKE = st.text(alphabet="abcenorstxyX 0123456789-;", max_size=40)
MODEL_LIKE = st.text(alphabet="SAGamsunglxype 0123\t", max_size=30)


@settings(max_examples=500)
@given(st.text() | st.none() | IMEI_LIKE)
def test_mask_imei_no_crash(s):
    try:
        result = mask_imei(s)
    except Exception as e:
        assert False, f"mask_imei crashed on {s!r} with {type(e).__name__}: {e}"

    # Invalid input must be rejected with None, not "masked" into something
    # that still leaks the number or looks like a real masked IMEI.
    if result is not None:
        assert isinstance(result, str), f"mask_imei({s!r}) returned {result!r}"
        visible = result.lstrip("*")
        assert len(result) > 4, f"mask_imei({s!r}) returned {result!r}: nothing is hidden"
        assert len(visible) == 4 and visible.isdigit(), (
            f"mask_imei({s!r}) returned {result!r}: must show exactly the last 4 digits"
        )


@settings(max_examples=500)
@given(st.text() | st.none() | ORDER_LIKE)
def test_parse_parts_order_no_crash(s):
    try:
        result = parse_parts_order(s)
    except Exception as e:
        assert False, f"parse_parts_order crashed on {s!r} with {type(e).__name__}: {e}"

    # A returned order must contain at least one part, and every quantity
    # must be a whole number of at least 1.
    if result is not None:
        assert isinstance(result, dict) and result, (
            f"parse_parts_order({s!r}) returned {result!r}: expected a non-empty dict"
        )
        for part, qty in result.items():
            assert isinstance(part, str) and part and part == part.strip(), (
                f"parse_parts_order({s!r}) returned bad part name {part!r}"
            )
            assert isinstance(qty, int) and qty >= 1, (
                f"parse_parts_order({s!r}) returned quantity {qty!r} for {part!r}"
            )


@settings(max_examples=500)
@given(st.text() | st.none() | MODEL_LIKE)
def test_parse_model_no_crash(s):
    try:
        result = parse_model(s)
    except Exception as e:
        assert False, f"parse_model crashed on {s!r} with {type(e).__name__}: {e}"

    # A returned result must be a (brand, model) pair of non-empty, trimmed strings.
    if result is not None:
        assert isinstance(result, tuple) and len(result) == 2, (
            f"parse_model({s!r}) returned {result!r}: expected a (brand, model) tuple"
        )
        brand, model = result
        assert isinstance(brand, str) and brand and brand == brand.strip(), (
            f"parse_model({s!r}) returned bad brand {brand!r}"
        )
        assert isinstance(model, str) and model and model == model.strip(), (
            f"parse_model({s!r}) returned bad model {model!r}"
        )
