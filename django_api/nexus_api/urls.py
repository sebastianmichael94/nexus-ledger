from django.contrib import admin
from django.urls import path
from ledger.views import get_user_profile  # This imports the Motor-based logic

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This creates the endpoint: http://127.0.0.1:8000/profile/USER_001/
    # <str:user_id> captures the ID from the URL and sends it to the view
    path('profile/<str:user_id>/', get_user_profile),
]