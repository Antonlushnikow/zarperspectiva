from rest_framework import serializers
from mainapp.models import Course, Age, Subject, AcademicHour


class AgeListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.age


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher')
    subject = SubjectSerializer(read_only=True, many=True)
    lesson_duration = serializers.IntegerField(source='lesson_duration.duration')
    lesson_price_once = serializers.IntegerField(source='lesson_duration.price_once')
    lesson_price_month = serializers.IntegerField(source='lesson_duration.price_month')

    class Meta:
        model = Course
        exclude = ('duration',)


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'
