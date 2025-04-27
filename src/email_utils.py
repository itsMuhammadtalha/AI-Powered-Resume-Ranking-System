def create_rejection_email_link(emails):
    # Join the emails into a comma-separated string
    to_emails = ', '.join(emails)
    
    # Define the subject and body of the email
    subject = "Application Status"
    body = "We will not be moving forward with your application. Thanks for applying!"
    
    # Create the mailto link
    mailto_link = f"mailto:{to_emails}?subject={subject}&body={body}"
    
    return mailto_link
