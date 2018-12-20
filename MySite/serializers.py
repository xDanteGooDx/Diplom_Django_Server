from rest_framework import serializers
from .models import *


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'id_question', 'is_right')


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title_book', 'author', 'icon_book')


class TextSerializers(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'text_html', 'id_book')
