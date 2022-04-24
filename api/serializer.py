from rest_framework import serializers

from NFT_GEN.models import LayersModel,Image,ProjectDesc, ArchivedProject



class LayersModelSerializer(serializers.ModelSerializer):
    class   Meta:
        model = LayersModel
        fields= '__all__'

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields='__all__'

class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model =ProjectDesc
        fields='__all__'

class ArchivedProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedProject
        fields='__all__'

