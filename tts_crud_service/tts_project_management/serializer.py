from rest_framework import serializers

from tts_project_management.models import AudioData, TtsProject


class AudioDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioData
        fields = "__all__"


class TtsProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TtsProject
        fields = "__all__"


class TtsProjectSerializerData(serializers.ModelSerializer):
    audio_data_set = AudioDataSerializer(many=True, read_only=True)
    audio_data_count = serializers.IntegerField(source="audio_data_set.count", read_only=True)

    class Meta:
        model = TtsProject
        fields = "__all__"


class TtsProjectCreateSchema(serializers.Serializer):
    project_title = serializers.CharField()
    sentenses = serializers.CharField()


class AudioDataInsertReqSchema(serializers.Serializer):
    project_title = serializers.CharField()
    sentenses = serializers.CharField()
    sequence = serializers.IntegerField()
