def cooking_units_converter_convert_temperature(from_unit: str, to_unit: str, value: float) -> dict:
    """
    Convert between Celsius (C) and Fahrenheit (F) temperatures.
    
    Parameters:
        from_unit (str): Source temperature unit, either "C" for Celsius or "F" for Fahrenheit
        to_unit (str): Target temperature unit, either "C" for Celsius or "F" for Fahrenheit
        value (float): The temperature value to convert
    
    Returns:
        dict: A dictionary containing the converted temperature value and unit information
              - value (float): The converted temperature
              - from_unit (str): The source temperature unit ("C" or "F")
              - to_unit (str): The target temperature unit ("C" or "F")
    
    Raises:
        ValueError: If from_unit or to_unit is not "C" or "F"
        TypeError: If value is not a number
    """
    # Input validation
    if not isinstance(value, (int, float)):
        raise TypeError("Value must be a number")
    
    if from_unit not in ["C", "F"]:
        raise ValueError("from_unit must be 'C' or 'F'")
    
    if to_unit not in ["C", "F"]:
        raise ValueError("to_unit must be 'C' or 'F'")
    
    # Conversion logic
    if from_unit == to_unit:
        converted_value = value
    elif from_unit == "C" and to_unit == "F":
        converted_value = (value * 9/5) + 32
    else:  # from_unit == "F" and to_unit == "C"
        converted_value = (value - 32) * 5/9
    
    return {
        "value": float(converted_value),
        "from_unit": from_unit,
        "to_unit": to_unit
    }