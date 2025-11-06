
from typing import Optional
from .models import CalculationRules, CalculationResult, ExtractedData

def _safe(v: Optional[float]) -> float:
    return float(v) if v is not None else 0.0

def compute_net(ex: ExtractedData, rules: CalculationRules) -> CalculationResult:
    warnings = []

    gross = ex.gross
    payout = ex.payout
    commission = ex.commission

    if gross is None and payout is not None and commission is not None:
        gross = payout + commission

    if gross is None and payout is not None and commission is None and rules.booking_commission_pct > 0:
        gross = payout / (1.0 - rules.booking_commission_pct)

    if gross is None:
        warnings.append("Gross mancante: calcolo parziale.")
        gross = 0.0

    computed_commission = commission if commission is not None else gross * rules.booking_commission_pct
    iva_amount = gross * rules.iva_pct if rules.iva_pct > 0 else 0.0

    nights = ex.nights or 0
    guests = ex.guests or 0
    city_tax_total = rules.city_tax_per_person_per_night * nights * guests if rules.city_tax_per_person_per_night > 0 else 0.0

    fixed_costs_total = rules.cleaning_fee_fixed + rules.other_fixed_costs
    net_total = gross - computed_commission - iva_amount - city_tax_total - fixed_costs_total

    details = {
        "gross": round(gross, 2),
        "commission_input": ex.commission,
        "commission_pct": rules.booking_commission_pct,
        "iva_pct": rules.iva_pct,
        "withholding_tax_pct": rules.withholding_tax_pct,
        "nights": nights,
        "guests": guests,
        "city_tax_per_person_per_night": rules.city_tax_per_person_per_night,
        "cleaning_fee_fixed": rules.cleaning_fee_fixed,
        "other_fixed_costs": rules.other_fixed_costs,
        "payout_input": ex.payout,
    }

    return CalculationResult(
        currency=rules.currency,
        gross_total=round(gross, 2),
        computed_commission=round(computed_commission, 2),
        iva_amount=round(iva_amount, 2),
        city_tax_total=round(city_tax_total, 2),
        fixed_costs_total=round(fixed_costs_total, 2),
        net_total=round(net_total, 2),
        details=details,
        warnings=warnings
    )
