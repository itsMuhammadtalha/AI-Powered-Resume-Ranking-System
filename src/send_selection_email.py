def generate_selection_email(candidate_name, candidate_email, candidate_phone):
    # Create the personalized message
    subject = "Application Status Update"
    body = f"Hi {candidate_name},\n\nCongratulations! We are pleased to inform you that we will be moving forward with your application. We appreciate your interest in the position and look forward to discussing the next steps with you.\n\nBest regards,\n[Your Company Name]\nContact: {candidate_phone}"
    
    # Create the mailto link
    mailto_link = f"mailto:{candidate_email}?subject={subject}&body={body}"
    
    return subject, body, mailto_link 