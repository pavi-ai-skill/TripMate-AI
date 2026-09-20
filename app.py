import streamlit as st
import sys
import os

# Ensure the root project directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.travel_graph import travel_graph

# Page configuration
st.set_page_config(
    page_title="TripMate AI - Travel Itinerary Planner",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ TripMate AI Itinerary Planner")
st.markdown("Enter your travel request below in natural language. Our multi-agent system will parse your details, fetch real-time flights, hotels, and weather, and generate a customized itinerary!")

# User Input Form
with st.form("travel_form"):
    user_query = st.text_area(
        "Describe your trip:",
        value="I want to plan a trip from Charlotte to Paris from September 18, 2026 to September 25, 2026, staying at a boutique hotel.",
        height=100
    )
    
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    if not user_query.strip():
        st.warning("Please enter a valid travel request.")
    else:
        # Initialize the state packet for LangGraph
        initial_state = {
            "user_query": user_query,
            "origin": "",
            "destination": "",
            "preferences": "",
            "start_date": "",
            "end_date": "",
            "flight_data": {},
            "hotel_data": {},
            "weather_data": {},
            "consolidated_itinerary": ""
        }
        
        # UI Progress representation
        with st.status("Executing Multi-Agent Workflow...", expanded=True) as status:
            st.write("Initializing LangGraph execution node...")
            try:
                # Invoke the compiled graph
                final_state = travel_graph.invoke(initial_state)
                status.update(label="Itinerary successfully generated!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Workflow execution failed.", state="error")
                st.error(f"Error: {str(e)}")
                final_state = None

        # Display Extracted Parameters & Results if successful
        if final_state and final_state.get("consolidated_itinerary"):
            st.success("Trip successfully planned!")
            
            # Show parsed metadata in an expandable section
            with st.expander("🔍 View Extracted Trip Parameters"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Origin", final_state.get("origin", "N/A"))
                col2.metric("Destination", final_state.get("destination", "N/A"))
                col3.metric("Dates", f"{final_state.get('start_date')} to {final_state.get('end_date')}")
                st.write(f"**Preferences:** {final_state.get('preferences', 'N/A')}")

            st.markdown("---")
            
            # Display Final Itinerary Output
            st.subheader("📋 Final Consolidated Itinerary")
            st.markdown(final_state["consolidated_itinerary"])