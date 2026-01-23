def cooking_units_converter_convert_volume(from_unit: str, to_unit: str, value: float) -> dict:
    """
    Convert between volume units (ml, l, cup, tbsp, tsp).
    
    Parameters:
        from_unit (str): Source volume unit. Must be one of: ml, l, cup, tbsp, tsp.
        to_unit (str): Target volume unit. Must be one of: ml, l, cup, tbsp, tsp.
        value (float): The volume value to convert.
        
    Returns:
        dict: A dictionary containing the converted value, source unit, and target unit.
              - value (float): Converted volume value rounded to three decimal places.
              - from_unit (str): Source volume unit.
              - to_unit (str): Target volume unit.
              
    Raises:
        ValueError: If invalid units are provided or if value is negative.
    """
    # Define conversion factors to milliliters (ml)
    to_ml = {
        'ml': 1,
        'l': 1000,
        'cup': 240,      # 1 US cup = 240 ml
        'tbsp': 15,      # 1 US tablespoon = 15 ml
        'tsp': 5         # 1 US teaspoon = 5 ml
    }
    
    # Validate inputs
    if from_unit not in to_ml:
        raise ValueError(f"Invalid source unit: {from_unit}. Use one of: ml, l, cup, tbsp, tsp")
    if to_unit not in to_ml:
        raise ValueError(f"Invalid target unit: {to_unit}. Use one of: ml, l, cup, tbsp, tsp")
    if value < 0:
        raise ValueError("Volume value must be non-negative")
    
    # Convert to ml first
    value_in_ml = value * to_ml[from_unit]
    
    # Convert from ml to target unit
    converted_value = value_in_ml / to_ml[to_unit]
    
    # Round to three decimal places
    converted_value = round(converted_value, 3)
    
    return {
        "value": converted_value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }