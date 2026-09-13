from decimal import Decimal, getcontext

from app.services.calculations import calculate_invoice, format_money


def test_calculates_line_subtotal_tax_and_total() -> None:
    totals = calculate_invoice([(Decimal("2"), Decimal("19.99")), (Decimal("1"), Decimal("10.00"))])

    assert [item.line_total_cents for item in totals.items] == [3998, 1000]
    assert totals.subtotal_cents == 4998
    assert totals.tax_cents == 750
    assert totals.total_cents == 5748
    assert format_money(totals.total_cents) == "57.48"


def test_rounds_half_up_and_allows_zero_price() -> None:
    totals = calculate_invoice([(Decimal("2.5"), Decimal("2.93")), (Decimal("1"), Decimal("0"))])

    assert totals.items[0].line_total_cents == 733
    assert totals.items[1].line_total_cents == 0
    assert totals.tax_cents == 110


def test_calculation_does_not_depend_on_global_decimal_context() -> None:
    original_precision = getcontext().prec
    getcontext().prec = 6
    try:
        totals = calculate_invoice([(Decimal("1"), Decimal("19.99"))])
    finally:
        getcontext().prec = original_precision

    assert totals.total_cents == 2299
