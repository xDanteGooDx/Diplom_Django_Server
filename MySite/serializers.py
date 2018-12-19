from  rest_framework import serializers
from .models import *

class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'id_question', 'is_right')
