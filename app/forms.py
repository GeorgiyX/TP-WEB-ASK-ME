from django import forms
from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class SignUpForm(forms.Form):
    username = forms.CharField(label="Login", max_length=60)
    email = forms.EmailField(label="Email address", max_length=50)
    nickname = forms.CharField(label="Nickname", max_length=50, required=False)
    password_1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Re-enter password")
    avatar = forms.ImageField(label="Upload your avatar", required=False)

    def save(self):
        if not self.is_valid():
            raise Exception("SignUpForm not valid")
        user = User.objects.create_user(username=self.cleaned_data["username"],
                                        password=self.cleaned_data["password_1"],
                                        email=self.cleaned_data["email"])
        user.save()
        profile = Profile()
        profile.user = user
        profile.nickname = self.cleaned_data["nickname"]
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            profile.avatar = avatar
        profile.save()
        return user

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_2 != password_1:
            self.add_error("password_2", "doesn't match")
            raise forms.ValidationError("Passwords don't match each other!")
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).count() != 0:
            self.add_error("username", "A profile with this name already exists!")


class AddAnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"row": "5", "placeholder": "Write your answer here..."}),
                           error_messages={"required": "Please specify your answer."}, label="")

    def save(self, user, question_id):
        if not self.is_valid():
            raise Exception("AddAnswerForm not valid")
        if Question.objects.filter(id=question_id).count() != 1:
            return
        answer = Answer()
        answer.author = user
        answer.question_id = question_id
        answer.text = self.cleaned_data["text"]
        answer.save()


class AddQuestionForm(forms.Form):
    title = forms.CharField(lable="Title")
    text = forms.CharField(widget=forms.Textarea(attrs={"row": "5"}),
                           error_messages={"required": "Please specify your question."}, label="Text")
    tags = forms.CharField(label="Tags", widget=forms.TextInput(
        attrs={"placeholder": "Select the appropriate tags for your question"}))
    pass
