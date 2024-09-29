import streamlit as st
import pandas as pd
from PIL import Image
import time

def create_superset(data):
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Superset Summary</h1>", unsafe_allow_html=True)

    default_keywords = [
        "Design thinking", "Innovation", "Problem solving", "Radical thinking", "Creativity", 
        "Morphological thinking", "Critical thinking", "Reasoning", "Invention", "Unconventional thinking",
        "Brainstorming", "Divergent thinking", "Convergent thinking", "Ideation",
        "Idea", "Lateral thinking", "Design sprint", "Systems thinking", "Innovation management"
    ]

    additional_keywords_input = st.text_area(
        "Enter additional keywords (comma-separated):", 
        value="", 
        placeholder="e.g., Agile, Lean, Iteration"
    )

    if st.button("Update Keywords"):
        additional_keywords = [keyword.strip() for keyword in additional_keywords_input.split(',') if keyword.strip()]
        keywords = default_keywords + additional_keywords
        st.session_state.keywords = keywords

        with st.spinner("Creating superset for keywords..."):
            time.sleep(2)
            st.session_state.superset_data = process_superset(data, keywords)

    if st.button("No new keywords, create superset"):
        st.session_state.keywords = default_keywords

        with st.spinner("Creating superset with default keywords..."):
            time.sleep(2)
            st.session_state.superset_data = process_superset(data, default_keywords)

    if 'superset_data' in st.session_state:
        table_df = st.session_state.superset_data
    else:
        table_df = pd.DataFrame(columns=["Course Structure", "Outcome", "Course Type"])

    st.markdown("""
        <style>
        .dataframe {
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe th, .dataframe td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe th {
            background-color: transparent;
            color: #4A90E2;
            text-align: center;
        }
        .dataframe td {
            text-align: left;
        }
        .dataframe tr:nth-child(even) {
            background-color: transparent;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.write(table_df.to_html(index=False, classes='dataframe', escape=False), unsafe_allow_html=True)

    with st.sidebar:
        st.download_button(
            label="Download Superset Summary",
            data=table_df.to_csv(index=False),
            file_name='superset_summary.csv',
            mime='text/csv'
        )
        if st.button("Back to Unicompare", key="back_to_unicompare_superset_sidebar"):
            st.session_state.page = "Unicompare"

def process_superset(data, keywords):
    def contains_keywords(text):
        if isinstance(text, str):
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    return True
        return False

    outcome_dict = {}

    for i, row in data.iterrows():
        course_topic = row.get('Course Topic', '')  
        topic_outcome = row.get('Topic OutCome', '')  
        course_type = row.get('Course Type', '') 

        if contains_keywords(course_topic):
            if topic_outcome not in outcome_dict:
                outcome_dict[topic_outcome] = {'Course Topics': [], 'Course Types': set()}
            
            outcome_dict[topic_outcome]['Course Topics'].append(course_topic)
            outcome_dict[topic_outcome]['Course Types'].add(course_type)

    result = pd.DataFrame({
        "Course Topic": [", ".join(set(outcome_dict[outcome]['Course Topics'])) for outcome in outcome_dict],
        "Topic OutCome": list(outcome_dict.keys()),
        "Course Type": [", ".join(outcome_dict[outcome]['Course Types']) for outcome in outcome_dict]
    })

    return result
