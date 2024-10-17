from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Medication, PersonalInformation, MedicationTask, UserMedicalInformation, LabRecord
from .serializers import (
    MedicationSerializer, 
    MedicationDetailSerializer, 
    UserSerializer, 
    RegisterSerializer, 
    PersonalInformationSerializer, 
    MedicationTaskSerializer, 
    UserMedicalInformationSerializer, 
    LabRecordSerializer
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

    
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('q', None)
        if query:
            medications = Medication.objects.filter(
                medicine_name__icontains=query
            )[:15]

            unique_meds = {med.medicine_name: med.id for med in medications}

            response_data = [
                {"id": unique_meds[name], "medicine_name": name} 
                for name in unique_meds
            ]
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='details/(?P<name>[^/.]+)')
    def medication_details(self, request, name=None):
        # Filter by medicine_name (case-insensitive) to find the specific medication
        medication = Medication.objects.filter(medicine_name__iexact=name).first()  
        if medication:
            serializer = MedicationDetailSerializer(medication)  # Serialize the single match
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()


        PersonalInformation.objects.create(
            user=user,
            first_name='',  
            last_name='',
            gender='',
            email=user.email, 
            phone_number='',
            address='',
            city='',
            state='',
            date_of_birth=None,
            age=None
        )

        UserMedicalInformation.objects.create(
            user=user,
            blood_group='',  
            weight=None,
            height=None,
            allergies='',
            medical_conditions='',
            blood_pressure='',
            blood_sugar_fasting=None,
            blood_sugar_postprandial=None,
            cholesterol_ldl=None,
            cholesterol_hdl=None,
            bmi=None,
            disabilities=''
        )



class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class PersonalInformationViewSet(viewsets.ModelViewSet):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalInformationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return PersonalInformation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()  # No need to pass user again since it's already linked

    
class UserMedicalInformationViewSet(viewsets.ModelViewSet):
    queryset = UserMedicalInformation.objects.all()
    serializer_class = UserMedicalInformationSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        return UserMedicalInformation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save the medical info with the logged-in user

    def perform_update(self, serializer):
        serializer.save()  # No need to pass user again since it's already linked


class MedicationTaskListCreate(generics.ListCreateAPIView):
    queryset = MedicationTask.objects.all()
    serializer_class = MedicationTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicationTask.objects.filter(user=self.request.user)  # Filter tasks by user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class LabRecordViewSet(viewsets.ModelViewSet):
    queryset = LabRecord.objects.all()
    serializer_class = LabRecordSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        # Filter lab records by the logged-in user
        return LabRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the new record to the logged-in user
        serializer.save(user=self.request.user)