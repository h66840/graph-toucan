from typing import Dict, List, Any
import math
import cmath

def rabi_mcp_server_simulate_two_level_atom(detuning: float, evolution_time: float, rabi_frequency: float) -> Dict[str, Any]:
    """
    Simulate dynamics of a two-level atom in an electromagnetic field using Rabi oscillation model.
    
    The simulation computes the time evolution of a two-level quantum system under a driving field
    characterized by a given Rabi frequency and detuning from resonance. The solution is based on
    analytical expressions for the state vector and populations.
    
    Parameters:
        detuning (float): Detuning from resonance in Hz
        evolution_time (float): Total evolution time in seconds
        rabi_frequency (float): Rabi frequency in Hz (coupling strength between levels)
    
    Returns:
        Dict containing:
            - population_in_excited_state (float): Final excited state population
            - population_in_ground_state (float): Final ground state population
            - rabi_oscillations (List[Dict]): Time-series of populations and phase
            - coherence (float): Magnitude of coherence at final time
            - total_evolution_time (float): Echo of input evolution time
            - detuning_used (float): Echo of input detuning
            - rabi_frequency_used (float): Echo of input Rabi frequency
            - final_state_vector (List[complex]): Final quantum state [ground, excited]
    """
    # Input validation
    if evolution_time < 0:
        raise ValueError("Evolution time must be non-negative")
    if rabi_frequency < 0:
        raise ValueError("Rabi frequency must be non-negative")
    
    # Effective Rabi frequency (generalized)
    omega_eff = math.sqrt(rabi_frequency**2 + detuning**2)
    
    # Final time state calculations
    cos_omega_eff_t = math.cos(omega_eff * evolution_time / 2)
    sin_omega_eff_t = math.sin(omega_eff * evolution_time / 2)
    
    # Ground state amplitude
    c_g = complex(cos_omega_eff_t, detuning / omega_eff * sin_omega_eff_t)
    # Excited state amplitude
    c_e = complex(-1j * rabi_frequency / omega_eff * sin_omega_eff_t, 0)
    
    # Final populations
    pop_excited = abs(c_e)**2
    pop_ground = abs(c_g)**2
    
    # Coherence magnitude (off-diagonal element of density matrix)
    coherence = abs(c_g * c_e.conjugate())
    
    # Time series data
    num_points = 100
    rabi_oscillations = []
    
    for i in range(num_points + 1):
        t = evolution_time * i / num_points
        cos_omega_eff_t_step = math.cos(omega_eff * t / 2)
        sin_omega_eff_t_step = math.sin(omega_eff * t / 2)
        
        c_g_step = complex(cos_omega_eff_t_step, detuning / omega_eff * sin_omega_eff_t_step)
        c_e_step = complex(-1j * rabi_frequency / omega_eff * sin_omega_eff_t_step, 0)
        
        ground_pop = abs(c_g_step)**2
        excited_pop = abs(c_e_step)**2
        
        # Phase difference between excited and ground state
        if abs(c_g_step) > 1e-10 and abs(c_e_step) > 1e-10:
            phase_diff = cmath.phase(c_e_step) - cmath.phase(c_g_step)
        else:
            phase_diff = 0.0
            
        rabi_oscillations.append({
            "time": round(t, 12),
            "ground_population": round(ground_pop, 12),
            "excited_population": round(excited_pop, 12),
            "phase": round(phase_diff, 12)
        })
    
    # Final state vector (normalized)
    final_state_vector = [complex(round(c_g.real, 12), round(c_g.imag, 12)), 
                         complex(round(c_e.real, 12), round(c_e.imag, 12))]
    
    # Ensure populations sum to 1 (within numerical precision)
    total_pop = pop_ground + pop_excited
    if abs(total_pop - 1.0) > 1e-10:
        # Renormalize if needed
        pop_ground = pop_ground / total_pop
        pop_excited = pop_excited / total_pop
    
    return {
        "population_in_excited_state": round(pop_excited, 12),
        "population_in_ground_state": round(pop_ground, 12),
        "rabi_oscillations": rabi_oscillations,
        "coherence": round(coherence, 12),
        "total_evolution_time": evolution_time,
        "detuning_used": detuning,
        "rabi_frequency_used": rabi_frequency,
        "final_state_vector": final_state_vector
    }