from django.urls import include, path
from . import views

urlpatterns = [

    path('', views.job_list),
    path('all', views.job_list),
    path('<int:id>', views.job_detail),
    path('problems1', views.Add_Sub_Problems),
    path('math_problem1', views.math_problem1),
    path('math_problem22', views.math_problem2),
    path('math_problem3', views.math_problem3),
]