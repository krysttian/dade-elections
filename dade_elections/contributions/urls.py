from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers, serializers, viewsets
from contributions.models import Contribution, Candidate, Contributor
from contributions.views import (
    index,
    contributions,
    contributors,
    candidates
)

app_name = "contributions"

# Serializers define the API representation.
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        # fields = ('name', 'date_created', 'candidate_number')

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('__all__')

class ContributionSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(many=False, read_only=True)
    contributor = ContributorSerializer(many=False, read_only=True)
    class Meta:
        model = Contribution
        fields = ('__all__')

# ViewSets define the view behavior.
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'contributions', ContributionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'contributors', ContributorViewSet)

urlpatterns = [
    path("", index, name="home"),
    path("contributions", contributions, name="contributions"),
    path("candidates", candidates, name="candidates"),
    path("api/", include(router.urls)),
    # path("", view=index, name="index"),
]
