from django.urls import path

from contributions.views import (
    index,
)

app_name = "contributions"
urlpatterns = [
    path("", view=index, name="index"),
]
