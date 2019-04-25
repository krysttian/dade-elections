from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    candidate_number = models.IntegerField(primary_key=True, unique=True)
    def __str__(self):
        return self.name

class Contributor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    occupation= models.CharField(max_length=30)
    type= models.CharField(max_length=30)
    address1= models.CharField(max_length=30)
    address2= models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    zip_number = models.IntegerField()
    date_created = models.DateTimeField()
    def __str__(self):
        return self.id

class Contribution(models.Model):
    type = models.CharField(max_length=20)
    date=models.DateField()
    contributor=models.ForeignKey(Contributor, on_delete=models.CASCADE)
    candidate_name=models.CharField(max_length=40)
    candidate=models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office=models.CharField(max_length=20)
    amount=models.IntegerField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    zip=models.CharField(max_length=20)
    zip_number = models.IntegerField()
    contribution_type=models.CharField(max_length=20)
    amend=models.CharField(max_length=20)
    date_created=models.DateTimeField()
    def __str__(self):
        return self.contributor
