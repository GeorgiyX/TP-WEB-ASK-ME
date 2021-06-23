from django.core.management.base import BaseCommand, CommandError
from app.models import *


def test_tags():
    for tag in Tag.objects.get_top():
        print("{}, questions count: {}".format(tag.name, tag.questions_count))


def test_users_rating():
    for profile in Profile.objects.get_top():
        print("{}, rating: {}".format(profile, profile.rating))


def test_questions():
    questions = list(Question.objects.get_hot_question())
    for question in questions:
        print("question.rating: {}".format(question.rating))
        print("question.dislikes_sum: {}".format(question.dislikes_sum))
        print("question.dislikes.count(): {}".format(question.dislikes.count()))
        print("question.likes_sum: {}".format(question.likes_sum))
        print("question.likes.count(): {}".format(question.likes.count()))
        print("ava url: {}".format(question.author_avatar))
        print("========")


class Command(BaseCommand):
    help = "run useful code"

    def handle(self, *args, **options):
        test_questions()
