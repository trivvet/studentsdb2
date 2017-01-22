from datetime import datetime

from django import forms
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DeleteView, CreateView, UpdateView
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Submit, Button

from ..models.students import Student
from ..models.groups import Group
from ..models.exams import Exam
from ..models.results import Result

from ..util import paginate, get_current_group

def results_list(request):
    current_group = get_current_group(request)
    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
    else:
        exams = Exam.objects.all()
    
    # exams ordering
    order_by = request.GET.get('order_by')
    reverse = request.GET.get('reverse')
    if order_by in ('id', 'name', 'date', 'teacher_name', 'exam_group__title'):
        exams = exams.order_by(order_by)
        if reverse == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('date').reverse()

    future_exams = []
    for exam in exams:
        if exam.date > datetime.now(timezone.utc):
            future_exams.append(exam)

    exams_result = []
    for exam in exams:
        if exam.is_completed == True:
            exams_result.append(exam) 

    # groups paginator
    context = paginate(exams_result, 3, request, {}, var_name='results')

    return render(request, 'students/results.html', {'context': context})
        
def results_add(request):
    if request.method == 'POST':
        data = request.POST
        if data.get('cancel_button'):
            messages.warning(request, _(u"Entry results of exam canceled"))
            return HttpResponseRedirect(reverse('results'))
        elif data.get('save_button'):
            i = 0
            errors = []
            all_score = []
            results = []
            result_exam = Exam.objects.get(pk=data['exam_id'])
            for student in Student.objects.filter(student_group=result_exam.exam_group):
                if data['student_mark%s' % student.id]:
                    score = data['student_mark%s' % student.id]
                    try:
                        score = int(score)
                    except ValueError:
                        errors.append({'student_id': student.id, 'text': _(u"Please enter the number from 0 to 12")})
                    else:
                        if score > 0 and score < 12:
                            all_score.append({'student_id': student.id, 'score': score})
                            results.append(Result(result_student=student, result_exam=result_exam, score=score))
                            result_exam.is_completed = True
                        else:
                            errors.append({'student_id': student.id, 'text': _(u"Please enter mark from 0 to 12")})
                else:
                    errors.append({'student_id': student.id, 'text': _(u"Please enter student's mark")})
                i += 1
        
            if not errors:
                for result in results:
                    result.save()
                result_exam.save()
                messages.success(request, _(u"Information about results of exam %s added successfully") % result_exam.name)
                return HttpResponseRedirect(reverse('results'))
            else:
                students = Student.objects.all().filter(student_group=result_exam.exam_group)
                return render(request, 'students/results_add_marks.html', { 'students': students, 'exam': result_exam, 'errors': errors, 'scores': all_score})
    else:
        errors = {}
        if request.GET.get('cancel_button'):
            messages.warning(request, _(u"Adding results of exam canceled"))
            return HttpResponseRedirect(reverse('results'))
        elif request.GET.get('save_button'):
            if request.GET.get('name') is not None:
                if request.GET.get('name'):
                    if Exam.objects.filter(pk=request.GET.get('name')):
                        exam = Exam.objects.get(pk=request.GET.get('name'))
                        students = Student.objects.all().filter(student_group=exam.exam_group)
                        return render(request, 'students/results_add_marks.html', { 'students': students, 'exam': exam })
                    else:
                      errors['name'] = _(u"Plese select completion exam")
                else:
                    errors['name'] = _(u"Please select exam")
        
        exams = Exam.objects.all().filter(is_completed=False)
        return render(request, 'students/results_add.html', { 'exams': exams, 'errors': errors })
  
def results_edit(request, rid=None):
    if request.method == "POST":
        data = request.POST
        if data.get('cancel_button'):
            messages.warning(request, _(u"Editing results of exam canceled"))
            return HttpResponseRedirect(reverse('results'))
        elif data.get('save_button'):
            i = 0
            errors = []
            all_score = []
            results = []
            result_exam = Exam.objects.get(pk=data['exam_id'])
            for student in Student.objects.filter(student_group=result_exam.exam_group):
                if data['student_mark%s' % student.id]:
                    score = data['student_mark%s' % student.id]
                    try:
                        score = int(score)
                    except ValueError:
                        errors.append({'student_id': student.id, 'text': _(u"Please enter the number from 0 to 12")})
                    else:
                        if score > 0 and score < 12:
                            all_score.append({'student_id': student.id, 'score': score})
                            result = Result.objects.get(result_exam=data['exam_id'], result_student=student)
                            result.score = score
                            results.append(result)
                        else:
                            errors.append({'student_id': student.id, 'text': _(u"Please enter mark from 0 to 12")})
                else:
                    errors.append({'student_id': student.id, 'text': _(u"Please enter student's mark")})
                i += 1
        
            if not errors:
                for result in results:
                    result.save()
                messages.success(request, _(u"Information about results of exam %s edited successfully") % result_exam.name)
                return HttpResponseRedirect(reverse('results'))
    else:
        results = Result.objects.filter(result_exam=rid)
        result_exam = Exam.objects.get(pk=rid)
        all_score = []
        for result in results:
            score = result.score
            all_score.append({'student_id': result.result_student.id, 'score': score})
    students = Student.objects.all().filter(student_group=result_exam.exam_group)
    return render(request, 'students/results_edit_marks.html', {'students': students, 'exam': result_exam, 'scores': all_score})

# Delete Page
  
def results_delete(request, rid):
    if request.method == "POST":
        if request.POST.get('cancel_button'):
            messages.warning(request, _(u"Deleting results of exam canceled"))
            return HttpResponseRedirect(reverse('results'))
        else:
            exam = Exam.objects.get(pk=int(rid))
            exam.is_completed = False
            results = Result.objects.filter(result_exam=exam)
            results.delete()
            exam.save()
            messages.success(request, _(u"Information about results of exam %s deleted successfully") % exam.name)
            return HttpResponseRedirect(reverse('results'))
    else:
        try:
            exam = Exam.objects.get(pk=int(rid))
        except:
            messages.error(_(u'There was an error on the server. Please try again later'))
            return HttpResponseRedirect(reverse('results'))
        else:
            return render(request, 'students/results_confirm_delete.html', {'exam': exam})

def exam_results(request, rid):
    context = {}
    results = Result.objects.filter(result_exam=int(rid))
    context['results'] = results
    context['exam'] = Exam.objects.get(pk=int(rid))
    return render(request, 'students/results_list.html', {'context': context})
