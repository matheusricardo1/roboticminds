import rest_framework
from robotic.models import RoboticUser

class RoboticUserRegisterSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = RoboticUser
        fields = (
            'username', 
            'password',

            #"email",
            #"cpf",
            #"registration",
            #"birth_date",
            #"level_access",
            #"sex",
        )

class RoboticUserSerializer(rest_framework.serializers.ModelSerializer):
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
