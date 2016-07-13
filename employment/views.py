from django.shortcuts import render

# Create your views here.
from employment.models import JobPage, JobListing


def jobs_view(request, template="job_page.html"):

    jobpage = JobPage.objects.first()

    return render(request, template, dict(jobpage=jobpage))


def jobs_listing_view(request, slug, template="job_listing_page.html"):

    job = JobListing.objects.get(slug=slug)

    return render(request, template, dict(job=job))