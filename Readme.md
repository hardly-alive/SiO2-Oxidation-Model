# Deal-Grove SiO₂ Oxidation & Thin-Film Color Simulator

A Python-based Streamlit application that models the thermal oxidation of silicon using the Deal-Grove model and visualizes the resulting thin-film interference color of the SiO₂ layer. Designed as a simulation tool for VLSI Process Engineering.

## 🌟 Features
* **Interactive UI:** Streamlit sliders for Process Temperature (800–1200 °C), Pressure (0.5–3.0 atm), and Oxidation Time (0–5 hours).
* **Advanced Deal-Grove Physics:** Computes oxide growth supporting both Dry O₂ and Wet H₂O environments, including Arrhenius temperature dependence and linear pressure scaling.
* **Real-time Color Mapping:** Calculates the constructive interference wavelength to accurately render the perceived visible color of the thin film.
* **Growth Visualization:** Dynamically generates a Matplotlib oxide thickness vs. time curve.

---

## 🔬 Physics & Mathematical Models

### 1. Deal-Grove Oxide Growth
The core oxide thickness is calculated using the positive root of the Deal-Grove solution:

$$x_o(t)=\frac{-A+\sqrt{A^2+4B(t+\tau)}}{2}$$

Where:
* $x_o$ = oxide thickness
* $A$ = linear rate constant ($\mu$ m)
* $B$ = parabolic rate constant ($\mu$ m²/hr)
* $\tau$ = time shift accounting for initial oxide thickness

### 2. Temperature Dependence (Arrhenius Equation)
The rate constants are highly temperature-dependent, driven by the activation energies ($E_a$) of the oxidizing species:

$$B(T)=B_0\exp\left(-\frac{E_{a,B}}{k_BT}\right)$$
$$(B/A)(T)=(B/A)_0\exp\left(-\frac{E_{a,BA}}{k_BT}\right)$$

**Activation Energies Used:**
* **Dry O₂:** $E_a$ (Parabolic) = 1.24 eV | $E_a$ (Linear) = 2.00 eV 
* **Wet H₂O:** $E_a$ (Parabolic) = 0.78 eV | $E_a$ (Linear) = 2.05 eV 

### 3. High-Pressure Scaling
Process pressure scales the rate constants linearly:

$$B_{new}=B\times P$$
$$(B/A)_{new}=(B/A)\times P$$
*(Where $P$ is pressure in atm)* 

### 4. Thin-Film Interference Color
The visible color of the oxide layer arises from normal-incidence destructive/constructive interference:

$$2n_{ox}x_o=(m+\frac{1}{2})\lambda$$

Where:
* $n_{ox}$ = 1.46 (Refractive index of SiO₂) 
* $m$ = interference order (0, 1, 2, ...) 
* $\lambda$ = wavelength in nm 

*Note on Color Engine Logic: If the calculated constructive wavelength falls into the UV or IR spectrum (outside the 400-700 nm range), the application clamps the value to the nearest visible edge to accurately approximate the color perceived by the human eye, preventing dead visual zones.*


## 📂 Project Structure

```text
sio2_oxidation_app/
│
├── app.py             # Main Streamlit GUI and visualization
├── physics.py         # Deal-Grove and Arrhenius calculations
├── color_map.py       # Interference wavelength to RGB/Hex mapping
├── test_physics.py    # Unit tests for the physics engine
├── test_color.py      # Unit tests for hex color generation
└── README.md

```

## 🚀 Installation & Usage

### Prerequisites

Make sure you have Python 3.10+ installed.

### 1. Install Dependencies

Install the required libraries via pip:

```bash
pip install streamlit numpy matplotlib
```

### 2. Run the Application

Navigate to the project directory in your terminal and start the Streamlit server.

**Standard Command:**

```bash
streamlit run app.py
```

**Windows User Fix:**
If your system throws a `'streamlit' is not recognized` error due to PATH configuration issues, use the Python module execution command instead:

```bash
python -m streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## ✅ Validation

This tool has been validated against the industry-standard **BYU Cleanroom Oxide Thickness Calculator**. For a (100) Silicon wafer undergoing Dry Oxidation at 1000°C for 1 hour, this engine predicts an oxide thickness of **71.1 nm** and accurately maps it to a Tan/Brown color, matching theoretical models.