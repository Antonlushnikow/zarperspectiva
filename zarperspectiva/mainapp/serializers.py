from rest_framework import serializers
from mainapp.models import Course, Age, Subject


class AgeListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.age


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject')
    teacher_name = serializers.CharField(source='teacher')
    subject = SubjectSerializer(read_only=True, many=True)
    # age = AgeListingField(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ('subject_name', 'teacher_name', 'subject')


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'
