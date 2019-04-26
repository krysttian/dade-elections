from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    candidate_number = models.IntegerField(primary_key=True, unique=True)
    def __str__(self):
        return self.name

class Contributor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    occupation= models.CharField(max_length=100)
    type= models.CharField(max_length=100)
    address1= models.CharField(max_length=100, null=True)
    address2= models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    zip_number = models.IntegerField()
    date_created = models.DateTimeField()
    def __str__(self):
        return self.id

class Contribution(models.Model):
    type = models.CharField(max_length=80)
    date=models.DateField()
    contributor=models.ForeignKey(Contributor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    occupation= models.CharField(max_length=100, null=True)
    candidate_name=models.CharField(max_length=100)
    candidate=models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    address1= models.CharField(max_length=100, null=True)
    address2= models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    zip_number = models.IntegerField()
    contribution_type=models.CharField(max_length=100)
    amend=models.CharField(max_length=100, null=True)
    date_created=models.DateTimeField()
    def __str__(self):
        return self.contributor
