from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Sum
from contributions.services.voterfocus import import_voter_focus_election_donations
from contributions.models import Contribution, Candidate, Contributor

# Create your views here.
def index(request):
    import_voter_focus_election_donations()
    all_contributions = Contribution.objects.all()
    return render(request, 'contributions/home.html', context={'all_contributions': all_contributions})

def contributions(request):
    all_contributions = Contribution.objects.all()
    zip_results = Contribution.objects.values('zip_number').order_by('-count').annotate(count=Count('zip_number'), sum=Sum('amount'))
    return render(request, 'contributions/contributions.html', context={'all_contributions': all_contributions, 'zip_codes':zip_results})

def candidates(request):
    all_contributions = Contribution.objects.all()
    candidate_total_contributions = Contribution.objects.values('candidate','candidate__name', 'amount').order_by('-amount').annotate(sum=Sum('amount'))
    return render(request, 'contributions/candidates.html', context={'candidate_total_contributions': candidate_total_contributions})

def contributors(request):
    all_contributors = Contributor.objects.all()
    return render(request, 'contributions/contributors.html', context={'all_contributors': all_contributors})
