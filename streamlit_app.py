import streamlit as st
import json
import os
from datetime import datetime
from laboratory import AgentLaboratory

# Set page config
st.set_page_config(
    page_title="Agent Laboratory Research Lab",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state for storing research results
if 'research_results' not in st.session_state:
    st.session_state.research_results = []
    # Load existing results if available
    if os.path.exists('research_results.json'):
        try:
            with open('research_results.json', 'r') as f:
                st.session_state.research_results = json.load(f)
        except:
            pass

def save_results():
    """Save research results to file."""
    with open('research_results.json', 'w') as f:
        json.dump(st.session_state.research_results, f)

def conduct_research(api_key, topic, focus_areas):
    """Conduct research using the Agent Laboratory."""
    lab = AgentLaboratory(api_key=api_key, model_name="o1-preview")
    
    task_notes = {
        "focus_areas": [area.strip() for area in focus_areas.split(",")],
        "experiment_preferences": {
            "dataset_size": "small",
            "model_complexity": "medium",
            "evaluation_metrics": ["accuracy", "perplexity"]
        }
    }
    
    results = lab.conduct_research(topic, task_notes)
    return results

# Main app layout
st.title("🧪 Agent Laboratory Research Lab")
st.subheader("Advanced Research Assistant")

# Sidebar
with st.sidebar:
    st.header("Previous Research")
    
    # Display list of previous research
    for idx, result in enumerate(st.session_state.research_results):
        if st.button(f"Research #{result['id']}: {result['topic']}", key=f"btn_{idx}"):
            st.session_state.selected_research = result

    st.divider()
    st.markdown("### Start New Research")
    
    # API Key input
    api_key = st.text_input("OpenAI API Key", type="password")
    
    # Research inputs
    topic = st.text_input("Research Topic")
    focus_areas = st.text_input("Focus Areas (comma-separated)")
    
    if st.button("Start Research", type="primary"):
        if not api_key:
            st.error("Please enter your API Key")
        elif not topic:
            st.error("Please enter a research topic")
        elif not focus_areas:
            st.error("Please enter focus areas")
        else:
            with st.spinner("Conducting research..."):
                try:
                    # Conduct research
                    results = conduct_research(api_key, topic, focus_areas)
                    
                    # Create new research entry
                    new_id = len(st.session_state.research_results) + 1
                    entry = {
                        "id": new_id,
                        "topic": topic,
                        "focus_areas": [area.strip() for area in focus_areas.split(",")],
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "final_report": results["final_report"],
                        "model_name": results.get("model_name", "Unknown")
                    }
                    
                    # Add to results and save
                    st.session_state.research_results.append(entry)
                    save_results()
                    
                    # Select the new research
                    st.session_state.selected_research = entry
                    st.success("Research completed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Main content area
if hasattr(st.session_state, 'selected_research'):
    result = st.session_state.selected_research
    
    # Display research details
    st.header(f"Research #{result['id']}: {result['topic']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Date:** {result['date']}")
    with col2:
        st.markdown(f"**Focus Areas:** {', '.join(result['focus_areas'])}")
    with col3:
        st.markdown(f"**AI Model:** {result.get('model_name', 'Unknown')}")
    
    st.divider()
    
    # Display research results
    st.markdown("## Research Results")
    st.markdown(result['final_report'])
    
    # Export options
    if st.button("Export as Markdown"):
        # Create markdown content
        content = f"# Research #{result['id']}: {result['topic']}\n\n"
        content += f"Date: {result['date']}\n\n"
        content += f"Focus Areas: {', '.join(result['focus_areas'])}\n\n"
        content += f"AI Model: {result.get('model_name', 'Unknown')}\n\n"
        content += "## Research Results\n\n"
        content += result['final_report']
        
        # Save to file
        filename = f"research_{result['id']}_{result['topic'][:30]}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        st.success(f"Research exported as {filename}")
else:
    st.info("👈 Select a previous research from the sidebar or start a new one")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center'>
        <p>© 2024 AI Engineering | <a href='https://ai-engineering.ai'>ai-engineering.ai</a></p>
        <p>Created by Dirk Wonhoefer | <a href='mailto:dirk.wonhoefer@ai-engineering.ai'>dirk.wonhoefer@ai-engineering.ai</a></p>
    </div>
    """,
    unsafe_allow_html=True
) 