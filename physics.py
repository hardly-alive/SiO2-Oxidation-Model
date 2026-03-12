import math

# --- Physical Constants ---
KB = 8.617e-5  # Boltzmann constant in eV/K

# Standard Deal-Grove parameters for <100> Silicon
# Using activation energies specified in the prompt.
OXIDATION_PARAMS = {
    "dry": {
        "Ea_B": 1.24,       # eV
        "Ea_BA": 2.00,      # eV
        "B_0": 772.0,       # um^2/hr (Pre-exponential for Parabolic)
        "BA_0": 6.23e6,     # um/hr (Pre-exponential for Linear)
    },
    "wet": {
        "Ea_B": 0.78,       # eV
        "Ea_BA": 2.05,      # eV
        "B_0": 386.0,       # um^2/hr
        "BA_0": 1.63e8,     # um/hr
    }
}

def compute_rate_constants(temp_c: float, pressure_atm: float, ox_type: str = "dry") -> tuple[float, float, float]:
    """
    Computes the Deal-Grove rate constants B, B/A, and A based on temperature and pressure.
    Returns: B (um^2/hr), BA (um/hr), A (um)
    """
    if ox_type not in OXIDATION_PARAMS:
        raise ValueError("ox_type must be 'dry' or 'wet'")
        
    params = OXIDATION_PARAMS[ox_type]
    temp_k = temp_c + 273.15  # Convert Celsius to Kelvin
    
    # Arrhenius temperature dependence
    B_atm = params["B_0"] * math.exp(-params["Ea_B"] / (KB * temp_k))
    BA_atm = params["BA_0"] * math.exp(-params["Ea_BA"] / (KB * temp_k))
    
    # Pressure scaling (linear according to prompt)
    B = B_atm * pressure_atm
    BA = BA_atm * pressure_atm
    
    # Compute A (um)
    A = B / BA if BA != 0 else 0.0
    
    return B, BA, A

def compute_thickness(time_hr: float, temp_c: float, pressure_atm: float, ox_type: str = "dry", initial_thickness_nm: float = 0.0) -> float:
    """
    Computes the oxide thickness using the Deal-Grove model.
    Takes time in hours, returns thickness in nanometers (nm).
    """
    # 1. Get constants
    B, BA, A = compute_rate_constants(temp_c, pressure_atm, ox_type)
    
    # 2. Convert initial thickness to micrometers for math consistency
    x_i = initial_thickness_nm / 1000.0 
    
    # 3. Calculate time shift tau (in hours) to account for initial oxide
    tau = (x_i**2 + A * x_i) / B if B != 0 else 0.0
    
    # 4. Deal-Grove positive root calculation (in micrometers)
    # x_o = (-A + sqrt(A^2 + 4B(t + tau))) / 2
    discriminant = A**2 + 4 * B * (time_hr + tau)
    
    if discriminant < 0:
        x_o_um = 0.0 # Safety fallback
    else:
        x_o_um = (-A + math.sqrt(discriminant)) / 2.0
        
    # 5. Convert back to nanometers for the output
    x_o_nm = x_o_um * 1000.0
    
    return x_o_nm