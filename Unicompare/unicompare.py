import streamlit as st
import pandas as pd

def unicompare(data):
    st.title("Unicompare")

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    if 'page' not in st.session_state:
        st.session_state.page = "Unicompare"

    data['Country'] = data['Country'].astype(str)
    data['State'] = data['State'].astype(str)

    country = st.selectbox("Country", ["All"] + sorted(data['Country'].unique().tolist()), key="country")

    if country == "All":
        state_options = ["All"] + sorted(data['State'].unique().tolist())
    else:
        state_options = ["All"] + sorted(data[data['Country'] == country]['State'].unique().tolist())
    
    state = st.selectbox("State", state_options, key="state")

    filtered_data = data[
        ((data['Country'] == country) | (country == "All")) &
        ((data['State'] == state) | (state == "All"))
    ]

    unique_course_types = filtered_data['Course Type'].unique().tolist()
    if not unique_course_types:
        unique_course_types = ["All"]
    course_type_options = {course: course for course in unique_course_types}
    course_type_options = {**{"All": "All"}, **course_type_options}  # Include "All" option

    course_type_display = st.selectbox("Course Type", list(course_type_options.keys()), key="course_type")

    selected_course_type = course_type_options[course_type_display]

    filtered_data = filtered_data[
        (filtered_data['Course Type'] == selected_course_type) | (selected_course_type == "All")
    ]

    unique_outcomes_count = filtered_data['Topic OutCome'].nunique()
    st.write(f"### Found {unique_outcomes_count} unique Courses")

    page_size = 15
    total_pages = (len(filtered_data) - 1) // page_size + 1
    start_idx = st.session_state.page_number * page_size
    end_idx = start_idx + page_size
    paginated_data = filtered_data.iloc[start_idx:end_idx]
    st.write(f"Displaying rows {start_idx + 1} to {end_idx} of {len(filtered_data)}")

    st.markdown("""
        <style>
            .dataframe {
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write(paginated_data.to_html(escape=False, index=False, classes='dataframe'), unsafe_allow_html=True)

    with st.sidebar:
        st.header("Navigation & Actions")

        if st.button("◀️ Previous Page") and st.session_state.page_number > 0:
            st.session_state.page_number -= 1
        if st.button("Next Page ▶️") and st.session_state.page_number < total_pages - 1:
            st.session_state.page_number += 1

        if st.button("Create Superset of Course Structures"):
            st.session_state.page = "Superset"
            st.session_state.superset_data = filtered_data


        if st.button("Back to Home Page"):
            st.session_state.page = "Home"

if __name__ == "__main__":
    data = pd.read_csv('data/Final dataset.csv')
    unicompare(data)
