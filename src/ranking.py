# src/ranking.py
def rank_resumes(resume_data, job_description, skills, experience):
    rankings = {}
    
    # Tokenize job description and skills
    job_tokens = tokenize(job_description)
    skill_tokens = tokenize(skills)

    for resume_name, data in resume_data.items():
        # Calculate similarity score
        similarity_score = calculate_similarity(data["text"], job_description)

        # Calculate skill relevance score
        skill_relevance = sum(1 for token in data['tokens'] if token in skill_tokens)

        # Calculate experience score (assuming experience is provided in the input)
        experience_score = 0
        if experience:
            experience_list = [int(exp.split()[0]) for exp in experience.split(',') if exp.isdigit()]
            experience_score = sum(experience_list) / len(experience_list) if experience_list else 0

        # Combine scores (you can adjust the weights as needed)
        total_score = (similarity_score * 0.5) + (skill_relevance * 0.3) + (experience_score * 0.2)
        rankings[resume_name] = total_score

    # Sort rankings based on total score
    sorted_rankings = dict(sorted(rankings.items(), key=lambda item: item[1], reverse=True))
    return sorted_rankings