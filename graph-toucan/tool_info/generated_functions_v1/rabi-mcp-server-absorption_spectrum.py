from typing import Dict, List, Any, Optional
import math
from datetime import datetime

def rabi_mcp_server_absorption_spectrum(linewidth: float, transition_frequency: float, temperature: Optional[float] = None) -> Dict[str, Any]:
    """
    Calculate absorption spectrum with various broadening mechanisms.
    
    Args:
        linewidth (float): Natural linewidth in rad/s
        transition_frequency (float): Transition frequency in rad/s
        temperature (float, optional): Temperature in Kelvin. If not provided, Doppler broadening is ignored.
    
    Returns:
        Dict containing:
        - spectrum_data (List[Dict]): List of frequency-intensity pairs with 'frequency' (rad/s) and 'intensity'
        - fwhm (float): Full width at half maximum of the main peak in rad/s
        - broadening_components (Dict): Breakdown of broadening contributions ('natural', 'doppler', 'total_effective')
        - peak_frequency (float): Frequency at maximum absorption in rad/s
        - metadata (Dict): Computation details including timestamp, temperature, and input transition frequency
    """
    if linewidth <= 0:
        raise ValueError("Linewidth must be positive")
    if transition_frequency <= 0:
        raise ValueError("Transition frequency must be positive")
    if temperature is not None and temperature < 0:
        raise ValueError("Temperature cannot be negative")
    
    # Set default temperature if not provided
    temp_k = temperature if temperature is not None else 0.0
    
    # Physical constants
    c = 299792458  # speed of light in m/s
    k_B = 1.380649e-23  # Boltzmann constant in J/K
    m = 85 * 1.660539e-27  # Approximate atomic mass (e.g., Rb-85) in kg
    
    # Natural broadening (FWHM)
    natural_fwhm = linewidth
    
    # Doppler broadening (FWHM) - only if temperature > 0
    doppler_fwhm = 0.0
    if temp_k > 0:
        nu_0 = transition_frequency / (2 * math.pi)  # Convert to Hz
        doppler_sigma_nu = nu_0 / c * math.sqrt(2 * k_B * temp_k / m)
        doppler_fwhm = 2 * math.sqrt(2 * math.log(2)) * doppler_sigma_nu * 2 * math.pi  # Convert to rad/s
    else:
        doppler_fwhm = 0.0
    
    # Total effective broadening (quadratic sum)
    total_effective_fwhm = math.sqrt(natural_fwhm**2 + doppler_fwhm**2)
    
    # Create spectrum around transition frequency
    # Use 5 times FWHM as range, with 200 points
    fwhm_range = 5 * total_effective_fwhm
    num_points = 200
    frequency_step = 2 * fwhm_range / num_points
    
    spectrum_data = []
    
    for i in range(num_points):
        freq = transition_frequency - fwhm_range + i * frequency_step
        
        # Calculate intensity using Voigt profile approximation (Lorentzian + Gaussian)
        lorentzian_factor = natural_fwhm / ((freq - transition_frequency)**2 + natural_fwhm**2)
        
        gaussian_factor = 1.0
        if temp_k > 0:
            sigma = doppler_fwhm / (2 * math.sqrt(2 * math.log(2)))
            gaussian_factor = math.exp(-0.5 * ((freq - transition_frequency) / sigma)**2)
        
        # Combined profile (approximate Voigt as product)
        intensity = lorentzian_factor * gaussian_factor
        spectrum_data.append({
            'frequency': freq,
            'intensity': intensity
        })
    
    # Find peak frequency (should be very close to transition_frequency)
    max_intensity = max(point['intensity'] for point in spectrum_data)
    peak_point = next(point for point in spectrum_data if point['intensity'] == max_intensity)
    peak_freq = peak_point['frequency']
    
    # Prepare metadata
    metadata = {
        'calculation_timestamp': datetime.utcnow().isoformat() + 'Z',
        'temperature_K': temp_k,
        'transition_frequency_input': transition_frequency
    }
    
    # Prepare broadening components
    broadening_components = {
        'natural': natural_fwhm,
    }
    
    if temp_k > 0:
        broadening_components['doppler'] = doppler_fwhm
    
    broadening_components['total_effective'] = total_effective_fwhm
    
    return {
        'spectrum_data': spectrum_data,
        'fwhm': total_effective_fwhm,
        'broadening_components': broadening_components,
        'peak_frequency': peak_freq,
        'metadata': metadata
    }