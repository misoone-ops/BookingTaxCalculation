
from app.models import ExtractedData, CalculationRules
from app.calculator import compute_net

def test_compute_net_basic():
    ex = ExtractedData(
        source="test",
        gross=1000.0,
        commission=None,
        payout=None,
        nights=3,
        guests=2,
        raw={},
    )
    rules = CalculationRules(
        currency="EUR",
        booking_commission_pct=0.15,
        iva_pct=0.10,
        cleaning_fee_fixed=10.0,
        city_tax_per_person_per_night=2.0
    )
    calc = compute_net(ex, rules)
    assert round(calc.gross_total,2) == 1000.00
    assert round(calc.computed_commission,2) == 150.00
    assert round(calc.iva_amount,2) == 100.00
    assert round(calc.city_tax_total,2) == 12.00
    assert round(calc.fixed_costs_total,2) == 10.00
    assert round(calc.net_total,2) == 728.00
