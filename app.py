import streamlit as st
import sys
import os

# Ensure root directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.travel_graph import travel_graph

# Page configuration
st.set_page_config(
    page_title="TripMate AI | Intelligent Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for a Flashy, Modern Look
st.markdown("""
    <style>
    /* Main Theme & Background */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 30px;
    }

    /* Itinerary Output Container */
    .itinerary-container {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/globe--v1.png", width=80)
    st.markdown("### **TripMate AI Dashboard**")
    st.markdown("Powered by **LangGraph** & **Groq**.")
    st.markdown("---")
    
    # Generate and display LangGraph workflow image in the sidebar
    st.markdown("### 🕸️ Multi-Agent Workflow")
    try:
        # Generate PNG bytes of the LangGraph state machine
        graph_image_bytes = travel_graph.get_graph().draw_mermaid_png()
        st.image(graph_image_bytes, caption="Sequential Agent Graph", use_container_width=True)
    except Exception as e:
        st.info("Workflow diagram preview unavailable (requires pygraphviz / graphviz system binaries).")

    st.markdown("---")
    st.markdown("💡 **Tip:** Be specific with your dates and cities for best real-time weather and flight matching!")

# Main Header
st.markdown('<p class="main-header">✈️ TripMate AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your autonomous multi-agent coordinator for intelligent, weather-aware travel itineraries.</p>', unsafe_allow_html=True)

# Tabs for dashboard organization
tab_plan, tab_about = st.tabs(["✨ Plan Trip", "📖 System Architecture"])

with tab_plan:
    with st.form("travel_form"):
        st.subheader("Describe Your Dream Trip")
        user_query = st.text_area(
            "Natural Language Request:",
            value="I want to plan a trip from Charlotte to Bangkok from September 25, 2026 to September 30, 2026, staying at a boutique hotel.",
            height=90,
            help="Type your travel request naturally including origin, destination, and exact dates."
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submitted = st.form_submit_button("🚀 Generate Trip", use_container_width=True)

    if submitted:
        if not user_query.strip():
            st.warning("⚠️ Please enter a valid travel request description.")
        else:
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
            
            with st.status("🤖 **Multi-Agents at Work...**", expanded=True) as status:
                st.write("🔍 Parsing sentence parameters & extracting dates...")
                st.write("✈️ Fetching round-trip flight options...")
                st.write("🏨 Searching top-rated hotels matching preferences...")
                st.write("🌤️ Pulling and filtering destination weather forecast...")
                try:
                    final_state = travel_graph.invoke(initial_state)
                    status.update(label="✨ Itinerary successfully built!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="❌ Workflow execution failed.", state="error")
                    st.error(f"Error encountered: {str(e)}")
                    final_state = None

            if final_state and final_state.get("consolidated_itinerary"):
                st.success("🎉 Your personalized travel plan is ready!")
                
                # Metric Cards Row
                st.markdown("### 📊 Trip Overview")
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    st.metric(label="📍 Origin", value=final_state.get("origin", "N/A"))
                with m2:
                    st.metric(label="🎯 Destination", value=final_state.get("destination", "N/A"))
                with m3:
                    st.metric(label="🛫 Departure", value=final_state.get("start_date", "N/A"))
                with m4:
                    st.metric(label="🛬 Return", value=final_state.get("end_date", "N/A"))
                
                st.markdown("<br>", unsafe_allow_html=True)

                # Final Itinerary Box
                st.markdown("### 📋 Final Consolidated Itinerary")
                st.markdown(f"""
                    <div class="itinerary-container">
                        {final_state["consolidated_itinerary"]}
                    </div>
                """, unsafe_allow_html=True)

with tab_about:
    st.subheader("How TripMate AI Works")
    st.markdown("""
    TripMate AI is a modular, state-driven multi-agent framework built using:
    * **LangGraph:** Orchestrates sequential agent workflows from query parsing to data consolidation.
    * **Groq Llama:** Powers lightning-fast natural language understanding and synthesis.
    * **OpenWeather & Aviation APIs:** Injects precise, window-filtered forecasts and carrier schedules directly into your daily timeline.
    """)
    
    # Optional full view of the graph on the architecture tab
    st.markdown("### Full Graph Topology")
    try:
        st.image(travel_graph.get_graph().draw_mermaid_png(), caption="LangGraph State Machine Pipeline", use_container_width=True)
    except Exception:
        st.info("Graph image requires graphviz system dependencies.")