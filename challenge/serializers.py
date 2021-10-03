from django.db.models.query_utils import select_related_descend
from rest_framework import serializers

from challenge.compile_run_entities import Language
from challenge.models import Candidate

class CompileRunRequestSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10,required=True)
    code = serializers.CharField(max_length=100000,required=True)
    stdin = serializers.CharField(max_length=1000000,required=True)
    is_custom_input = serializers.BooleanField()
    guid = serializers.UUIDField()
