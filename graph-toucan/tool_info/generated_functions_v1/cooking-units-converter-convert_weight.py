def cooking_units_converter_convert_weight(from_unit: str, to_unit: str, value: float) -> dict:
    """
    Convert between weight units (g, kg, oz, lb).
    
    Parameters:
        from_unit (str): Source weight unit. Must be one of 'g', 'kg', 'oz', 'lb'.
        to_unit (str): Target weight unit. Must be one of 'g', 'kg', 'oz', 'lb'.
        value (float): The numerical value to convert.
    
    Returns:
        dict: A dictionary containing the converted value and unit information.
              Keys: 'value' (float), 'from_unit' (str), 'to_unit' (str)
    
    Raises:
        ValueError: If invalid units are provided or if value is not a number.
    """
    # Define conversion factors to grams
    to_grams = {
        'g': 1.0,
        'kg': 1000.0,
        'oz': 28.3495,
        'lb': 453.592
    }
    
    # Validate inputs
    if from_unit not in to_grams:
        raise ValueError(f"Invalid source unit '{from_unit}'. Must be one of {list(to_grams.keys())}")
    if to_unit not in to_grams:
        raise ValueError(f"Invalid target unit '{to_unit}'. Must be one of {list(to_grams.keys())}")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("Value must be a number")
    
    # Convert to grams first
    value_in_grams = value * to_grams[from_unit]
    
    # Convert from grams to target unit
    converted_value = value_in_grams / to_grams[to_unit]
    
    return {
        'value': float(converted_value),
        'from_unit': from_unit,
        'to_unit': to_unit
    }