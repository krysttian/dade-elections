from django.shortcuts import render
from django.http import HttpResponse
from contributions.services.voterfocus import import_voter_focus_election_donations
# Create your views here.
def index(request):
    import_voter_focus_election_donations()
    return HttpResponse("You're looking at question")
