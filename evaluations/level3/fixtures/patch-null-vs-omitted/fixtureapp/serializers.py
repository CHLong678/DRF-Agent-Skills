from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "note")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.note = validated_data.get("note")
        instance.save()
        return instance
