from rest_framework import serializers

from . import models


class PhonebookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PhoneBook
        fields = (
            'pk',
            'creator',
            'first_name',
            'last_name',
            'phone_number',
        )
        read_only_fields = (
            'pk',
        )