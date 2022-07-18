from rest_framework import serializers
from mainapp.models import Course, Age, Subject, AcademicHour


class AgeListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.age


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class AcademicHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHour
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher')
    subject = SubjectSerializer(read_only=True, many=True)
    lesson_info = AcademicHourSerializer(source='academic_hour')

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ('teacher_name', 'subject')


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'
