from rest_framework import serializers
from robotic.models import RoboticUser, Certificate, CertificateAssignment


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


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('id', 'name', 'details', 'start_date', 'end_date', 'city', 'hours')


class CertificateAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CertificateAssignment
        fields = '__all__'
