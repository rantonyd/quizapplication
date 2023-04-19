from django.urls import path
from quizweb import views



urlpatterns=[
    path("login",views.SignInView.as_view(),name="signup"),
    path("register",views.SignUpView.as_view(),name="signin"),
    path("home",views.HomeView.as_view(),name="home"),
    path("home/quiz",views.QuizHome.as_view(),name="quiz-home"),
    path("questions/all/<str:cat>/<str:mode>/",views.QuestionList.as_view(),name="question-list"),
    path("questions/record",views.QuizrecordView.as_view(),name="quiz-record"),
    path("",views.IndexView.as_view(),name="index"),
    path("signout",views.signout_view,name="signout"),
]