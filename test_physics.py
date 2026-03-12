from physics import compute_thickness, compute_rate_constants

def test_oxidation():
    print("--- Testing Physics Engine ---")
    
    # Test 1: Dry Oxidation
    # Parameters: 1000 C, 1 atm, 2 hours, Native oxide ~2nm
    t_dry, temp_dry, p_dry = 2.0, 1000.0, 1.0
    B_d, BA_d, A_d = compute_rate_constants(temp_dry, p_dry, "dry")
    thick_dry = compute_thickness(t_dry, temp_dry, p_dry, "dry", initial_thickness_nm=2.0)
    
    print("\n[Dry Oxidation: 1000 C, 1 atm, 2 hours, 2nm initial]")
    print(f"B   = {B_d:.5f} um^2/hr")
    print(f"B/A = {BA_d:.5f} um/hr")
    print(f"A   = {A_d:.5f} um")
    print(f"Resulting Thickness: {thick_dry:.2f} nm")

    # Test 2: Wet Oxidation
    # Parameters: 1000 C, 1 atm, 1 hour, No initial oxide
    t_wet, temp_wet, p_wet = 1.0, 1000.0, 1.0
    B_w, BA_w, A_w = compute_rate_constants(temp_wet, p_wet, "wet")
    thick_wet = compute_thickness(t_wet, temp_wet, p_wet, "wet", initial_thickness_nm=0.0)
    
    print("\n[Wet Oxidation: 1000 C, 1 atm, 1 hour, 0nm initial]")
    print(f"B   = {B_w:.5f} um^2/hr")
    print(f"B/A = {BA_w:.5f} um/hr")
    print(f"A   = {A_w:.5f} um")
    print(f"Resulting Thickness: {thick_wet:.2f} nm")
    
    # Test 3: High Pressure Dry
    t_hp, temp_hp, p_hp = 2.0, 1000.0, 2.0 # 2 atm
    thick_hp = compute_thickness(t_hp, temp_hp, p_hp, "dry", initial_thickness_nm=2.0)
    print("\n[High Pressure Dry: 1000 C, 2.0 atm, 2 hours, 2nm initial]")
    print(f"Resulting Thickness: {thick_hp:.2f} nm")

if __name__ == "__main__":
    test_oxidation()