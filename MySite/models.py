from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Answer(models.Model):
    answer_text = models.TextField()
    id_question = models.ForeignKey('Question', models.CASCADE)
    is_right = models.BooleanField()

    class Meta:
        db_table = 'Answer'


class Book(models.Model):
    title_book = models.TextField()
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Book'
        permissions = (
            ('read_Book', 'Can read book'),
            ('write_Book', 'Can write book'),
        )


class Chapter(models.Model):
    chapter_title = models.TextField()
    id_book = models.ForeignKey(Book, models.CASCADE)

    class Meta:
        db_table = 'Chapter'


class Educator(models.Model):
    scientific_degree = models.TextField(blank=True, null=True)
    subject_area = models.TextField(blank=True, null=True)
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Educator'


class File(models.Model):
    path_file = models.CharField(max_length=255)
    id_text = models.ForeignKey('Text', models.CASCADE)
    format = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        db_table = 'File'


class Profile(models.Model):
    patronymic = models.TextField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Question(models.Model):
    question_text = models.TextField()
    id_test = models.ForeignKey('Test', models.CASCADE)
    get_score = models.IntegerField()

    class Meta:
        db_table = 'Question'


class StudGroup(models.Model):
    title = models.CharField(db_column='Title', max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'StudGroup'
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'

    def __str__(self):
        return self.title


class Student(models.Model):
    group = models.ForeignKey(StudGroup, models.SET_NULL, blank=True, null=True)
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Student'


class Test(models.Model):
    test_title = models.TextField()
    author = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    about = models.TextField()

    class Meta:
        db_table = 'Test'
        permissions = (
            ('read_Test', 'Can read test'),
            ('write_Test', 'Can write test'),
        )


class TestResult(models.Model):
    id_test = models.OneToOneField(Test, models.CASCADE, null=True)
    id_student = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField()
    score = models.IntegerField()

    class Meta:
        unique_together = (('id_test', 'id_student', 'attempts'),)
        db_table = 'TestResult'


class Text(models.Model):
    text_source = models.TextField()
    id_chapter = models.ForeignKey(Chapter, models.CASCADE)

    class Meta:
        db_table = 'Text'
