import streamlit as st
import requests
from dotenv import load_dotenv
import os
from ui_components import header, display_single_business, display_business_list, instructions

load_dotenv()
BASE_URL = os.getenv("API_BASE_URL")

# Streamlit app configuration
st.set_page_config(page_title="LeadGen Scraper", layout="wide")

# App title
header("LeadGen Scraper", "Effortlessly fetch business details, similar businesses, and competitors.")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Single Business", "Multiple Businesses", "Find Competitors"])

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Get Business Details")
        query = st.text_input("Enter a company name", key="single_query", placeholder="Apple Inc.")
        location = st.text_input("Enter the location", key="single_location", placeholder="California")

        if st.button("Fetch Details", key="fetch_single"):
            if query and location:
                with st.spinner("Fetching business details..."):
                    response = requests.get(f"{BASE_URL}/business-details",
                                            params={"query": query, "location": location})
                    if response.status_code == 200:
                        st.success("Business details retrieved successfully!")
                        st.session_state["single_business"] = response.json()["data"]
                    else:
                        st.error(f"Error: {response.json()['detail']}")

    with col2:
        output_single = st.empty()  # Placeholder for instructions or data

        if "single_business" in st.session_state:
            output_single.empty()  # Remove instruction text when data is available
            display_single_business(st.session_state["single_business"])
        else:
            output_single.markdown(
                f"ℹ️ **{instructions[0]}**",
                unsafe_allow_html=True,
            )

with tab2:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Get Businesses by Category")
        query = st.text_input("Enter a business type", key="multiple_query", placeholder="Private equity firm")
        location = st.text_input("Enter the location", key="multiple_location", placeholder="Vancouver")

        if st.button("Fetch Businesses", key="fetch_multiple"):
            if query and location:
                with st.spinner("Fetching businesses by category..."):
                    response = requests.get(f"{BASE_URL}/businesses-by-category",
                                            params={"query": query, "location": location})
                    if response.status_code == 200:
                        st.success(f"Found {len(response.json()['data'])} businesses!")
                        st.session_state["multiple_businesses"] = response.json()["data"]
                    else:
                        st.error(f"Error: {response.json()['detail']}")

    with col2:
        output_multi = st.empty()  # Placeholder for instructions or data

        if "multiple_businesses" in st.session_state:
            output_multi.empty()  # Remove instruction text when data is available
            with st.container():
                display_business_list(st.session_state["multiple_businesses"])
        else:
            output_multi.markdown(
                f"ℹ️ **{instructions[1]}**",
                unsafe_allow_html=True,
            )

with tab3:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Find Competitors")
        query = st.text_input("Enter a company name", key="competitor_query")
        location = st.text_input("Enter the location", key="competitor_location")

        if st.button("Find Competitors", key="fetch_competitors"):
            if query and location:
                with st.spinner("Fetching competitors..."):
                    response = requests.get(f"{BASE_URL}/get-competitors",
                                            params={"query": query, "location": location})
                    if response.status_code == 200:
                        st.success(f"Found {len(response.json()['data'])} competitors!")
                        st.session_state["competitors"] = response.json()["data"]
                    else:
                        st.error(f"Error: {response.json()['detail']}")

    with col2:
        output_comp = st.empty()  # Placeholder for instructions or data

        if "competitors" in st.session_state:
            output_comp.empty()  # Remove instruction text when data is available
            with st.container():
                display_business_list(st.session_state["competitors"])
        else:
            output_comp.markdown(
                f"ℹ️ **{instructions[2]}**",
                unsafe_allow_html=True,
            )