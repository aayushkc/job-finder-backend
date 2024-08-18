from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q, Count
from recruiter.models import Job, JobRequest
from datetime import datetime
def recommend_jobs_for_seeker(seeker):
    # Get seeker's preferences and qualifications
    seeker_industry = seeker.seeker.seeker_details.industry
    seeker_skills = seeker.seeker.seeker_details.skills.values_list('title', flat=True)
    seeker_preferred_jobs = seeker.seeker.seeker_details.prefferd_job.values_list('title', flat=True)

    # Filter jobs based on seeker's industry and preferred job categories
    applied_job_pks = JobRequest.objects.filter(job_seeker=seeker.seeker).values_list('job__pk', flat=True)
    jobs_queryset = Job.objects.filter(
       Q(industry=seeker_industry) | Q(required_skills__title__in=seeker_skills) | Q(job_category__title__in=seeker_preferred_jobs),is_job_approved=True
    ).distinct().exclude(pk__in = applied_job_pks).annotate(job_request_count=Count('job_request')).select_related('industry','quiz','company__recruiter_details').prefetch_related('required_skills','job_category','education_info')

    if not jobs_queryset:
        return []

    job_features = []
    for job in jobs_queryset:
        skills_text = ', '.join(job.required_skills.values_list('title', flat=True))
        job_categories_text = ', '.join(job.job_category.values_list('title', flat=True))
        combined_text = f"{skills_text} {job_categories_text}"  # Combine skills and job categories
        job_features.append(combined_text)

    # Vectorize features using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    job_feature_vectors = tfidf_vectorizer.fit_transform(job_features)

    seeker_features = [f"{', '.join(seeker_skills)} {', '.join(seeker_preferred_jobs)}"]
    seeker_vector = tfidf_vectorizer.transform(seeker_features)
    
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(seeker_vector, job_feature_vectors).flatten()
    
    # Get indices of top-N most similar jobs
    top_n = 100
    similar_jobs_indices = similarity_matrix.argsort()[::-1][:top_n].tolist()  # Exclude the job itself
    


    recommended_jobs = [jobs_queryset[int(index)] for index in similar_jobs_indices]
   
    recommended_jobs.sort(key=lambda job: (job.apply_before < datetime.now().date()))

    return recommended_jobs

