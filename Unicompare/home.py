import streamlit as st

def home():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(to right, #f8f9fa, #e9ecef);
                font-family: 'Helvetica Neue', sans-serif;
            }
            .header {
                text-align: center;
                color: #4A90E2;
                margin-bottom: 20px;
            }
            .course-card {
                border: 1px solid #4A90E2;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                text-align: center;
                transition: transform 0.2s;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .course-card:hover {
                transform: scale(1.05);
                background-color: #f0f8ff;
            }
            .button {
                background-color: #4A90E2;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                text-align: center;
                display: inline-block;
                transition: background-color 0.3s;
                margin-top: 20px;
                text-decoration: none;
                font-weight: bold;
            }
            .button:hover {
                background-color: #357ABD;
            }
            .button-container {
                text-align: center;
            }
            .expander-header {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            .expander-header:hover {
                background-color: #357ABD;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='header'>Welcome to Unicompare</h1>", unsafe_allow_html=True)
    st.write(""" #### This web app allows you to search and compare university courses based on various filters. Click on the button below to get started.
    """)

    st.write("### Course Types")
    st.write("Here are a few course types along with their descriptions:")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        with st.expander("Workshop", expanded=False):
            st.markdown("<div class='course-card'><h4>Workshop</h4><p>Short-term, intensive sessions focused on a specific skill or topic, typically lasting from a few hours to a few days (0 - 10 hours).</p></div>", unsafe_allow_html=True)

    with col2:
        with st.expander("Short Term Course", expanded=False):
            st.markdown("<div class='course-card'><h4>Short Term Course</h4><p>Courses that provide in-depth knowledge or skills on a particular subject, usually lasting from a few days to several weeks (10.5 - 45 hours).</p></div>", unsafe_allow_html=True)

    with col3:
        with st.expander("Certificate", expanded=False):
            st.markdown("<div class='course-card'><h4>Certificate</h4><p>Programs that offer specialized training and education, often for professional development, ranging from a few weeks to several months (45 - 300 hours).</p></div>", unsafe_allow_html=True)

    with col4:
        with st.expander("Diploma", expanded=False):
            st.markdown("<div class='course-card'><h4>Diploma</h4><p>Comprehensive programs that cover a broad area of study, typically lasting from a few months to a year or more (301 - 780 hours).</p></div>", unsafe_allow_html=True)

    with col5:
        with st.expander("Degree Course", expanded=False):
            st.markdown("<div class='course-card'><h4>Degree Course</h4><p>Extensive programs that lead to a degree, covering a wide range of subjects and skills, usually spanning several years (781 - 8000 hours).</p></div>", unsafe_allow_html=True)

    st.write("### Get Started with Adding or Comparing Courses")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add a New Course", key="add_course", help="Click to add a new course"):
            st.session_state.page = "Add Course"

    with col2:
        if st.button("Choose and Compare Courses", key="search_and_compare", help="Click to search and compare courses"):
            st.session_state.page = "Unicompare"
