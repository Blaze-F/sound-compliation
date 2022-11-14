from rest_framework import serializers

from tts_project_management.models import AudioData, TtsProjects


class TtsProjectSerializer(serializers.Serializer):
    class Meta:
        model = TtsProjects
        fields = "__all__"


class AudioDataSerializer(serializers.Serializer):
    class Meta:
        model = AudioData
        fields = "__all__"
