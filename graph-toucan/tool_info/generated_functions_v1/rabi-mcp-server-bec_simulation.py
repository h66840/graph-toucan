from typing import Dict, List, Any, Optional
import math
import time
from dataclasses import dataclass

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching BEC simulation data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Simulation success status
        - result_type (str): Type of result, e.g., "bec_simulation"
        - ground_state_chemical_potential_j (float): Chemical potential in joules
        - ground_state_total_energy_j (float): Total energy in joules
        - ground_state_kinetic_energy_j (float): Kinetic energy in joules
        - ground_state_interaction_energy_j (float): Interaction energy in joules
        - ground_state_particle_number (int): Number of particles in ground state
        - characteristic_oscillator_length_m (float): Oscillator length in meters
        - characteristic_thomas_fermi_radius_m (float): Thomas-Fermi radius in meters
        - characteristic_healing_length_m (float): Healing length in meters
        - characteristic_scattering_length_m (float): Scattering length in meters
        - density_positions_0 (float): First position in density profile (m)
        - density_positions_1 (float): Second position in density profile (m)
        - density_density_per_m_0 (float): Linear density at first position
        - density_density_per_m_1 (float): Linear density at second position
        - density_peak_density (float): Maximum density value
        - parameters_particle_number (int): Input particle number
        - parameters_scattering_length_a0 (float): Scattering length in Bohr radii
        - parameters_trap_frequency_hz (float): Trap frequency in Hz
        - parameters_interaction_strength (float): Interaction strength parameter
        - analysis_interaction_regime (str): Interaction regime (e.g., "strong")
        - analysis_thomas_fermi_parameter (float): Thomas-Fermi parameter
        - analysis_quantum_depletion (float): Quantum depletion fraction
        - analysis_condensate_fraction (float): Condensate fraction
        - computation_time_seconds (float): Computation time in seconds
        - real_physics_calculation (bool): Whether real physics calculation was performed
    """
    return {
        "success": True,
        "result_type": "bec_simulation",
        "ground_state_chemical_potential_j": 1.23e-22,
        "ground_state_total_energy_j": 4.56e-22,
        "ground_state_kinetic_energy_j": 7.89e-23,
        "ground_state_interaction_energy_j": 3.77e-22,
        "ground_state_particle_number": 10000,
        "characteristic_oscillator_length_m": 1.41e-6,
        "characteristic_thomas_fermi_radius_m": 5.67e-6,
        "characteristic_healing_length_m": 2.34e-7,
        "characteristic_scattering_length_m": 5.29e-9,
        "density_positions_0": -1.0e-5,
        "density_positions_1": 1.0e-5,
        "density_density_per_m_0": 8.5e+13,
        "density_density_per_m_1": 8.5e+13,
        "density_peak_density": 9.2e+13,
        "parameters_particle_number": 10000,
        "parameters_scattering_length_a0": 100.0,
        "parameters_trap_frequency_hz": 100.0,
        "parameters_interaction_strength": 0.015,
        "analysis_interaction_regime": "strong",
        "analysis_thomas_fermi_parameter": 24.1,
        "analysis_quantum_depletion": 0.023,
        "analysis_condensate_fraction": 0.977,
        "computation_time_seconds": 0.15,
        "real_physics_calculation": True
    }

def rabi_mcp_server_bec_simulation(
    particle_number: int,
    scattering_length: float,
    trap_frequency: Optional[float] = 100.0
) -> Dict[str, Any]:
    """
    Simulate Bose-Einstein condensate dynamics using Gross-Pitaevskii equation.
    
    This function models the ground state properties of a BEC in a harmonic trap
    using physical parameters and returns characteristic properties, energy components,
    density profiles, and analysis metrics.
    
    Args:
        particle_number (int): Number of particles in the condensate (required)
        scattering_length (float): Scattering length in nanometers (required)
        trap_frequency (float, optional): Trap frequency in Hz (default: 100.0 Hz)
    
    Returns:
        Dict containing simulation results with the following structure:
        - success (bool): Whether simulation completed successfully
        - result_type (str): Type of result ("bec_simulation")
        - ground_state_properties (Dict): Energy and particle properties in ground state
        - characteristic_lengths (Dict): Key length scales in meters
        - density_profile (Dict): Spatial density distribution
        - parameters (Dict): Input parameters used in simulation
        - analysis (Dict): Derived analysis metrics
        - computation_time_seconds (float): Time taken for computation
        - real_physics_calculation (bool): Whether real physics was computed
    
    Raises:
        ValueError: If particle_number <= 0, scattering_length <= 0, or trap_frequency <= 0
    """
    # Input validation
    if particle_number <= 0:
        raise ValueError("particle_number must be positive")
    if scattering_length <= 0:
        raise ValueError("scattering_length must be positive")
    if trap_frequency is not None and trap_frequency <= 0:
        raise ValueError("trap_frequency must be positive")
    
    # Set default trap frequency if not provided
    if trap_frequency is None:
        trap_frequency = 100.0
    
    # Start timer
    start_time = time.time()
    
    # Constants
    hbar = 1.0545718e-34  # J·s
    m_rubidium = 1.443e-25  # kg (for Rb-87)
    a0 = 5.29177210903e-11  # Bohr radius in meters
    
    # Convert scattering length to meters and a0 units
    scattering_length_m = scattering_length * 1e-9
    scattering_length_a0 = scattering_length_m / a0
    
    # Calculate oscillator length
    omega = 2 * math.pi * trap_frequency
    oscillator_length = math.sqrt(hbar / (m_rubidium * omega))
    
    # Calculate interaction strength
    a_s = scattering_length_m
    interaction_strength = (4 * math.pi * hbar**2 * a_s * particle_number) / m_rubidium
    
    # Thomas-Fermi approximation
    if particle_number * scattering_length_a0 * (omega / (2 * math.pi))**(-2/3) > 1:
        regime = "strong"
    else:
        regime = "weak"
    
    # Thomas-Fermi radius
    tf_radius = (15 * particle_number * a_s / oscillator_length)**(1/5) * oscillator_length
    
    # Chemical potential (Thomas-Fermi approximation)
    mu = hbar * omega * (15 * particle_number * a_s / oscillator_length)**(2/5)
    
    # Total energy (TF approximation)
    total_energy = (2/7) * mu * particle_number
    
    # Kinetic energy estimate
    kinetic_energy = total_energy * 0.15
    
    # Interaction energy
    interaction_energy = total_energy - kinetic_energy
    
    # Healing length
    n_peak = (15 * particle_number) / (8 * math.pi * tf_radius**3)
    healing_length = math.sqrt(hbar**2 / (2 * m_rubidium * interaction_energy / particle_number))
    
    # Quantum depletion (Bogoliubov theory)
    quantum_depletion = (8 / (3 * math.sqrt(math.pi))) * (n_peak * a_s**3)**(1/2)
    condensate_fraction = max(0.0, 1.0 - quantum_depletion)
    
    # Thomas-Fermi parameter
    tf_parameter = tf_radius / healing_length
    
    # Density profile (parabolic TF profile)
    num_points = 2
    positions = [-1.0e-5, 1.0e-5]  # Two points for simplicity
    density_per_m = []
    peak_density = (15 * particle_number) / (8 * math.pi * tf_radius**3)
    
    for x in positions:
        r = abs(x)
        if r < tf_radius:
            n = peak_density * (1 - (r/tf_radius)**2)
        else:
            n = 0.0
        density_per_m.append(n)
    
    # Computation time
    computation_time = time.time() - start_time
    
    # Construct result dictionary
    result = {
        "success": True,
        "result_type": "bec_simulation",
        "ground_state_properties": {
            "chemical_potential_j": float(mu),
            "total_energy_j": float(total_energy),
            "kinetic_energy_j": float(kinetic_energy),
            "interaction_energy_j": float(interaction_energy),
            "particle_number": particle_number
        },
        "characteristic_lengths": {
            "oscillator_length_m": float(oscillator_length),
            "thomas_fermi_radius_m": float(tf_radius),
            "healing_length_m": float(healing_length),
            "scattering_length_m": float(scattering_length_m)
        },
        "density_profile": {
            "positions_m": positions,
            "density_per_m": density_per_m,
            "peak_density": float(peak_density)
        },
        "parameters": {
            "particle_number": particle_number,
            "scattering_length_a0": float(scattering_length_a0),
            "trap_frequency_hz": float(trap_frequency),
            "interaction_strength": float(interaction_strength)
        },
        "analysis": {
            "interaction_regime": regime,
            "thomas_fermi_parameter": float(tf_parameter),
            "quantum_depletion": float(quantum_depletion),
            "condensate_fraction": float(condensate_fraction)
        },
        "computation_time_seconds": computation_time,
        "real_physics_calculation": True
    }
    
    return result