
from app.extractors.pdf_fallback import _norm_number

def test_norm_number_variants():
    assert _norm_number("1.234,56") == 1234.56
    assert _norm_number("1,234.56") == 1234.56
    assert _norm_number("1234,56") == 1234.56
    assert _norm_number("1.234") == 1234.0
