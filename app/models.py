from django.db import models
from django.contrib.auth.models import User
from ask_me.settings import AVATARS, MEDIA_ROOT
from cachetools import cached, TTLCache
import app.constants as constants
import os


# Create your models here.
def row_preview(number, text, length=30):
    return "[{}]: {}".format(number, ("%s..." % str(text)[0:length]) if len(text) > length else str(text)[0:len(text)])


class ProfileManager(models.Manager):
    @cached(cache=TTLCache(maxsize=10, ttl=constants.CACHE_TTL))
    def get_top(self, fetch_count=10):
        """Возвращае пользователей с самыми большими рейтингами"""
        return self.annotate(questions_rating=models.Count("user__questions__likes", distinct=True),
                             answers_rating=models.Count("user__answers__likes", distinct=True),
                             rating=models.F("questions_rating") + models.F("answers_rating")) \
                   .order_by("-rating")[0:fetch_count]


class Profile(models.Model):
    nickname = models.CharField(max_length=40, null=True)
    avatar = models.ImageField(upload_to=AVATARS, default=os.path.join(AVATARS, "no-ava.png"), max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    objects = ProfileManager()

    def __str__(self):
        return row_preview(self.id, "{} - {}".format(self.user.username, self.nickname))


class TagManager(models.Manager):
    @cached(cache=TTLCache(maxsize=10, ttl=constants.CACHE_TTL))
    def get_top(self, fetch_count=25):
        """Возвращает список наиболее частых тегов"""
        return self.annotate(questions_count=models.Count("questions")).order_by("-questions_count")[0:fetch_count]


class Tag(models.Model):
    name = models.CharField(max_length=30)
    objects = TagManager()

    def __str__(self):
        return row_preview(self.id, self.name)


class QuestionManager(models.Manager):
    def get_questions_with_rating(self):
        return self.annotate(likes_sum=models.Count("likes", distinct=True),
                             dislikes_sum=models.Count("dislikes", distinct=True),
                             rating=models.F("likes_sum") - models.F("dislikes_sum"),
                             answers_count=models.Count("answers", distinct=True))

    def get_new_question(self):
        return self.get_questions_with_rating().order_by("-id")

    def get_question_by_tag(self, tag_id):
        return self.get_questions_with_rating().filter(tags__id=tag_id).order_by("-id")

    def get_hot_question(self):
        return self.get_questions_with_rating().order_by("-rating")

    def get_answers(self):
        return self.answers.all()


class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="questions")
    tags = models.ManyToManyField(Tag, related_name="questions")
    likes = models.ManyToManyField(User, related_name="question_likes")
    dislikes = models.ManyToManyField(User, related_name="question_dislikes")
    objects = QuestionManager()

    def __str__(self):
        return row_preview(self.id, self.title)


class AnswerManager(models.Manager):
    def get_answer_by_question_id(self, question_id):
        return self.filter(question_id=question_id) \
            .annotate(likes_sum=models.Count("likes", distinct=True),
                      dislikes_sum=models.Count("dislikes", distinct=True),
                      rating=models.F("likes_sum") - models.F("dislikes_sum")).order_by("-rating")


class Answer(models.Model):
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    likes = models.ManyToManyField(User, related_name="answers_likes")
    dislikes = models.ManyToManyField(User, related_name="answers_dislikes")
    is_checked = models.BooleanField(default=False)
    objects = AnswerManager()

    def __str__(self):
        return row_preview(self.id, self.text)
