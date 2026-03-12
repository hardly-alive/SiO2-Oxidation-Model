import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from physics import compute_thickness
from color_map import thickness_to_color

def main():
    st.set_page_config(page_title="SiO2 Oxidation Model", layout="wide")
    
    st.title("Deal-Grove SiO₂ Oxidation Model")
    st.markdown("Calculates thermal oxide thickness and simulates thin-film interference color.")

    # --- SIDEBAR INPUTS ---
    st.sidebar.header("Process Parameters")
    
    ox_type = st.sidebar.radio("Oxidation Type", ["dry", "wet"])
    
    temp_c = st.sidebar.slider("Temperature (°C)", min_value=800, max_value=1200, value=1000, step=10)
    pressure_atm = st.sidebar.slider("Pressure (atm)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    time_hr = st.sidebar.slider("Oxidation Time (hours)", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
    
    init_thickness = st.sidebar.number_input("Initial Oxide Thickness (nm)", min_value=0.0, max_value=100.0, value=0.0)

    # --- COMPUTATION ---
    # 1. Compute single target thickness
    final_thickness_nm = compute_thickness(time_hr, temp_c, pressure_atm, ox_type, init_thickness)
    
    # 2. Get color for target thickness
    oxide_color = thickness_to_color(final_thickness_nm)

    # --- RESULTS DISPLAY ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Results")
        st.metric(label="Final Oxide Thickness", value=f"{final_thickness_nm:.2f} nm")
        
        st.markdown("### Thin-Film Interference Color")
        # Display the color using HTML/CSS
        color_box_html = f"""
        <div style="
            background-color: {oxide_color};
            width: 100%;
            height: 150px;
            border-radius: 10px;
            border: 2px solid #333;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        ">
            <span style="background-color: rgba(255,255,255,0.7); padding: 5px 10px; border-radius: 5px; font-weight: bold; color: black;">
                {oxide_color}
            </span>
        </div>
        """
        st.markdown(color_box_html, unsafe_allow_html=True)

    with col2:
        st.subheader("Growth Curve")
        # Generate time array for plotting
        t_array = np.linspace(0.01, max(5.0, time_hr), 100)
        thickness_array = [
            compute_thickness(t, temp_c, pressure_atm, ox_type, init_thickness) 
            for t in t_array
        ]
        
        # Matplotlib Plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(t_array, thickness_array, color='blue', linewidth=2)
        ax.scatter([time_hr], [final_thickness_nm], color='red', zorder=5, label='Current State')
        
        ax.set_title(f"{ox_type.capitalize()} Oxidation at {temp_c}°C, {pressure_atm} atm")
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Thickness (nm)")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        st.pyplot(fig)

if __name__ == "__main__":
    main()