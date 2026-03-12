from color_map import thickness_to_color, wavelength_to_rgb

def test_colors():
    print("--- Testing Thin-Film Color Mapping ---")
    
    # Standard known thicknesses and their typical perceived colors
    # ~50nm: Tan/Brown
    # ~100nm: Purple/Violet
    # ~150nm: Blue
    # ~200nm: Greenish/Yellow
    # ~280nm: Orange/Red
    
    test_thicknesses = [10.0, 50.0, 100.0, 150.0, 200.0, 280.0, 450.0]
    
    for t in test_thicknesses:
        hex_col = thickness_to_color(t)
        print(f"Thickness: {t:>5.1f} nm --> Hex Color: {hex_col}")
        
    print("\n[Optional] You can check these hex codes in a color picker online to see if they match the expected SiO2 chart colors.")

if __name__ == "__main__":
    test_colors()