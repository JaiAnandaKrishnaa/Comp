import streamlit as st
import pandas as pd

def add_course(data):
    st.title("📚 Add a New Course")

    st.markdown("""
        <style>
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        .info {
            font-size: 18px;
            color: #555;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'course_structures' not in st.session_state:
        st.session_state.course_structures = []
    if 'topic_count' not in st.session_state:
        st.session_state.topic_count = 1
    if 'reset' not in st.session_state:
        st.session_state.reset = False
    if 'editing_mode' not in st.session_state:
        st.session_state.editing_mode = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "add_course"
    if 'recently_uploaded_course' not in st.session_state:
        st.session_state.recently_uploaded_course = pd.DataFrame()

    if 'course_name' not in st.session_state:
        st.session_state.course_name = ""
    if 'course_type' not in st.session_state:
        st.session_state.course_type = "Workshop"
    if 'university_name' not in st.session_state:
        st.session_state.university_name = ""
    if 'fees' not in st.session_state:
        st.session_state.fees = 0
    if 'country' not in st.session_state:
        st.session_state.country = ""
    if 'state' not in st.session_state:
        st.session_state.state = ""
    if 'website_link' not in st.session_state:
        st.session_state.website_link = ""

    if st.session_state.current_page == "add_course":
        st.subheader("Course Details")
        with st.expander("Course Information"):
            course_name = st.text_input("Course Name", value=st.session_state.course_name, key="course_name")
            course_type = st.selectbox("Course Type", ["Workshop", "Short Term Course", "Certificate", "Diploma", "Degree Course"], 
                                       index=["Workshop", "Short Term Course", "Certificate", "Diploma", "Degree Course"].index(st.session_state.course_type), key="course_type")
            university_name = st.text_input("University Name", value=st.session_state.university_name, key="university_name")
            fees = st.number_input("Fees Structure (in rupees)", min_value=0, step=1, value=st.session_state.fees, key="fees")
            country = st.text_input("Country", value=st.session_state.country, key="country")
            state = st.text_input("State", value=st.session_state.state, key="state")
            website_link = st.text_input("Website Link", value=st.session_state.website_link, key="website_link")

        st.subheader("Course Topics")
        with st.expander("Add Course Topics"):
            topic_name = st.text_area(f"Course Topic {st.session_state.topic_count}", key=f"topic_name_{st.session_state.topic_count}")

            if topic_name:
                topic_duration = st.number_input(f"Duration for Topic {st.session_state.topic_count} (in hours)", min_value=1, step=1, key=f'duration_{st.session_state.topic_count}')
                topic_outcome = st.text_area(f"Outcome for Topic {st.session_state.topic_count}", key=f'outcome_{st.session_state.topic_count}')
                topic_delivery_mode = st.selectbox(f"Delivery Mode for Topic {st.session_state.topic_count}", ["Online", "Offline", "Hybrid"], key=f'delivery_mode_{st.session_state.topic_count}')

                if st.button(f"Submit Topic {st.session_state.topic_count}", key=f"submit_topic_{st.session_state.topic_count}"):
                    st.session_state.course_structures.append({
                        "Course Topic": f"{st.session_state.topic_count}. {topic_name}",
                        "Duration for Each Course (in hours)": topic_duration,
                        "Topic OutCome": f"{st.session_state.topic_count}. {topic_outcome}",
                        "Topic Delivery Model": f"{st.session_state.topic_count}. {topic_delivery_mode}"
                    })
                    st.session_state.topic_count += 1

        if st.button("No more topics", key="no_more_topics"):
            if not course_name or not university_name or fees <= 0 or not country or not state or not website_link or not st.session_state.course_structures:
                st.error("Please fill out all the required fields and add at least one course topic before submitting.")
            else:
                total_duration = sum(item["Duration for Each Course (in hours)"] for item in st.session_state.course_structures)

                new_courses = []
                for structure in st.session_state.course_structures:
                    new_course = {
                        "Course Name": course_name,
                        "Course Type": course_type,
                        "University Name": university_name,
                        "Fees Structure(in rupees)": fees,
                        "Country": country,
                        "State": state,
                        "Website Link": website_link,
                        "Duration(in hours)": total_duration,
                        **structure
                    }
                    new_courses.append(new_course)

                new_courses_df = pd.DataFrame(new_courses)
                data = pd.concat([data, new_courses_df], ignore_index=True)
                data.to_csv('data/Final dataset.csv', index=False)
                st.session_state.recently_uploaded_course = new_courses_df
                st.success("Courses added successfully!")

                for key in ['course_name', 'course_type', 'university_name', 'fees', 'country', 'state', 'website_link', 'course_structures', 'topic_count']:
                    if key in st.session_state:
                        del st.session_state[key]


        if st.button("Back to Home"):
            st.session_state.page = "Home"

        st.sidebar.header("Manage Courses")
        if st.sidebar.button("View Uploaded Courses"):
            st.session_state.current_page = "view_courses"

        if st.sidebar.button("Edit Uploaded Courses"):
            st.session_state.editing_mode = True
            st.session_state.current_page = "edit_courses"

        if st.sidebar.button("View Prev added Courses"):
            st.session_state.current_page = "view_prev_courses"


    elif st.session_state.current_page == "view_courses":
        st.title("📋 Recently Uploaded Courses")
        if not st.session_state.recently_uploaded_course.empty:
            st.write("### Recently Uploaded Courses")
            st.write(st.session_state.recently_uploaded_course.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.warning("No recently uploaded courses to display.")

        if st.button("Back to Add Course"):
            st.session_state.current_page = "add_course"

    elif st.session_state.current_page == "edit_courses":
        st.write("### Edit Recently Uploaded Courses")
        if not st.session_state.recently_uploaded_course.empty:
            edited_courses_df = st.session_state.recently_uploaded_course.copy()

            for index, row in edited_courses_df.iterrows():
                st.write(f"#### Course {index + 1}")
                cols = st.columns(len(edited_courses_df.columns))
                for col, column_name in zip(cols, edited_courses_df.columns):
                    new_value = col.text_input(f"{column_name}", value=str(row[column_name]), key=f"{column_name}_{index}")
                    if column_name == "Duration for Each Course (in hours)":
                        new_value = int(new_value) if new_value.isdigit() else row[column_name]
                    edited_courses_df.at[index, column_name] = new_value

            if st.button("Save Changes"):
                edited_courses_df['Duration(in hours)'] = edited_courses_df['Duration for Each Course (in hours)'].sum()

                data = pd.concat([data, edited_courses_df], ignore_index=True)
                data.to_csv('data/Final dataset.csv', index=False)
                st.session_state.recently_uploaded_course = edited_courses_df
                st.success("Courses edited and saved successfully!")

        else:
            st.warning("No recently uploaded courses to edit.")

        if st.button("Back to Add Course"):
            st.session_state.current_page = "add_course"

    elif st.session_state.current_page == "view_prev_courses":
        st.title("📚 Previously Added Courses")

        page_size = 10
        page_number = st.number_input("Page number", min_value=1, max_value=(len(data) // page_size) + 1, step=1)

        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size

        paginated_data = data.iloc[start_idx:end_idx]

        if paginated_data.empty:
            st.warning("No previous courses to display.")
        else:
            st.write("### Previously Added Courses")
            st.write(paginated_data.to_html(escape=False, index=False), unsafe_allow_html=True)

        if st.button("Back to Add Course"):
            st.session_state.current_page = "add_course"
