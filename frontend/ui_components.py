import streamlit as st

instructions = ["Enter a name of a business along with its location, then click 'Fetch Details' to retrieve its essential information. This will include the business name, industry category, address, rating, phone number, and website link (if available). Ideal for quickly looking up a specific business and verifying its details.", "Search for businesses in a specific category within a given location by entering a business type (e.g., 'Tech company') and a city or region. Then, click 'Fetch Businesses' to retrieve a list of matching businesses. Great for discovering potential leads, partners, or competitors in a given industry.", "Enter a name of a business and its location, then click 'Find Competitors' to discover similar businesses in the same industry. Helps identify direct competitors in the same area, useful for market research."]

def header(title: str, subtitle: str = ""):
    """
    Render a styled header with a title and optional subtitle.
    """
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"#### {subtitle}")

def display_single_business(data: dict):
    """
    Render a structured and styled format for a single business.
    """
    st.markdown("""
        <style>
            .business-name {
                font-size: 24px;
                font-weight: bold;
                color: #E1AD01;
            }
            .business-info {
                font-size: 18px;
                color: #DDDDDD;
            }
            .divider {
                border-bottom: 1px solid #555;
                margin-top: 5px;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Extract business details
    name = data.get("Name", "N/A")
    category = data.get("Category", "N/A")
    rating = data.get("Rating", "N/A")
    address = data.get("Address", "N/A")
    website = data.get("Website", "N/A")
    phone = data.get("Phone", "N/A")

    # Display business details in a structured format
    st.markdown(f"""
        <div class='business-name'>{name}</div>
        <div class='business-info'>{category} | {rating} ⭐</div>
        <div class='divider'></div>
        <div class='business-info'><strong>📍 Address:</strong> {address}</div>
        <div class='business-info'><strong>🌐 <a href='{website}' target='_blank'>Website</a></strong></div>
        <div class='business-info'><strong>📞 Phone:</strong> {phone}</div>
    """, unsafe_allow_html=True)

def display_business_list(data: list):
    """
    Render a structured business list with minimalistic design.
    """
    with st.container():
        # Minimal CSS Styling
        st.markdown("""
            <style>
                .scroll-box {
                    max-height: 400px;
                    overflow-y: auto;
                    border: 1px solid #333;
                    border-radius: 6px;
                    padding: 12px;
                    background-color: #1E1E1E;
                }
                .business-title {
                    font-size: 26px;
                    font-weight: bold;
                    color: #E1AD01;
                }
                .business-info {
                    font-size: 18px;
                    color: #DDDDDD;
                }
                .divider {
                    border-bottom: 1px solid #555;
                    margin-top: 5px;
                    margin-bottom: 10px;
                }
                .small-text {
                    font-size: 14px;
                    color: #AAAAAA;
                }
            </style>
            """, unsafe_allow_html=True)

        # Scrollable container
        with st.container():
            for index, item in enumerate(data, start=1):
                # Extracting data properly
                name = item.get("Name", "N/A")
                category = item.get("Category", "N/A")
                rating = item.get("Rating", "N/A")
                address = item.get("Address", "N/A")
                website = item.get("Website", "#")
                phone = item.get("Phone", "N/A")

                # Minimalistic Output
                st.markdown(f"""
                    <div class='business-title'>{name}</div>
                    <div class='business-info'>{category} | {rating} ⭐</div>
                    <div class='divider'></div>
                    <div class='small-text'>
                        📍 {address} <br>
                        🌐 <a href="{website}" target="_blank">Website</a> &nbsp;&nbsp; 📞 {phone}
                    </div>
                    <br>
                """, unsafe_allow_html=True)