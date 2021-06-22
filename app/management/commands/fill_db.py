from django.core.management.base import BaseCommand, CommandError
from ask_me.settings import AVATARS, MEDIA_ROOT
from app.models import Profile, Question, Tag, Answer, User
from app.constants import *
import random
import names
import time


# def get_questions(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
#     questions = list()
#     random.seed(datetime.datetime.now().second)
#     for i in get_elem_cnt_cur_pg(page_no, per_page, total):
#         questions.append(quest)
#     return questions
#
#
# def get_answers(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
#     answers = list()
#     random.seed(datetime.datetime.now().second)
#     for i in get_elem_cnt_cur_pg(page_no, per_page, total):
#         answer = {"text": LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))],
#                   "rating": random.randint(0, 100),
#                   "is_checked": ""}
#         answers.append(answer)
#     answers[random.randint(0, 3)]["is_checked"] = "checked"  # out of range
#     return answers


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
        profile.login = user.email.split("@")[0]
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
        question.title = LOREM_IPSUM[0:random.randint(15, int(len(LOREM_IPSUM) * 0.02))]
        question.text = LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))]
        question.author = User.objects.get(id=random.randint(1, USER_COUNT))
        question.save()

        question.tags.add(*get_range(Tag.objects.all(), TAGS_COUNT, 10))
        question.likes.add(*get_range(User.objects.all(), USER_COUNT, 50))
        question.dislikes.add(*get_range(User.objects.all(), USER_COUNT, 10))
        question.save()


def add_answers():
    for i in range(0, ANSWERS_COUNT):
        answer = Answer()
        answer.text = LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))]
        answer.author = User.objects.get(id=random.randint(1, USER_COUNT))
        answer.question = Question.objects.get(id=random.randint(1, QUESTION_COUNT))
        answer.is_checked = random.choices([True, False], weights=[1, 20])
        answer.save()

        answer.likes.add(*get_range(User.objects.all(), USER_COUNT, 50))
        answer.dislikes.add(*get_range(User.objects.all(), USER_COUNT, 10))
        answer.save()


class Command(BaseCommand):
    help = "Add askme data to current db"

    def handle(self, *args, **options):
        start_time = time.time()
        # try:
        add_users()
        add_tags()
        add_questions()
        add_answers()

    # except:
    #     self.stdout.write(self.style.ERROR("Can't fill database"))
    #     return
        end_time = time.time()
        self.stdout.write(self.style.SUCCESS("Database filled in {.f3} sec".format(end_time - start_time)))