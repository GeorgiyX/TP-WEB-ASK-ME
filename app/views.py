import datetime
import random
from math import ceil
from django.http import Http404
from django.shortcuts import render
import app.constants as constants
from django.core.paginator import Paginator, Page
from django.shortcuts import get_object_or_404
from django.urls import reverse
import app.constants
from app.constants import *
from app.models import *


def get_pages_list(page: Page, click_range=2):
    return list(page.paginator.page_range[page.number - click_range - 1: page.number - 1]) + [page.number] \
           + list(page.paginator.page_range[page.number: page.number + click_range])


def get_page(paginator, page_no):
    if page_no > paginator.num_pages:
        page_no = paginator.num_pages
    return paginator.page(page_no)


def get_elem_cnt_cur_pg(page_no, per_page=ELEMENTS_PER_PAGE, total=TOTAL_ELEMENT):
    return range(TOTAL_ELEMENT % ELEMENTS_PER_PAGE
                 if page_no * ELEMENTS_PER_PAGE > TOTAL_ELEMENT else ELEMENTS_PER_PAGE)


def get_questions(page_no, per_page=ELEMENTS_PER_PAGE, total=TOTAL_ELEMENT):
    questions = list()
    random.seed(datetime.datetime.now().second)
    for i in get_elem_cnt_cur_pg(page_no, per_page, total):
        quest = {"text": LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))],
                 "title": LOREM_IPSUM[0:random.randint(15, int(len(LOREM_IPSUM) * 0.02))],
                 "rating": random.randint(0, 100),
                 "answer_cnt": random.randint(0, 100)}
        questions.append(quest)
    return questions


def get_answers(page_no, per_page=ELEMENTS_PER_PAGE, total=TOTAL_ELEMENT):
    answers = list()
    random.seed(datetime.datetime.now().second)
    for i in get_elem_cnt_cur_pg(page_no, per_page, total):
        answer = {"text": LOREM_IPSUM[0:random.randint(50, len(LOREM_IPSUM))],
                  "rating": random.randint(0, 100),
                  "is_checked": ""}
        answers.append(answer)
    answers[random.randint(0, 3)]["is_checked"] = "checked"  # out of range
    return answers


def get_pagination_info(page_no, per_page=ELEMENTS_PER_PAGE, total=TOTAL_ELEMENT):
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


def get_right_col_data():
    return {"top_tags": Tag.objects.get_top(), "tag_url": constants.TAG_URL, "top_users": Profile.objects.get_top()}

def index(request, page_no=1):
    paginator = Paginator(Question.objects.get_new_question(), constants.ELEMENTS_PER_PAGE)
    context = {}
    context["url_to"] = constants.HOT_URL
    context["url_name"] = "Hot Question"
    context["header_text"] = "New Questions"
    context["pagination_info"] = {"url": constants.INDEX_URL}
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
    context["right_col"] = get_right_col_data()
    return render(request, "index.html", context)


def hot(request, page_no=1):
    paginator = Paginator(Question.objects.get_hot_question(), constants.ELEMENTS_PER_PAGE)
    context = {}
    context["url_to"] = constants.INDEX_URL
    context["url_name"] = "New Question"
    context["header_text"] = "Hot Questions"
    context["pagination_info"] = {"url": constants.HOT_URL}
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
    context["right_col"] = get_right_col_data()
    return render(request, "index.html", context)


def tag(request, tag_id, page_no=1):
    tag_object = get_object_or_404(Tag, id=tag_id)
    paginator = Paginator(Question.objects.get_question_by_tag(tag_id), constants.ELEMENTS_PER_PAGE)
    if paginator.count == 0:
        raise Http404("No questions")
    context = {}
    context["url_to"] = constants.HOT_URL
    context["url_name"] = "Hot Question"
    context["header_text"] = "Tag Questions - {}".format(tag_object.name)
    context["pagination_info"] = {"url": constants.TAG_URL, "id": tag_id}
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
    context["right_col"] = get_right_col_data()
    return render(request, "index.html", context)


def question(request, question_id, page_no=1):
    question_object = get_object_or_404(Question, id=question_id)
    paginator = Paginator(Answer.objects.get_answer_by_question_id(question_id), constants.ELEMENTS_PER_PAGE)
    context = {}
    context["pagination_info"] = {"url": constants.QUESTION_URL, "id": question_id}
    context["question"] = question_object
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
    context["right_col"] = get_right_col_data()
    return render(request, "question.html", context)


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def ask(request):
    return render(request, "ask.html", {})


def setting(request):
    return render(request, "setting.html", {})
