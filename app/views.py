import datetime
import random
from math import ceil
from django.http import Http404
from django.shortcuts import render
import app.constants as constants
from app.constants import LOREM_IPSUM, map_id_to_name, TOTAL_ELEMENT, ELEMENT_PER_PAGE, PAGINATION_ELEMENT_COUNT


def get_elem_cnt_cur_pg(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    return range(TOTAL_ELEMENT % ELEMENT_PER_PAGE
                 if page_no * ELEMENT_PER_PAGE > TOTAL_ELEMENT else ELEMENT_PER_PAGE)


def get_questions(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    questions = list()
    random.seed(datetime.datetime.now().second)
    for i in get_elem_cnt_cur_pg(page_no, per_page, total):
        quest = {"text": LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))],
                 "title": LOREM_IPSUM[0:random.randint(15, int(len(LOREM_IPSUM) * 0.02))],
                 "rating": random.randint(0, 100),
                 "answer_cnt": random.randint(0, 100)}
        questions.append(quest)
    return questions


def get_answers(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    answers = list()
    random.seed(datetime.datetime.now().second)
    for i in get_elem_cnt_cur_pg(page_no, per_page, total):
        answer = {"text": LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))],
                  "rating": random.randint(0, 100),
                  "is_checked": ""}
        answers.append(answer)
    answers[random.randint(0, 3)]["is_checked"] = "checked"  # out of range
    return answers


def get_pagination_info(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    min_element_index = (page_no - 1) * per_page + 1
    if min_element_index > total or min_element_index < 0:
        raise Http404("Wrong page index!")
    pagination_info = {}
    if total <= per_page:
        pagination_info["is_enabled"] = False
        return pagination_info
    remaining_pages = ceil((total - min_element_index) / per_page)
    page_count = ceil(total / per_page)

    # Число элементов которые остаются за пределами "индексов" пагинатора
    right_delta = page_count - (page_no + (PAGINATION_ELEMENT_COUNT // 2))
    left_delta = page_no - (PAGINATION_ELEMENT_COUNT // 2) - 1
    # В элементе пагинации могут быть от 2 до PAGINATION_ELEMENT_COUNT кнопок:
    if page_count <= PAGINATION_ELEMENT_COUNT:
        pagination_info["indexes"] = range(1, page_count + 1)
    elif left_delta < 0:
        pagination_info["indexes"] = range(1, page_no + PAGINATION_ELEMENT_COUNT // 2 + abs(left_delta) + 1)
    elif right_delta < 0:
        pagination_info["indexes"] = range(page_no - PAGINATION_ELEMENT_COUNT // 2 - abs(right_delta), page_count + 1)
    else:
        pagination_info["indexes"] = range(page_no - PAGINATION_ELEMENT_COUNT // 2,
                                           page_no + PAGINATION_ELEMENT_COUNT // 2 + 1)

    pagination_info["is_next_disabled"] = (remaining_pages == 0)
    pagination_info["is_prev_disabled"] = (page_no == 1)
    pagination_info["is_enabled"] = True
    pagination_info["current_page_no"] = page_no
    pagination_info["next_page_no"] = page_no + 1
    pagination_info["prev_page_no"] = page_no - 1
    return pagination_info


def index(request, page_no=1):
    context = {"url_to": "/hot", "url_name": "Hot Question",
               "header_text": "New Questions",
               "pagination_info": get_pagination_info(page_no),
               "questions": get_questions(page_no)}
    context["pagination_info"]["url"] = constants.INDEX_URL
    return render(request, "index.html", context)


def hot(request, page_no=1):
    context = {"url_to": "/", "url_name": "New Questions",
               "header_text": "Hot Questions",
               "pagination_info": get_pagination_info(page_no),
               "questions": get_questions(page_no)}
    context["pagination_info"]["url"] = constants.HOT_URL
    return render(request, "index.html", context)


def tag(request, tag_id, page_no=1):
    tag_name = map_id_to_name.get(tag_id, "some name")
    context = {"url_to": "/hot", "url_name": "Hot Questions",
               "header_text": "Tag Questions - {0}".format(tag_name),
               "pagination_info": get_pagination_info(page_no),
               "questions": get_questions(page_no)}
    context["pagination_info"]["url"] = constants.TAG_URL
    context["pagination_info"]["id"] = 1  # Tag параметр URL
    return render(request, "index.html", context)


def question(request, question_id, page_no=1):
    context = {"pagination_info": get_pagination_info(page_no, total=25),
               "question": get_questions(1, 1)[0],
               "answers": get_answers(page_no)}
    context["pagination_info"]["url"] = constants.QUESTION_URL
    context["pagination_info"]["id"] = 1  # Первый параметр URL
    return render(request, "question.html", context)


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def ask(request):
    return render(request, "ask.html", {})


def setting(request):
    return render(request, "setting.html", {})
