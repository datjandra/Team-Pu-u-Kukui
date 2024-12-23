import streamlit as st
import pandas as pd

from pygwalker.api.streamlit import StreamlitRenderer
from streamlit_extras.add_vertical_space import add_vertical_space
from style_helper import apply_custom_style
from st_circular_progress import CircularProgress

@st.cache_data
def fetch_usage_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query("""SELECT Use_pc_internet, County, Estimate, Estimate_Perccent, Margin_Error, Margin_Error_Percent 
        FROM use_pc_internet_by_county""", ttl=6)
    return df

def main():
    apply_custom_style()
    st.header("Internet Usage by County")

    df = fetch_usage_data()
    # Filter out rows where "Use_pc_internet" is "Total households"
    df_filtered = df[df['Use_pc_internet'] != 'Total households']

    # Reorder df_filtered so "HawaiiState" appears first in the "County" column
    df_filtered = pd.concat([
        df_filtered[df_filtered['County'] == "HawaiiState"],
        df_filtered[df_filtered['County'] != "HawaiiState"]
    ])

    # Group by county and display each type in two columns for each county
    for county, group in df_filtered.groupby("County", sort=False):
        st.write(f"### {county}")  # Display the county name as a section header
    
        # Create two columns for displaying progress bars side by side
        col1, col2 = st.columns(2)
        
        for i, (_, row) in enumerate(group.iterrows()):
            # Alternate between columns for each type of internet usage
            if i % 2 == 0:
                col = col1
                color = "#0778DF"
            else:
                col = col2
                color = "#FF3583"

            percentage = int(row['Estimate_Perccent'] * 100)

            # Display the type of internet usage and the progress bar
            with col:
                cp = CircularProgress(
                        label=row['Use_pc_internet'],
                        value=percentage,
                        color=color,
                        key=f"cell_{i}_{col}")
                cp.st_circular_progress()

    renderer = StreamlitRenderer(df, spec="./gw_config.json")
    renderer.explorer()
    
if __name__ == "__main__":
    main()
