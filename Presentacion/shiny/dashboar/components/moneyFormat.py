
def money_format(value):
    """
    Convierte un valor numérico a un formato legible en millones (M) o billones (B),
    con estilo de moneda colombiano.
    """
    if value >= 1_000_000_000:
        formatted_number = f"${value / 1_000_000_000:,.2f} B"  # Billones
    elif value >= 1_000_000:
        formatted_number = f"${value / 1_000_000:,.2f} M"  # Millones
    else:
        formatted_number = f"${value:,.2f}"

    # Reemplazar comas y puntos al estilo colombiano
    formatted_number = formatted_number.replace(",", "_").replace(".", ",").replace("_", ".")
    return formatted_number
