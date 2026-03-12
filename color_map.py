def wavelength_to_rgb(wavelength_nm: float) -> tuple[int, int, int]:
    """
    Converts a given wavelength (nm) to an RGB tuple (0-255).
    Expanded slightly to 380-780nm to capture full human vision.
    """
    gamma = 0.80
    intensity_max = 255
    factor = 0.0
    R = G = B = 0.0

    if 380 <= wavelength_nm <= 440:
        R = -(wavelength_nm - 440) / (440 - 380)
        G = 0.0
        B = 1.0
    elif 440 < wavelength_nm <= 490:
        R = 0.0
        G = (wavelength_nm - 440) / (490 - 440)
        B = 1.0
    elif 490 < wavelength_nm <= 510:
        R = 0.0
        G = 1.0
        B = -(wavelength_nm - 510) / (510 - 490)
    elif 510 < wavelength_nm <= 580:
        R = (wavelength_nm - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif 580 < wavelength_nm <= 645:
        R = 1.0
        G = -(wavelength_nm - 645) / (645 - 580)
        B = 0.0
    elif 645 < wavelength_nm <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        return (0, 0, 0) 

    if 380 <= wavelength_nm <= 420:
        factor = 0.3 + 0.7 * (wavelength_nm - 380) / (420 - 380)
    elif 420 < wavelength_nm <= 700:
        factor = 1.0
    elif 700 < wavelength_nm <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength_nm) / (780 - 700)
    else:
        factor = 0.0

    def adjust(color, factor):
        if color == 0.0:
            return 0
        return int(round(intensity_max * (color * factor) ** gamma))

    return adjust(R, factor), adjust(G, factor), adjust(B, factor)


def thickness_to_color(thickness_nm: float) -> str:
    """
    Maps oxide thickness to a hex color using the thin-film interference equation:
    2 * n_ox * x_o = (m + 1/2) * lambda
    """
    N_OX = 1.46 
    
    if thickness_nm < 30:
        return "#A9A9A9" # Bare Silicon / Very thin oxide

    valid_rgbs = []
    closest_wavelength = None
    min_dist = float('inf')
    
    for m in range(5):
        wavelength = (2 * N_OX * thickness_nm) / (m + 0.5)
        
        # Track the wavelength closest to the center of visible spectrum (~550nm)
        dist_to_center = abs(wavelength - 550)
        if dist_to_center < min_dist:
            min_dist = dist_to_center
            closest_wavelength = wavelength
        
        # Use an expanded visible spectrum
        if 380 <= wavelength <= 780:
            rgb = wavelength_to_rgb(wavelength)
            valid_rgbs.append(rgb)

    # If no wavelengths fell in the visible spectrum (UV/IR gaps), 
    # clamp the closest one to the edge of the visible spectrum.
    if not valid_rgbs and closest_wavelength is not None:
        clamped_wl = max(380.0, min(780.0, closest_wavelength))
        valid_rgbs.append(wavelength_to_rgb(clamped_wl))
         
    # Average the RGB values
    avg_r = int(sum(c[0] for c in valid_rgbs) / len(valid_rgbs))
    avg_g = int(sum(c[1] for c in valid_rgbs) / len(valid_rgbs))
    avg_b = int(sum(c[2] for c in valid_rgbs) / len(valid_rgbs))

    return f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"