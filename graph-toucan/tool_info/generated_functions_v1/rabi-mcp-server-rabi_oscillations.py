from typing import Dict, List, Any, Optional
import numpy as np
import time
from math import pi, sin, cos, floor


def rabi_mcp_server_rabi_oscillations(
    max_time: float,
    rabi_frequency: float,
    time_points: Optional[int] = 1000
) -> Dict[str, Any]:
    """
    Calculate Rabi oscillations for a two-level quantum system.
    
    This function simulates the time evolution of a two-level quantum system under resonant driving,
    computing the population dynamics in the ground and excited states based on the Rabi model.
    
    Args:
        max_time (float): Maximum evolution time in seconds.
        rabi_frequency (float): Rabi frequency in Hz (cycles per second).
        time_points (int, optional): Number of time points to evaluate. Defaults to 1000.
        
    Returns:
        Dict[str, Any]: A dictionary containing simulation results with the following keys:
            - success (bool): Whether the calculation was successful.
            - result_type (str): Type of result, always "rabi_oscillations".
            - times (List[float]): Time points in seconds.
            - excited_population (List[float]): Population in excited state at each time point.
            - ground_population (List[float]): Population in ground state at each time point.
            - parameters (Dict): Input parameters used in simulation.
            - oscillation_properties (Dict): Theoretical and measured oscillation characteristics.
            - analysis (Dict): Summary analysis of oscillation behavior.
            - computation_time_seconds (float): Time taken for computation.
            - real_physics_calculation (bool): Whether a real physical simulation was performed.
    """
    start_time = time.time()
    
    # Input validation
    if max_time <= 0:
        return {
            "success": False,
            "error": "max_time must be positive"
        }
    
    if rabi_frequency <= 0:
        return {
            "success": False,
            "error": "rabi_frequency must be positive"
        }
    
    if time_points is None:
        time_points = 1000
    elif time_points < 2:
        return {
            "success": False,
            "error": "time_points must be at least 2"
        }
    
    try:
        # Convert Rabi frequency to angular frequency (rad/s)
        rabi_frequency_rad_per_s = 2 * pi * rabi_frequency
        
        # Generate time array
        times = np.linspace(0, max_time, time_points)
        
        # Calculate populations
        # For resonant driving and starting from |g>, excited state population is sin²(Ωt/2)
        excited_population = [float(sin(rabi_frequency_rad_per_s * t / 2) ** 2) for t in times]
        ground_population = [1.0 - pop for pop in excited_population]
        
        # Theoretical properties
        theoretical_rabi_period_s = 1.0 / rabi_frequency
        theoretical_frequency_hz = rabi_frequency
        
        # Find peaks (maximum population transfer times)
        peak_times = []
        for i in range(1, len(excited_population) - 1):
            if excited_population[i] > excited_population[i-1] and excited_population[i] > excited_population[i+1]:
                peak_times.append(float(times[i]))
        
        # Measure period from peaks if available
        measured_period_s = None
        measured_frequency_hz = None
        if len(peak_times) >= 2:
            periods = [peak_times[i+1] - peak_times[i] for i in range(len(peak_times)-1)]
            measured_period_s = float(sum(periods) / len(periods))
            measured_frequency_hz = 1.0 / measured_period_s if measured_period_s > 0 else 0.0
        
        # Analysis
        max_population_transfer = max(excited_population)
        number_of_oscillations = max_time / theoretical_rabi_period_s
        perfect_oscillations = abs(max_population_transfer - 1.0) < 1e-10
        
        # Prepare output
        result = {
            "success": True,
            "result_type": "rabi_oscillations",
            "times": [float(t) for t in times],
            "excited_population": excited_population,
            "ground_population": ground_population,
            "parameters": {
                "rabi_frequency_rad_per_s": rabi_frequency_rad_per_s,
                "max_time_s": max_time,
                "time_points": time_points
            },
            "oscillation_properties": {
                "theoretical_rabi_period_s": theoretical_rabi_period_s,
                "theoretical_frequency_hz": theoretical_frequency_hz,
                "measured_period_s": measured_period_s,
                "measured_frequency_hz": measured_frequency_hz,
                "peak_times": peak_times
            },
            "analysis": {
                "number_of_oscillations": number_of_oscillations,
                "maximum_population_transfer": max_population_transfer,
                "perfect_oscillations": perfect_oscillations
            },
            "computation_time_seconds": time.time() - start_time,
            "real_physics_calculation": True
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }