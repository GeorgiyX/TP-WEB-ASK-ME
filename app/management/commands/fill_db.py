from django.core.management.base import BaseCommand, CommandError
from ask_me.settings import AVATARS, MEDIA_ROOT
from app.models import Profile, Question, Tag, Answer, User
from app.constants import *
import random
import names
import time


def add_users():
    profiles = []
    random_indexes = list(range(0, USER_COUNT))
    random.shuffle(random_indexes)
    for index in random_indexes:
        user = User()
        user.email = "my.mail.{}@google.com".format(index)
        user.username = "{}_{}".format(names.get_last_name(), index)
        user.password = "password"
        user.save()

        profile = Profile()
        profile.nickname = user.email.split("@")[0]
        profile.user = user
        profiles.append(profile)

    Profile.objects.bulk_create(profiles)


def get_range(query_set, object_count, count_to_fetch):
    offset = random.randint(1, object_count - 1)
    limit = offset + random.randint(1, count_to_fetch)
    limit = limit if limit < object_count else object_count
    return list(query_set[offset: limit])


def add_tags():
    tag_names = ["Python", "Java", "Ruby/Ruby on Rails", "HTML", "JavaScript", "C", "Language",
                 "C++", "C#", "Objective-C", "PHP", "SQL", "Swift", "Web", "SQL", "Design"]
    tags = []
    for i in range(0, TAGS_COUNT):
        tag = Tag()
        tag.name = "{}:{}".format(random.choices(tag_names)[0], random.randint(0, 100))
        tags.append(tag)

    Tag.objects.bulk_create(tags)


def add_questions():
    for i in range(0, QUESTION_COUNT):
        question = Question()
        question.title = random.choices(["How", "What", "Why"])[0] + " " \
                         + LOREM_IPSUM[0:random.randint(15, int(len(LOREM_IPSUM) * 0.02))].lower() + "?"
        question.text = LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))] + "?"
        question.author = User.objects.get(id=random.randint(1, USER_COUNT))
        question.save()

        question.tags.add(*get_range(Tag.objects.all(), TAGS_COUNT, 5))
        question.likes.add(*get_range(User.objects.all(), USER_COUNT, 50))
        question.dislikes.add(*get_range(User.objects.all(), USER_COUNT, 10))
        question.save()


def add_answers():
    for i in range(0, ANSWERS_COUNT):
        answer = Answer()
        answer.text = random.choices(["Hi!", "This is a common problem", "I think this solution will help:",
                                      "Hello.", ""])[0]+ " " + LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))]
        answer.author = User.objects.get(id=random.randint(1, USER_COUNT))
        answer.question = Question.objects.get(id=random.randint(1, QUESTION_COUNT))
        answer.is_checked = random.choices([True, False], weights=[1, 20])[0]
        answer.save()

        answer.likes.add(*get_range(User.objects.all(), USER_COUNT, 50))
        answer.dislikes.add(*get_range(User.objects.all(), USER_COUNT, 10))
        answer.save()


class Command(BaseCommand):
    help = "Add askme data to current db"

    def handle(self, *args, **options):
        start_time = time.time()
        add_users()
        add_tags()
        add_questions()
        add_answers()
        end_time = time.time()
        self.stdout.write(self.style.SUCCESS("Database filled in {} sec".format(end_time - start_time)))
