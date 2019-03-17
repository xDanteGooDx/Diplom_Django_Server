from django.contrib.auth.models import User
from rest_framework import serializers

from MySite.models import Answer, Book, Text, Test, FullText, Header


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'id_question', 'is_right')


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title_book', 'author', 'icon_book')


class FullTextSerializers(serializers.ModelSerializer):
    class Meta:
        model = FullText
        fields = ('id', 'text_html', 'id_book')


class TextSerializers(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'text_html', 'id_book')


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',)


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'test_title', 'author', 'about')


class HeaderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ('id', 'id_book', 'text_header')


class TextSerializers(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'text_html', 'id_header')
