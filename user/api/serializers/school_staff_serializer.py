from rest_framework import serializers
from schools.models import School
from user.models import SchoolStaffProfile, SchoolStaff, SchoolStaffProfile,User
from rest_framework.validators import UniqueTogetherValidator
import jwt
from rest_framework.exceptions import AuthenticationFailed


class SchoolStaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStaffProfile
        fields = ['school']


class SchoolStaffSerializer(serializers.ModelSerializer):
    tprofile = SchoolStaffProfileSerializer(source='school_staff')
    class Meta:
        model = SchoolStaff
        fields = [
            'username',
            'email',
            'password',
            'phone_number',
            'tprofile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=SchoolStaff.objects.all(),
                fields=['phone_number'],
                message='phone_number must be unique'
            ),
            UniqueTogetherValidator(
                queryset=SchoolStaff.objects.all(),
                fields=['email'],
                message='email must be unique'
            )
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        t = validated_data.pop('school_staff', None)
        school_staff = super().create(validated_data)

        school_staff_profile = SchoolStaffProfile.objects.get(user=school_staff)
        if school_staff_profile:
            school_staff_profile.school = t.get('school')
            school_staff_profile.save()
        else:
            SchoolStaffProfile.objects.create(user=school_staff,school=t.get('school'))

        if password:
            school_staff.set_password(password)
            school_staff.save()
        return school_staff


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        t = validated_data.pop('school_staff', None)

        # instance.username = validated_data.pop('username', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        school_pk = t.get('school')  
        try:
            school_obj = School.objects.get(title=t.get('school'))
        except School.DoesNotExist:
            school_obj = None

        if school_obj is not None:
            school_staff_profile, created = SchoolStaffProfile.objects.get_or_create(user=instance)
            school_staff_profile.school = school_obj
            school_staff_profile.save()

        if password:
            instance.set_password(password)
            instance.save()

        return instance
    

class SchoolStaffRetrieveSerializer(serializers.ModelSerializer):
    tprofile = SchoolStaffProfileSerializer(source='school_staff')
    class Meta:
        model = SchoolStaff
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'national_code',
            'phone_number',
            'tprofile'
        ]
        extra_kwargs = {
            'id':{'read_only':True},
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=SchoolStaff.objects.all(),
                fields=['phone_number'],
                message='phone_number must be unique'
            ),
            UniqueTogetherValidator(
                queryset=SchoolStaff.objects.all(),
                fields=['email'],
                message='email must be unique'
            ),
            UniqueTogetherValidator(
                queryset=SchoolStaff.objects.all(),
                fields=['national_code'],
                message='national_code must be unique'
            )
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        t = validated_data.pop('school_staff', None)
        school_staff = super().create(validated_data)

        school_staff_profile = SchoolStaffProfile.objects.get(user=school_staff)
        if school_staff_profile:
            school_staff_profile.school = t.get('school')
            school_staff_profile.save()
        else:
            SchoolStaffProfile.objects.create(user=school_staff,school=t.get('school'))

        if password:
            school_staff.set_password(password)
            school_staff.save()
        return school_staff


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        t = validated_data.pop('school_staff', None)

        # instance.username = validated_data.pop('username', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        school_pk = t.get('school')  
        try:
            school_obj = School.objects.get(title=t.get('school'))
        except School.DoesNotExist:
            school_obj = None

        if school_obj is not None:
            school_staff_profile, created = SchoolStaffProfile.objects.get_or_create(user=instance)
            school_staff_profile.school = school_obj
            school_staff_profile.save()

        if password:
            instance.set_password(password)
            instance.save()

        return instance
    

class ActiveUserSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    class Meta:
        fields=['token']
