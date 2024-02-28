from django.urls import path
from .views import *

urlpatterns = [
    path('', Dashboard, name='dashboard'),
    path('facebook-instagram/', facebook_instagram, name='facebook_instagram'),
    path('google/', google, name='google'),
    path('tiktok/', tiktok, name='tiktok'),
    path('youtube/', youtube, name='youtube'),
    path('save_visitor/', save_visitor, name='save_visitor'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('subscription_limit/', subscription_limit, name='subscription_limit'),
    path('logout/', logout_view, name='logout'),
    path('subscribe/', subscription_form, name='subscribe'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
    path('success', success, name='success'),
]
