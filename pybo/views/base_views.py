from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.db.models import Q, Count

def index(request) :
    """
    pybo 모델 출력
    """
    #입력 인자
    3/0
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    #정렬
    if so == 'recommend' :
        question_list = Question.objects.annotate(num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular' :
        question_list = Question.objects.annotate(num_answer = Count('answer')).order_by('-num_answer', '-create_date')
    else :
        question_list = Question.objects.order_by('-create_date')
    #조회
    if kw :
        question_list = question_list.filter(
            Q(subject__icontains = kw) |
            Q(content__icontains = kw) |
            Q(author__username__icontains = kw) |
            Q(answer__author__username__icontains = kw)
        ).distinct()
    #페이지 처리
    paginator = Paginator(question_list, 10)#1페이지에 10개씩
    page_obj = paginator.get_page(page)
    context = {'question_list' : page_obj, 'page' : page, 'kw' : kw, 'so' : so}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def test(request, exception) :
    img = open("C:\projects\mysite\templates\mss.jpg", mode = "r")
    return img