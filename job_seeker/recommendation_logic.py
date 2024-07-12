from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q
from recruiter.models import Job
def recommend_jobs_for_seeker(seeker):
    # Get seeker's preferences and qualifications
    seeker_industry = seeker.seeker.seeker_details.industry
    seeker_skills = seeker.seeker.seeker_details.skills.all()
    seeker_preferred_jobs = seeker.seeker.seeker_details.prefferd_job.all()

    # Filter jobs based on seeker's industry and preferred job categories
    jobs_queryset = Job.objects.filter(
        Q(industry=seeker_industry) | Q(job_category__in=seeker_preferred_jobs),is_job_approved=True
    ).distinct()

    if not jobs_queryset:
        return []

    job_features = []
    for job in jobs_queryset:
        skills_text = ', '.join(job.required_skills.values_list('title', flat=True))
        job_categories_text = ', '.join(job.job_category.values_list('title', flat=True))
        combined_text = f"{skills_text} {job_categories_text}"  # Combine skills and job categories
        job_features.append(combined_text)

    print("Featuresssssssssssssssssssssssss",job_features)
    # Vectorize features using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    job_feature_vectors = tfidf_vectorizer.fit_transform(job_features)

    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(job_feature_vectors, job_feature_vectors)
    
    # Get indices of top-N most similar jobs
    top_n = 100
    similar_jobs_indices = similarity_matrix.argsort()[:, ::-1][:, 0:top_n+1]  # Exclude the job itself

   
   
        
    similar_jobs_indices_list = similar_jobs_indices.tolist()
    
    # Get recommended jobs for each job listing
    # recommended_jobs = []
    # for indices in similar_jobs_indices_list:
            
    #         jobs = [jobs_queryset[index] for index in indices]
    #         recommended_jobs.append(jobs)

    flat_recommended_jobs_indices = {index for sublist in similar_jobs_indices_list for index in sublist}
    
    recommended_jobs = [jobs_queryset[index] for index in flat_recommended_jobs_indices]
    return recommended_jobs

