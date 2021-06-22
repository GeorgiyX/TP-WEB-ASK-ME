from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from ask_me.settings import AVATARS, MEDIA_ROOT

# Create your models here.
def row_preview(number, text, length=30):
    return "[{}]: {}".format(number,  ("%s..." % str(text)[0:length]) if len(text) > length else str(text)[0:len(text)])


class Profile(models.Model):
    login = models.CharField(max_length=40)
    avatar = models.ImageField(upload_to=AVATARS, null=True, default=str(MEDIA_ROOT / AVATARS / "no-ava.png"),
                               storage=FileSystemStorage(location=MEDIA_ROOT), max_length=300)  # Доступ через .url
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return row_preview(self.id, "{} - {}".format(self.user.username, self.login))


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return row_preview(self.id, self.name)


class Question(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="questions")
    tags = models.ManyToManyField(Tag, related_name="questions")
    likes = models.ManyToManyField(User, related_name="question_likes")
    dislikes = models.ManyToManyField(User, related_name="question_dislikes")

    def __str__(self):
        return row_preview(self.id, self.title)


class Answer(models.Model):
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    likes = models.ManyToManyField(User, related_name="answers_likes")
    dislikes = models.ManyToManyField(User, related_name="answers_dislikes")
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return row_preview(self.id, self.text)
