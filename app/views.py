from django.http import Http404, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render
import app.constants as constants
from django.core.paginator import Paginator, Page
from django.shortcuts import get_object_or_404
from django.urls import reverse
from app.constants import *
from app.models import *
from app.forms import *


def get_pages_list(page: Page, click_range=2):
    return list(page.paginator.page_range[page.number - click_range - 1: page.number - 1]) + [page.number] \
           + list(page.paginator.page_range[page.number: page.number + click_range])


def get_page(paginator, page_no):
    if page_no > paginator.num_pages:
        page_no = paginator.num_pages
    return paginator.page(page_no)


def get_redirect_url_from_request(request, redirect_get_key=constants.LOGIN_REDIRECT_KEY):
    redirect_url = request.GET.get(redirect_get_key, "/")
    return redirect_url if url_has_allowed_host_and_scheme(redirect_url, allowed_hosts=[]) \
        else reverse(constants.INDEX_URL)


def index(request, page_no=1):
    paginator = Paginator(Question.objects.get_new_question(), constants.ELEMENTS_PER_PAGE)
    context = {}
    context["url_to"] = constants.HOT_URL
    context["url_name"] = "Hot Question"
    context["header_text"] = "New Questions"
    context["pagination_info"] = {"url": constants.INDEX_URL}
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
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
    return render(request, "index.html", context)


def question(request, question_id, page_no=1):
    question_object = get_object_or_404(Question, id=question_id)
    paginator = Paginator(Answer.objects.get_answer_by_question_id(question_id), constants.ELEMENTS_PER_PAGE)
    context = {}
    context["pagination_info"] = {"url": constants.QUESTION_URL, "id": question_id}
    context["question"] = question_object
    context["page"] = get_page(paginator, page_no)
    context["pages_list"] = get_pages_list(context["page"])
    if request.user.is_authenticated:
        if request.method == "POST":
            context["form"] = AddAnswerForm(request.POST)
            if context["form"].is_valid():
                context["form"].save(request.user, question_id)
                return HttpResponseRedirect(reverse(constants.QUESTION_URL, args=[question_id, page_no]))
        else:
            context["form"] = AddAnswerForm()
    return render(request, "question.html", context)


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(constants.INDEX_URL))
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(get_redirect_url_from_request(request))
            else:
                form.add_error(None, "Wrong login or password!")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(get_redirect_url_from_request(request))


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(constants.INDEX_URL)
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            auth.login(request, form.save())
            return HttpResponseRedirect(reverse(constants.INDEX_URL))
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required(redirect_field_name=constants.LOGIN_REDIRECT_KEY)
def ask(request):
    return render(request, "ask.html")


@login_required(redirect_field_name=constants.LOGIN_REDIRECT_KEY)
def setting(request):
    return render(request, "setting.html")

@login_required(redirect_field_name=constants.LOGIN_REDIRECT_KEY)
def add_answer(request, question_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse(constants.INDEX_URL))
    form = AddAnswerForm(request)
    if form.is_valid():
        form.save
    re
