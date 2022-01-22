from django.db.models.query_utils import select_related_descend
from rest_framework import serializers
from rest_framework.utils import model_meta

from challenge.compile_run_entities import Language
from challenge.models import Candidate,TestCase

class CompileRunRequestSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10,required=True)
    code = serializers.CharField(max_length=100000,required=True)
    stdin = serializers.CharField(max_length=1000000,required=True)
    is_custom_input = serializers.BooleanField()
    guid = serializers.UUIDField()

class TestcaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestCase
        fields  = ['id','question','timeout','hint','score','sample']

