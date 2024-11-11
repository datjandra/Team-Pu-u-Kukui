import streamlit as st
import streamlit.components.v1 as components
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from streamlit_extras.metric_cards import style_metric_cards

@st.cache_data
def fetch_broadband_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT BroadbandCoverage, Latitude, Longitude FROM broadbcover_by_city', ttl=6)
    return df

@st.cache_data
def fetch_readiness_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT Dimension, Details, Unprepared, Old_Guard, Social_Users, Technical, Digital FROM readiness_by_dimensions', ttl=6)
    return df

@st.cache_data
def fetch_campaign_fund_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT Name, `Aggregated Amount` FROM campaign_fund ORDER BY `Aggregated Amount` DESC LIMIT 3', ttl=6)
    return df

def get_header_style():
    # Define the style for the card and header
    header_style = """
        <style>
            .card-header {
                background-image: linear-gradient(0deg, rgba(5, 96.7, 181, 1) 0%, rgba(2.2, 42.2, 1) 100%);
                color: white;
                padding: 10px 20px;
                font-size: 1.2rem;
                font-weight: bold;
                border-radius: 0.5rem 0.5rem 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .card-header .card-header-image img {
                height: 25px;
                width: auto;
            }
            .card {
                border: 1px solid #d3d3d3;
                border-radius: 0.5rem;
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .card-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                border-top: 1px solid #ddd;
            }
            .card-footer-text {
                font-size: 16px;
                color: #333;
            }
            .card-footer-button {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 50px;
                height: 50px;
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                text-decoration: none;
            }
            .card-footer-button:hover {
                background-color: #0056b3;
            }
        </style>
    """
    return header_style

