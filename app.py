import sys
import os
import json

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import pandas as pd
from src.resume_processor import process_resumes
import plotly.express as px
from src.resume_processor import load_candidate_data_from_resumes
# from src.recommendation_system import recommend_candidates
from recommendation_system import recommend_candidates

# Function to save feedback to a JSON file
def save_feedback(feedback):
    feedback_file = "data/feedback.json"
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = {"feedback": []}
    
    feedback_data["feedback"].append(feedback)
    
    with open(feedback_file, 'w') as f:
        json.dump(feedback_data, f, indent=4)

# Function to calculate average feedback
def calculate_average_feedback():
    feedback_file = "data/feedback.json"
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedback_data = json.load(f)
        if feedback_data["feedback"]:
            average_feedback = sum(item['score'] for item in feedback_data["feedback"]) / len(feedback_data["feedback"])
            return average_feedback
    return None

def main():

    # Sidebar: Feedback Section
    st.sidebar.subheader("Feedback on Resume Relevance")

    # Select box for rating relevance
    feedback_option = st.sidebar.selectbox(
        "How relevant were the CVs overall?",
        ["Select an Option", "Very Relevant", "Somewhat Relevant", "Not Relevant"]
    )

    # Button to submit feedback
    if st.sidebar.button("Submit Feedback"):
        if feedback_option != "Select an Option":
            feedback = {
                "text": feedback_option,
                "score": {
                    "Very Relevant": 3,
                    "Somewhat Relevant": 2,
                    "Not Relevant": 1
                }[feedback_option]
            }
            save_feedback(feedback)
            st.sidebar.success("Thank you for your feedback!")
        else:
            st.sidebar.warning("Please select a feedback option before submitting.")


        # Show the average feedback score
    average_feedback = calculate_average_feedback()
    st.sidebar.subheader("Average Feedback Score")

    if average_feedback is not None:
        # Map numeric scores back to a rough interpretation if you'd like
        interpretation = (
            "High Relevance" if average_feedback >= 2.5
            else "Moderate Relevance" if average_feedback >= 1.5
            else "Low Relevance"
        )
        st.sidebar.write(f"{average_feedback:.2f} out of 3 ({interpretation})")
    else:
        st.sidebar.write("No feedback received yet.")           


    # Sidebar for help and instructions
    st.sidebar.title("Help")
    st.sidebar.markdown("""
    ### Steps to Use the Application
    1. **Upload Resumes**: Click on the "Upload Resumes" button to select the resumes you want to process.
    2. **Enter Job Description**: Fill in the job description for the position you are hiring for.
    3. **Specify Skills and Experience**: Enter relevant skills and experience required for the job.
    4. **Rank Resumes**: Click the "Rank Resumes" button to process the resumes and see the results.
    5. **Download Results**: Use the "Download Results" button to save the displayed results as a CSV file.
    """)

    # Toggle section for email templates
    st.sidebar.subheader("Email Templates")
    template_option = st.sidebar.selectbox("Select a Template", ["Select a Template", "Congratulation", "Interview Invitation"])

    # Predefined templates
    templates = {
        "Congratulation": "Dear {name},\n\nCongratulations! We are pleased to inform you that you have been selected for the next stage of the hiring process.\n\nBest regards,\n[Your Company Name]",
        "Interview Invitation": "Dear {name},\n\nWe are excited to invite you for an interview for the position you applied for. Please let us know your availability.\n\nBest regards,\n[Your Company Name]"
    }

    # Display the selected template
    if template_option in templates:
        st.sidebar.markdown("### Selected Template")
        st.sidebar.text_area("Template", templates[template_option], height=150)

    # Beautiful title
    st.title("🌟 AI-Powered Resume Ranking System 🌟")
    st.markdown("### Streamline your hiring process with AI!")

    # Input fields in the main area
    uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
    job_description = st.text_area("Job Description", placeholder="Enter the job description here...")
    skills = st.text_input("Relevant Skills (comma-separated)", placeholder="e.g., Python, Machine Learning")
    experience = st.text_input("Relevant Experience (comma-separated)", placeholder="e.g., 5 years in software development")

    candidate_data = None  # Initialize candidate_data to None

    # if st.button("Load Candidates"):
    #     if uploaded_files:
    #         # Load candidate data from uploaded resumes
    #         candidate_data = load_candidate_data_from_resumes(uploaded_files)
    #         st.subheader("Candidate Profiles")
    #         st.dataframe(candidate_data)
    #     else:
    #         st.error("Please upload at least one resume.")

    # Button to process resumes
    if st.button("Rank Resumes"):
        if uploaded_files and job_description:
            # Save uploaded resumes to the data directory
            for uploaded_file in uploaded_files:
                with open(os.path.join("data", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Process resumes and rank them
            rankings, resume_data = process_resumes(uploaded_files, job_description, skills, experience)

            # Convert rankings to a DataFrame for better presentation
            rankings_df = pd.DataFrame(rankings.items(), columns=['Resume Name', 'Similarity Score'])
            rankings_df['Similarity Score'] = rankings_df['Similarity Score'].apply(lambda x: f"{x:.2%}")  # Format as percentage

            # Display the rankings in a structured table
            st.subheader("Ranking Results")
            st.dataframe(rankings_df.style.highlight_max(axis=0))

            # Present contact information in a table
            contact_info = []
            for resume_name, data in resume_data.items():
                contact_info.append({
                    "Resume Name": resume_name,
                    "Emails": ', '.join(data['emails']) if data['emails'] else "N/A",
                    "Phones": ', '.join(data['phones']) if data['phones'] else "N/A",
                    "Name": data.get('name', 'N/A'),  # Assuming name is part of the data
                    "Similarity Score": f"{rankings[resume_name]:.2%}",
                    "Resume": data.get('resume_text', 'N/A')  # Assuming resume text is part of the data
                })

            # Create a DataFrame for contact information
            contact_df = pd.DataFrame(contact_info)
            st.subheader("Contact Information")
            st.table(contact_df)

            # Explanation of Similarity Scores
            st.markdown("### Understanding Similarity Scores")
            st.write("The similarity score indicates how closely each resume matches the job description. A higher score means a better fit for the position.")
            st.write("For example:")
            st.write("- A score of **80%** means the resume is a strong match for the job description.")
            st.write("- A score of **50%** indicates a moderate match, while a score below **30%** suggests the resume may not be suitable.")

            # Create a bar chart for similarity scores
            rankings_df['Similarity Score Numeric'] = rankings_df['Similarity Score'].str.rstrip('%').astype(float)

            # Calculate irrelevant CVs
            irrelevant_count = (rankings_df['Similarity Score Numeric'] < 30).sum()  # Assuming <30% is irrelevant

            # Create the bar chart
            fig = px.bar(rankings_df, x='Resume Name', y='Similarity Score Numeric',
                         title='Similarity Scores of Resumes',
                         labels={'Similarity Score Numeric': 'Similarity Score (%)'},
                         color='Similarity Score Numeric',
                         color_continuous_scale=px.colors.sequential.Viridis)

            # Add a bar for irrelevant CVs
            if irrelevant_count > 0:
                fig.add_bar(x=['Irrelevant CVs'], y=[irrelevant_count], 
                             marker_color='red', name='Irrelevant CVs')

            st.plotly_chart(fig)

            # Candidate Profile Selection
            if candidate_data is not None:  # Check if candidate_data is loaded
                st.subheader("View Candidate Profile")
                selected_candidate = st.selectbox("Select a Candidate", options=contact_df['Name'].tolist())

                # Display selected candidate's details
                if selected_candidate:
                    candidate_details = contact_df[contact_df['Name'] == selected_candidate].iloc[0]
                    st.markdown(f"### Profile for {selected_candidate}")
                    st.write(f"**Skills:** {candidate_details['Skills']}")
                    st.write(f"**Qualifications:** {candidate_details['Qualifications']}")  # Display qualifications

                    # Get recommendations based on the selected candidate
                    candidate_index = contact_df.index[contact_df['Name'] == selected_candidate][0]
                    recommendations = recommend_candidates(candidate_data, candidate_index)

                    # Visualization of Recommendations
                    st.subheader("Recommended Candidates")
                    st.table(recommendations[['Name', 'Skills', 'Qualifications']])  # Show new structure

                    # Visualize similarity scores
                    similarity_scores = recommendations['Similarity Score']  # Assuming you have this in your recommendations
                    fig = px.bar(recommendations, x='Name', y='Similarity Score', title='Similarity Scores of Recommended Candidates')
                    st.plotly_chart(fig)

            # Download Results Button
            if st.button("Download Results"):
                # Save the results to a CSV file
                results_file = "resume_rankings.csv"
                rankings_df.to_csv(results_file, index=False)
                st.success(f"Results saved as {results_file}. You can download it from the file explorer.")

        else:
            st.error("Please upload resumes and provide a job description.")

    # Button to process resumes and recommend candidates
    if st.button("Recommend Candidates"):
        st.write("Candidate Data:", candidate_data)
        st.write("Job Description:", job_description)
        if candidate_data is not None and not candidate_data.empty and job_description:
            recommended_candidate = recommend_candidates(candidate_data, candidate_index)
            st.subheader("Recommended Candidate")
            st.dataframe(recommended_candidate)

            # Display the name of the top-ranked candidate
            top_candidate_name = recommended_candidate.iloc[0]['Name']  # Assuming 'Name' is the column for candidate names
            st.success(f"The top-ranked candidate is: **{top_candidate_name}**")

            # Feedback input in the sidebar
            st.sidebar.subheader("Feedback Section")

            # Text input for detailed feedback
            feedback_text = st.sidebar.text_input("Please provide your feedback on the recommendations:")

            # Select options for feedback
            feedback_options = st.sidebar.selectbox("How relevant were the recommendations?", 
                                                     ["Select an Option", "Very Relevant", "Somewhat Relevant", "Not Relevant"])

            if st.sidebar.button("Submit Feedback"):
                if feedback_text or feedback_options != "Select an Option":
                    feedback = {
                        "text": feedback_text,
                        "score": {"Very Relevant": 3, "Somewhat Relevant": 2, "Not Relevant": 1}[feedback_options]
                    }
                    save_feedback(feedback)
                    st.sidebar.success("Thank you for your feedback!")
                else:
                    st.sidebar.warning("Please enter some feedback before submitting.")

    # Display average feedback
    average_feedback = calculate_average_feedback()
    if average_feedback is not None:
        st.sidebar.subheader("Average Feedback Score")
        st.sidebar.write(f"{average_feedback:.2f} out of 3")
    else:
        st.sidebar.subheader("Average Feedback Score")
        st.sidebar.write("No feedback received yet.")

if __name__ == "__main__":
    main()
