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
    path('success1', success1, name='success1'),

    path('updatecard/', update_card, name='update_card'),
    path('Profile/', Profile, name='profile'),
    path('change-name/', change_name, name='change_name'),
    path('change-password/', change_password, name='change_password'),

    path('get_categories/', get_categories, name='get_categories'),
    path('admin_category_dropdown/', admin_category_dropdown, name='admin_category_dropdown'),

    path('Location/', Location, name='Location'),
]
