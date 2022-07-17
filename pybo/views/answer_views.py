from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url = 'common:login')
def answer_create(request, question_id) :
    question = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST' :
        form = AnswerForm(request.POST)
        if form.is_valid() :
            answer = form.save(commit = False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            print('resolve', resolve_url('pybo:detail', question.id),'테스트 입니다.', '{}#answer_{}'.format('첫', '둘'))
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id = question.id), answer.id))
    else :
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url = 'common:login')
def answer_modify(request, answer_id) :
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author :
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)
    if request.method == "POST" :
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid() :
            answer = form.save(commit = False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id) #Answer 테이블의 question_id 컬럼 값은 Answer 에 새로 추가할놈과 연동된 question 테이블의 id 값이란 소리
    else :
        form = AnswerForm(instance = answer)
    print("엔서퀘스쳔아이디", answer.question.id, answer.question_id)
    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url = 'common:login')
def answer_delete(request, answer_id) :
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author :
        messages.error(request, '삭제권한이 없?습니다.')
    else :
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)