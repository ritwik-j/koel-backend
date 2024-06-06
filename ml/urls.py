from django.urls import path
from . import views as v

urlpatterns = [
    path("predict_image", v.PredictImageView.as_view()),
    path("predict_audio", v.PredictAudioView.as_view()),
]