from django.shortcuts import render,redirect
from quiz.models import Category,Questions,Answers,QuizRecord
from django.contrib.auth.models import User
from quizweb.forms import RegisterationForm,LoginForm
from django.views.generic import CreateView,View,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import random
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if  not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

@signin_required
@never_cache
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")



class SignUpView(CreateView):
    form_class=RegisterationForm
    model=User
    template_name="register.html"
    success_url=reverse_lazy("signup")

    # def form_valid(self,form):
    #     messages.success(self.request,"account has been created")
    #     return super().form_valid(form)
    # def form_invalid(self, form):
    #     messages.error(self.request,"failed to create account")
    #     return super().form_valid(form)


class SignInView(FormView):
    form_class=LoginForm
    template_name='login.html'
    # success_url=reverse_lazy("#")
    def post(self, request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})

@method_decorator(decs,name="dispatch")
class HomeView(TemplateView):
    template_name="home.html"


@method_decorator(decs,name="dispatch")
class QuizHome(View):
    def get(self,request,*args,**kwargs):
        qs=Category.objects.all()
        return render(request,"quiz-home.html",{"cats":qs})
    def post(self,request,*args,**kwargs):
        cat=request.POST.get("category")
        mode=request.POST.get("mode")
        print(cat,mode)
        return redirect("question-list",mode=mode,cat=cat)

@method_decorator(decs,name="dispatch")
class QuestionList(View):

    def get(self,request,*args,**kwargs):
        category=kwargs.get("cat")
        mode=kwargs.get("mode")
        qs=list(Questions.objects.filter(category__name=category,mode=mode))
        

        random.shuffle(qs)
        return render(request,"question-list.html",{"questions":qs})

    def post(self,request,*args,**kwargs):
        category=kwargs.get("cat")
        mode=kwargs.get("mode")
        data=request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        questions_attended=len(data)
        total_marks=0
        wrong_ans_count=0
        result=""
        qob=Questions.objects.filter(category__name=category,mode=mode)
        grand_total=0
        for q in qob:
            grand_total+=q.mark
        pass_mark=grand_total//2

        for q,ans in data.items():
            question=Questions.objects.get(question=q)
            right_ans_object=question.answer
            if (right_ans_object.options==ans):
                total_marks=total_marks+question.mark
            else:
                wrong_ans_count +=1
        right_ans_count=questions_attended-wrong_ans_count

        if total_marks>=pass_mark:
            print(request.user," passed the quiz")
            result="pass"
        else:
            print(request.user," failed the quiz")
            result="failed"
        print(f"hello user{request.user} total no of questions attempted={questions_attended} your total mark={total_marks} worng answers count={wrong_ans_count} ")

        data=QuizRecord.objects.create(marks_obtained=total_marks,right_answer_count=right_ans_count,wrong_answer_count=wrong_ans_count,user=request.user,result=result)
        return render(request,"quiz-mark.html",{"questions_attended":questions_attended,"total_marks":total_marks ,"result":result,"right_answer_count":right_ans_count,"wrong_answer_count":wrong_ans_count})
        
@method_decorator(decs,name="dispatch")
class QuizrecordView(ListView):
    model=QuizRecord
    template_name='quiz-record.html'
    context_object_name='records'

    def get_queryset(self):
        return QuizRecord.objects.filter(user=self.request.user)
        
class IndexView(TemplateView):
    template_name='index.html'
