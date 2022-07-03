from django.urls import path


from .views import UserRegisterView, UserView, UserViewDetail, LoginView


urlpatterns = [
    path('users/login/', LoginView.as_view()),
    path('users/register/', UserRegisterView.as_view()),
    path('users/', UserView.as_view()),
    path('users/<int:user_id>', UserViewDetail.as_view())
]