def create_card_header(title, image_link):
    st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <div>{title}</div>
                <div class="card-header-image">
                    <img src="{image_link}" alt="Card Header Image">
                </div>
            </div>
            <div>
    """, unsafe_allow_html=True)

def show_digital_equity_card():
    # Set up a blue header style for the card
    header_style = get_header_style()

    # Display the custom styles in Streamlit
    st.markdown(header_style, unsafe_allow_html=True)
    
    # Create a card layout with a blue header
    st.markdown("""
        <div class="card">
            <div class="card-header">
                <div>Geographical Breakdown</div>
            </div>
            <div>
    """, unsafe_allow_html=True)

    components.iframe("https://app.powerbi.com/view?r=eyJrIjoiM2JmM2QxZjEtYWEzZi00MDI5LThlZDMtODMzMjhkZTY2Y2Q2IiwidCI6ImMxMzZlZWMwLWZlOTItNDVlMC1iZWFlLTQ2OTg0OTczZTIzMiIsImMiOjF9", 
                      height=500)
    
    # Close the card div
    # Add the footer with "Read more about it" and a button
    st.markdown("""
            </div>
            <div class="card-footer">
                <span class="card-footer-text">Read more about it</span>
                <a href="https://app.powerbi.com/view?r=eyJrIjoiM2JmM2QxZjEtYWEzZi00MDI5LThlZDMtODMzMjhkZTY2Y2Q2IiwidCI6ImMxMzZlZWMwLWZlOTItNDVlMC1iZWFlLTQ2OTg0OTczZTIzMiIsImMiOjF9" target="_blank" class="card-footer-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                    </svg>
                </a>
    """, unsafe_allow_html=True)
    
    # Close the card footer and card div
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_device_access_card(col):
    # Set up a blue header style for the card
    header_style = get_header_style()
    
    with col:
        # Display the custom styles in Streamlit
        st.markdown(header_style, unsafe_allow_html=True)
        
        create_card_header("Device Access", "https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/images/monitor-mobbile.png")
            
        df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

        internet_df = df.iloc[170:174]
    
        # Rename columns for clarity (based on your provided data)
        internet_df.columns = ['Computers and Internet Use', 'Hawaii_Total', 'Hawaii_MOE', 'Hawaii_Percent', 'Hawaii_Percent_MOE',
                      'Hawaii_County_Total', 'Hawaii_County_MOE', 'Hawaii_County_Percent', 'Hawaii_County_Percent_MOE',
                      'Honolulu_County_Total', 'Honolulu_County_MOE', 'Honolulu_County_Percent', 'Honolulu_County_Percent_MOE',
                      'Kalawao_County_Total', 'Kalawao_County_MOE', 'Kalawao_County_Percent', 'Kalawao_County_Percent_MOE',
                      'Kauai_County_Total', 'Kauai_County_MOE', 'Kauai_County_Percent', 'Kauai_County_Percent_MOE',
                      'Maui_County_Total', 'Maui_County_MOE', 'Maui_County_Percent', 'Maui_County_Percent_MOE']
    
        # Extract relevant rows and columns for each county
        locations = {
            "Hawaii Total": internet_df.iloc[0, 1],  # Column 2 for "Total households", row 2 for Hawaii Total
        }
        
        # "With a computer" values for each county
        computer_users = {
            "Hawaii Total": internet_df.iloc[1, 1]
        }
    
        # "With broadband" values for each county
        broadband_users = {
            "Hawaii Total": internet_df.iloc[2, 1]
        }
    
        # Create progress bars
        st.subheader("Computer Usage")
        
        for county, total_households in locations.items():
            with_computer = computer_users[county]
            
            # Calculate percentage of households with a computer
            percentage = with_computer / total_households
            
            # Display progress bar with the computed percentage
            st.progress(percentage)

        # Create progress bars
        st.subheader("Broadband Usage")
        
        for county, total_households in locations.items():
            with_broadband = broadband_users[county]
            
            # Calculate percentage of households with broadband
            percentage = with_broadband / total_households
            
            # Display progress bar with the computed percentage
            st.progress(percentage)
        
        # Close the card div
        # Add the footer with "Read more about it" and a button
        st.markdown("""
                </div>
                <div class="card-footer">
                    <span class="card-footer-text">Read more about it</span>
                    <a href="/device_access" target="_self" class="card-footer-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                        </svg>
                    </a>
        """, unsafe_allow_html=True)
        
        # Close the card footer and card div
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_broadband_card(col):
    # Set up a blue header style for the card
    header_style = get_header_style()

    with col:
        # Display the custom styles in Streamlit
        st.markdown(header_style, unsafe_allow_html=True)
        
        # Create a card layout with a blue header
        create_card_header("Broadband Connectivity", "https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/images/cloud-connection.png")
        
        st.subheader("State of Hawaii Broadband Connectivity Map")
        
        # Create a Leaflet map centered at an example location
        # Drop rows where coordinates couldn't be found
        data = fetch_broadband_data()
        data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    
        # Create Leafmap map
        m = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii
    
        # Prepare data for heatmap
        # data['BroadbandCoverage'] = data['BroadbandCoverage'].str.replace('%', '').astype(float)
    
        # Add heatmap layer
        m.add_heatmap(data=data,
                      latitude="Latitude",
                      longitude="Longitude",
                      value="BroadbandCoverage",
                      name="Heat map",
                      radius=15,
                      blur=10, 
                      max_val=100)
            
        # Display the map in Streamlit
        m.to_streamlit(height=500)
        
        # Close the card div
        # Add the footer with "Read more about it" and a button
        st.markdown("""
                </div>
                <div class="card-footer">
                    <span class="card-footer-text">Read more about it</span>
                    <a href="/broadband" target="_self" class="card-footer-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                        </svg>
                    </a>
        """, unsafe_allow_html=True)
        
        # Close the card footer and card div
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_digital_literacy_card(col):
    # Set up a blue header style for the card
    header_style = get_header_style()

    with col:
        # Display the custom styles in Streamlit
        st.markdown(header_style, unsafe_allow_html=True)
        
        # Create a card layout with a blue header
        create_card_header("Digital Literacy", "https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/images/book.png")

        df = fetch_readiness_data()
        # Select the first row where Dimension is 'Overall' and specific columns
        overall_row = df.loc[df['Dimension'] == 'Overall', ['Unprepared', 'Old_Guard', 'Social_Users', 'Technical', 'Digital']]

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Unprepared", value=overall_row['Unprepared'].values[0])
        col2.metric(label="Old Guard", value=overall_row['Old_Guard'].values[0])
        col3.metric(label="Social Users", value=overall_row['Social_Users'].values[0])
        
        col1, col2 = st.columns(2)
        col1.metric(label="Technical", value=overall_row['Technical'].values[0])
        col2.metric(label="Digital", value=overall_row['Digital'].values[0])

        style_metric_cards()

        # Close the card div
        # Add the footer with "Read more about it" and a button
        st.markdown("""
                </div>
                <div class="card-footer">
                    <span class="card-footer-text">Read more about it</span>
                    <a href="/digital_literacy" target="_self" class="card-footer-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                        </svg>
                    </a>
        """, unsafe_allow_html=True)
        
        # Close the card footer and card div
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_open_data_card(col):
    # Set up a blue header style for the card
    header_style = get_header_style()

    with col:
        # Display the custom styles in Streamlit
        st.markdown(header_style, unsafe_allow_html=True)
        
        # Create a card layout with a blue header
        st.markdown("""
            <div class="card">
                <div class="card-header">Open Data</div>
                <div>
        """, unsafe_allow_html=True)

        # Get data from the MySQL table
        df = fetch_campaign_fund_data()
        
        # Create a horizontal bar chart
        fig = px.bar(df, x="Amount", y="Name", orientation='h',
                     title="Top 5 Campaign Fundraising Candidates",
                     labels={"CampaignTotal": "Amount ($)", "Name": "ContributorName"})

        # Customize layout for better readability with long names
        fig.update_layout(yaxis_tickangle=0, margin=dict(l=200, r=20, t=50, b=20))
        
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        
        # Close the card div
        # Add the footer with "Read more about it" and a button
        st.markdown("""
                </div>
                <div class="card-footer">
                    <span class="card-footer-text">Read more about it</span>
                    <a href="https://opendata.hawaii.gov/organization/hbdeo" target="_blank" class="card-footer-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                        </svg>
                    </a>
        """, unsafe_allow_html=True)
        
        # Close the card footer and card div
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_user_feedback_card(col):
    # Set up a blue header style for the card
    header_style = get_header_style()

    with col:
        # Display the custom styles in Streamlit
        st.markdown(header_style, unsafe_allow_html=True)
        
        # Create a card layout with a blue header
        st.markdown("""
            <div class="card">
                <div class="card-header">User Feedback</div>
                <div>
        """, unsafe_allow_html=True)

        # Sample data - replace this with your actual data source
        data = {
            "feedback": ["Yes", "No", "Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "No"]
        }
        df = pd.DataFrame(data)
        
        # Count the "Yes" and "No" responses
        feedback_counts = df['feedback'].value_counts().reset_index()
        feedback_counts.columns = ['Response', 'Count']
        
        # Display the feedback distribution in a pie chart
        fig = px.pie(feedback_counts, values='Count', names='Response', title="User Satisfaction Feedback",
                     color_discrete_sequence=['#34A853', '#EA4335'],  # Customize colors for Yes/No
                     labels={'Count': 'Number of Responses'})
        
        st.plotly_chart(fig)
        
        # Close the card div
        # Add the footer with "Read more about it" and a button
        st.markdown("""
                </div>
                <div class="card-footer">
                    <span class="card-footer-text">Read more about it</span>
                    <a href="#" target="_self" class="card-footer-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                        </svg>
                    </a>
        """, unsafe_allow_html=True)
        
        # Close the card footer and card div
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    
    # Define the HTML and CSS
    html_content = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* Set Montserrat as the default font */
    body {
        font-family: 'Montserrat', sans-serif;
    }
    .e1_15 { 
        color:rgba(255, 255, 255, 1);
        height:52px;
        font-family:Montserrat;
        font-size:45.37845230102539px;
        letter-spacing:0;
        line-height:52px; /* Adjusted to give line height a specific value */
    }
    .e2_21 { 
        background-image:linear-gradient(0deg, rgba(4.999259691685438, 96.68749898672104, 180.9985300898552, 1) 0%, rgba(2.1819744911044836, 42.20017835497856, 78.99852856993675, 1) 100%);
        width: 100%;
        /* height: 256px; */
        height: 200px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
    }
    .e2_22 { 
        color: #f0f8ff;
        height: 52px;
        font-family: Montserrat;
        text-align: left;
        font-size: 45.37845230102539px;
        letter-spacing: 0;
        line-height: 52px; /* Adjusted for consistency */
    }
    .e2_23 { 
        transform: rotate(-2.4848083448933725e-17deg);
        width: 100%;
        height: 0px;
        border: 2px solid rgba(255, 255, 255, 1);
    }
    .e1_8 { 
        width:281px;
        height:281px;
        position: absolute;
        right: 20px;
    }
    .e1_9 { 
        width:259.046875px;
        height:166.84375px;
        position:absolute;
        left:10.9765625px;
        top:57.078125px;
    }
    .header-text-container {
        display: flex;
        flex-direction: column;
    }
    .header-image {
        max-width: 150px;
        height: auto;
    }
    .stButton > button {
        background-image: linear-gradient(0deg, rgba(4, 65, 121, 1) 0%, rgba(7, 119, 223, 1) 100%);
        color: rgba(255, 255, 255, 1);
        width: 200px;  /* Set a maximum width */
        height: 60px;  /* Set height */
        border-radius: 23px;  /* Rounded corners */
        font-family: 'Montserrat', sans-serif;
        font-size: 16px;  /* Font size */
        text-align: center;
        line-height: 60px;  /* Center text vertically */
        border: none;  /* No border */
        cursor: pointer;  /* Change cursor on hover */
        transition: opacity 0.3s ease;  /* Smooth transition for hover effect */
        overflow-wrap: break-word;  /* Allow text to wrap */
        word-wrap: break-word;  /* For compatibility */
        hyphens: auto;  /* Hyphenate words if needed */
    }
    
    /* Hover effect */
    .stButton > button:hover {
        opacity: 0.9;  /* Slightly transparent on hover */
    }
    </style>
    
    <div class="e2_21">
        <div class="header-text-container">
            <div class="e1_15">DIGITAL EQUITY DASHBOARD</div>
            <div class="e2_23"></div>
            <div class="e2_22">Hawaii</div>
        </div>
        <div class="header-image">
            <a href="app" target="_self">
                <img src="https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/images/hawaii.png" alt="Header Image">
            </a>
        </div>
    </div>
    """
    
    # Insert the HTML and CSS into the Streamlit app
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.header("Bridging Hawaii's Digital Divide")
    
    st.markdown(
        """
        Welcome to Hawaii's Digital Equity Dashboard, where we track technology and internet access across our islands. 
        This tool maps the digital divide in our communities, showing where support is needed most.
        """
    )

    col1, col2 = st.columns(2)
    show_device_access_card(col1)
    show_digital_literacy_card(col1)
    show_open_data_card(col1)
    show_broadband_card(col2)
    show_user_feedback_card(col2)
    show_digital_equity_card()

if __name__ == "__main__":
    main()
