from backend.models import JobSeeker
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """ Replaces the social.pipeline.user.create_user function for valid email check
    """
    print(user)
    if user:
        return
    user = strategy.create_user(email=details['email'], username=details['username'],is_seeker=True)
    JobSeeker.objects.create(user=user)
    return {
        'user': user
    }