from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
TAX_RATE = Decimal("0.15")
THOUSAND = Decimal("1000")
HUNDRED = Decimal("100")


@dataclass(frozen=True)
class CalculatedItem:
    quantity_millis: int
    unit_price_cents: int
    line_total_cents: int


@dataclass(frozen=True)
class InvoiceTotals:
    items: list[CalculatedItem]
    subtotal_cents: int
    tax_cents: int
    total_cents: int


def money_to_cents(value: Decimal) -> int:
    return int(value.quantize(CENT, rounding=ROUND_HALF_UP) * HUNDRED)


def cents_to_money(value: int) -> Decimal:
    return (Decimal(value) / HUNDRED).quantize(CENT, rounding=ROUND_HALF_UP)


def format_money(cents: int) -> str:
    return f"{cents_to_money(cents):.2f}"


def quantity_to_millis(value: Decimal) -> int:
    return int((value * THOUSAND).to_integral_exact())


def format_quantity(millis: int) -> str:
    value = Decimal(millis) / THOUSAND
    return format(value.normalize(), "f") if value % 1 else str(int(value))


def calculate_invoice(items: list[tuple[Decimal, Decimal]]) -> InvoiceTotals:
    calculated_items: list[CalculatedItem] = []
    for quantity, unit_price in items:
        line_total = (quantity * unit_price).quantize(CENT, rounding=ROUND_HALF_UP)
        calculated_items.append(
            CalculatedItem(
                quantity_millis=quantity_to_millis(quantity),
                unit_price_cents=money_to_cents(unit_price),
                line_total_cents=money_to_cents(line_total),
            )
        )
    subtotal_cents = sum(item.line_total_cents for item in calculated_items)
    tax_cents = money_to_cents(cents_to_money(subtotal_cents) * TAX_RATE)
    return InvoiceTotals(
        items=calculated_items,
        subtotal_cents=subtotal_cents,
        tax_cents=tax_cents,
        total_cents=subtotal_cents + tax_cents,
    )
