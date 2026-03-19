import math

def wavelength_to_rgb(wavelength_nm: float) -> tuple[float, float, float]:
    """
    Returns raw 0.0 to 1.0 RGB values for a specific wavelength.
    """
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
        return 0.0, 0.0, 0.0

    # Intensity fall-off near edges of human vision
    if 380 <= wavelength_nm <= 420:
        factor = 0.3 + 0.7 * (wavelength_nm - 380) / (420 - 380)
    elif 420 < wavelength_nm <= 700:
        factor = 1.0
    elif 700 < wavelength_nm <= 780:
        factor = 0.3 + 0.7 * (780 - wavelength_nm) / (780 - 700)
    else:
        factor = 0.0

    return (R * factor, G * factor, B * factor)


def thickness_to_color(thickness_nm: float) -> str:
    """
    Maps oxide thickness to a hex color using Visible Spectrum Integration.
    This avoids the flaws of discrete-wavelength mapping by simulating 
    broad-spectrum white light reflection.
    """
    N_OX = 1.46
    
    # Base Silicon (Silver/Grey)
    if thickness_nm < 2:
        return "#A9A9A9"

    sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
    
    # Integrate over the visible spectrum (380nm to 780nm)
    for wl in range(380, 781, 5):
        # Calculate reflection intensity for this specific wavelength
        # Intensity scales with cos^2(2 * pi * n * x / lambda) for SiO2 on Si
        phase = (2 * math.pi * N_OX * thickness_nm) / wl
        intensity = math.cos(phase) ** 2
        
        # Add the weighted color to our total reflection
        r, g, b = wavelength_to_rgb(wl)
        sum_r += r * intensity
        sum_g += g * intensity
        sum_b += b * intensity
        
    # Normalize the accumulated light to valid 0-255 RGB values
    max_val = max(sum_r, sum_g, sum_b, 1.0)
    
    # Apply a slight gamma correction (0.8) to emulate realistic, non-neon oxide colors
    gamma = 0.80
    final_r = int(255 * ((sum_r / max_val) ** gamma))
    final_g = int(255 * ((sum_g / max_val) ** gamma))
    final_b = int(255 * ((sum_b / max_val) ** gamma))
    
    return f"#{final_r:02x}{final_g:02x}{final_b:02x}"