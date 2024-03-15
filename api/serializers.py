import rest_framework
from robotic.models import RoboticUser

class RoboticUserSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = RoboticUser
        fields = (
            'id',
            'username', 
            'full_name', 
            'mini_bio',
            'email', 
            'cpf', 
            'registration', 
            'level_access',  
            'birth_date',
            'sex',           
            'school',           
            'is_activated_by_admin',           
        )
        
        #profile_picture 
