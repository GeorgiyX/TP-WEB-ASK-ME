from math import ceil
from django.http import Http404
from django.shortcuts import render

map_id_to_name = {1: "C++", 2: "libs", 3: "linux", 4: "mapnik"}
PAGINATION_ELEMENT_COUNT = 5
ELEMENT_PER_PAGE = 15
TOTAL_ELEMENT = 15


def get_elem_cnt_cur_pg(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    return range(TOTAL_ELEMENT % ELEMENT_PER_PAGE
                 if page_no * ELEMENT_PER_PAGE > TOTAL_ELEMENT else ELEMENT_PER_PAGE)


def get_pagination_info(page_no, per_page=ELEMENT_PER_PAGE, total=TOTAL_ELEMENT):
    max_index = page_no * per_page
    if max_index > total or max_index < 0:
        raise Http404("Wrong page index!")
    pagination_info = {}
    if total <= per_page:
        pagination_info["is_enabled"] = False
        return pagination_info
    remaining_pages = ceil((total - max_index) / per_page)
    page_count = ceil(total / per_page)

    # В элементе пагинации могут быть от 2 до PAGINATION_ELEMENT_COUNT кнопок:
    if page_count <= PAGINATION_ELEMENT_COUNT:
        pagination_info["indexes"] = list(range(1, page_count))
    elif (PAGINATION_ELEMENT_COUNT // 2 + page_no) > page_count:
        pagination_info["indexes"] = list(range(page_count - PAGINATION_ELEMENT_COUNT, page_count))
    pagination_info["is_next_disabled"] = True if remaining_pages == 0 else False
    pagination_info["is_prev_disabled"] = True if page_no == 1 else False
    pagination_info["is_enabled"] = True
    pagination_info["current_page_no"] = page_no
    # Значения не используются, если кнопка не валидна
    pagination_info["next_page_no"] = page_no + 1
    pagination_info["prev_page_no"] = page_no - 1
    return pagination_info


def index(request, page_no=1):
    context = {"url_to": "/hot", "url_name": "Hot Question",
               "header_text": "New Questions",
               "pagination_info": get_pagination_info(page_no),
               "question_cnt": get_elem_cnt_cur_pg(page_no)}
    context["pagination_info"]["base_url"] = "/"
    return render(request, "index.html", context)


def hot(request, page_no=1):
    context = {"url_to": "/", "url_name": "New Questions",
               "header_text": "Hot Questions",
               "pagination_info": get_pagination_info(page_no),
               "question_cnt": get_elem_cnt_cur_pg(page_no)}
    context["pagination_info"]["base_url"] = "hot/"
    print(context["pagination_info"])
    return render(request, "index.html", context)


def tag(request, tag_id, page_no=1):
    tag_name = map_id_to_name.get(tag_id, "some name")
    context = {"url_to": "/hot", "url_name": "Hot Questions",
               "header_text": "Tag Questions - {0}".format(tag_name),
               "pagination_info": get_pagination_info(page_no),
               "question_cnt": get_elem_cnt_cur_pg(page_no)}
    context["pagination_info"]["base_url"] = "tag/{0}/".format(tag_id)
    return render(request, "index.html", context)


def question(request, question_id, page_no=1):
    context = {"pagination_info": get_pagination_info(page_no, total=25),
               "answer_cnt": get_elem_cnt_cur_pg(page_no, total=25)}
    context["pagination_info"]["base_url"] = "question/{0}/".format(question_id)
    return render(request, "question.html", context)


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def ask(request):
    return render(request, "ask.html", {})


def setting(request):
    return render(request, "setting.html", {})
