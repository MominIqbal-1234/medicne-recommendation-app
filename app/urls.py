

from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
urlpatterns = [
      path('',views.Login.as_view(),name=''),
      path('signup',views.Signup.as_view(),name='signup'),
      path('home',views.Home.as_view(),name='home'),
      path('medicine_recommendation',views.MedicineRecommendation.as_view(),name='medicine_recommendation'),
      path('predicted_disease',views.PredictedDisease.as_view(),name='predicted_disease'),
      path('description',views.Description.as_view(),name='description'),
      path('precautions',views.Precautions.as_view(),name='precautions'),
      path('medications',views.Medications.as_view(),name='medications'),
      path('diets',views.Diets.as_view(),name='diets'),
      path('workout',views.Workout.as_view(),name='workout'),
      path('disease_list_dataset',views.DiseaseListDataset.as_view(),name='disease_list_dataset'),
      path('matrix/<str:model_name>',views.Matrix.as_view(),name='matrix'),
      path('logout',views.Logout.as_view(),name='logout'),
      path('ModelTrainingResults',views.ModelTrainingResults.as_view(),name='ModelTrainingResults'),
      path('total_number_of_unique_disease',views.TotalNumberofUniqueDisease.as_view(),name='total_number_of_unique_disease'),
]
        