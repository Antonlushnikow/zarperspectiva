from rest_framework import serializers
from mainapp.models import Course, Age


class AgeListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.age


class CourseSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.title')
    teacher_name = serializers.CharField(source='teacher')
    age = AgeListingField(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ('subject_name', 'teacher_name')
