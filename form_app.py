import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("AIGH Bug Reporting Structure")
st.markdown("Enter the details of the bug found here.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="AIGH", usecols=list(range(9)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Bugs
APP_TYPE = [
    "News to Video",
    "Trends to Video",
]
ISSUE = [
    "Loop Related",
    "Community Related",
]

# Entering new bug details
with st.form(key="aigh_form"):
    publication_date = st.text_input(label="Publication Date*")
    app_type = st.selectbox("App Type*", options=APP_TYPE, index=None)
    issue = st.multiselect("Issue Relation", options=ISSUE)
    news_title = st.text_input(label="News Title")
    date_of_issue = st.date_input(label="Date when issue occurred")
    time_of_issue = st.text_input(label="Time when issue occured")
    issue_description = st.text_area(label="Description of issue")
    Loop_Community_Name_wanted_to_search = st.text_input(label="Loop/Community Name wanted to search")
    Loop_Community_Description_wanted_to_search = st.text_input(label="Loop/Community Description wanted to search")


    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Bug Details")

     # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not publication_date or not app_type:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        # elif existing_data["NewsTitle"].str.contains(str(news_title)).any():
        #     st.warning("A bug with same news title already exists")
        #     st.stop()
        else:
            # Create a new row of bug details
            bugs_data = pd.DataFrame(
                [
                    {
                        "PublicationDate": publication_date,
                        "AppType": app_type,
                        "IssueRelation": ", ".join(issue),
                        "NewsTitle": news_title,
                        "DateofIssue": date_of_issue.strftime("%Y-%m-%d"),
                        "TimeofIssue": time_of_issue,
                        "IssueDescription": issue_description,
                        "Loop/Community Name wanted to search": Loop_Community_Name_wanted_to_search,
                        "Loop/Community Description wanted to search": Loop_Community_Description_wanted_to_search,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, bugs_data], ignore_index=True)

            # Update Google Sheets with the new bug data
            conn.update(worksheet="AIGH", data=updated_df)

            st.success("Bug details successfully submitted to the QA Team!")