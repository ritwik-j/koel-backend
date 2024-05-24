from django.urls import path
from . import views as v

urlpatterns = [
    path("predict", v.PredictView.as_view()),
]