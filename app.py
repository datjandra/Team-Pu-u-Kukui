import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Broadband Connectivity Heatmap")

    # Load data
    data_file = "data/BroadBandCover_by_City.csv"
    data = pd.read_csv(data_file)
    
    # Drop rows where coordinates couldn't be found
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    # Create Leafmap map
    m = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii

    # Prepare data for heatmap
    data['BroadbandCoverage'] = data['BroadbandCoverage'].str.replace('%', '').astype(float)

    # Add heatmap layer
    m.add_heatmap(data=data,
                  latitude="Latitude",
                  longitude="Longitude",
                  value="BroadbandCoverage",
                  name="Heat map",
                  radius=15,
                  blur=10, 
                  max_val=100)
    
    m.to_streamlit(height=500)

#-------------------------
#Test tiger
# Initialize connection.
conn = st.connection('mysql', type='sql')
st.write ("Connection to mysql")

#------------------

if __name__ == "__main__":
    main()
