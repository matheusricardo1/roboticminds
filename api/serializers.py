from rest_framework import serializers
from robotic.models import RoboticUser, Certificate, CertificateAssignment, Project, Event, UserProjectAssignment, UserEventAssignment

class RoboticUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoboticUser
        fields = ( 
            'id',
            'username', 
            'password',
            "email",
            "cpf",
            "registration",
            "birth_date",
            "level_access",
            "sex",
            'profile_picture',
            'full_name', 
            'mini_bio',
            'school',           
            'is_activated_by_admin',      
        )

class PublicRoboticUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoboticUser
        fields = ( 
            'id',
            'username', 
            "email",
            'profile_picture',
            'full_name', 
            'mini_bio',
        )



class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('id', 'name', 'details', 'start_date', 'end_date', 'city', 'hours')


class CertificateAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateAssignment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class UserProjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjectAssignment
        fields = '__all__'

class UserEventAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEventAssignment
        fields = '__all__'
