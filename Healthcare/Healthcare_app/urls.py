from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicationViewSet,
    RegisterView,
    LoginView,
    PersonalInformationViewSet,
    MedicationTaskListCreate,
    UserMedicalInformationViewSet,
    LabRecordViewSet 
)

# Set up the router
router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'personal-info', PersonalInformationViewSet)
router.register(r'medical-info', UserMedicalInformationViewSet)
router.register(r'lab-records', LabRecordViewSet)  # Register lab records

urlpatterns = [
    path('', include(router.urls)),  # Remove the extra 'api/' prefix
    path('search-names/', MedicationViewSet.as_view({'get': 'search'}), name='medication-search'),
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('login/', LoginView.as_view(), name='login'),  # User login
    path('medication-tasks/', MedicationTaskListCreate.as_view(), name='medication-tasks'),  # List and create medication tasks
]
