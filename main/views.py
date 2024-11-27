from lib2to3.fixes.fix_input import context
from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache

from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject
from main.services import get_cached_subjects_for_student

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject



class StudentListView(LoginRequiredMixin, ListView):
    model = Student



#def index(request):
#   students_list = Student.objects.all()
#    context = {
#       'object_list':students_list,
#       'title': 'Главная'
#    }
#    return render(request, 'main/material_list.html', context)


@login_required
def contact(request):
    if request.method == 'POST':
       name = request.POST.get('name')
       email = request.POST.get('email')
       message = request.POST.get('message')
       print (f'{name}, ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'main/contact.html', context)


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    #template_name = 'main/student_detail.html'

    permission_required = 'main.view_student'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subjects'] = get_cached_subjects_for_student(self.object.pk)
        return context_data
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    #fields = ('first_name', 'last_name','avatar')
    success_url = reverse_lazy('main:index')
    permission_required = 'main.add_student'

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    #fields = ('first_name', 'last_name','avatar')
    success_url = reverse_lazy('main:index')
    permission_required = 'main.change_student'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data ['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data ['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data ['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data ['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Student
    success_url = reverse_lazy('main:index')

    def test_func(self):
        return self.request.user.is_superuser

def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)
    if student_item.is_active:
        student_item.is_active = False
    else:
        student_item.is_active = True
    student_item.save()

    return redirect(reverse('main:index'))


#def view_student(request, pk):
#    student_item = get_object_or_404(Student, pk=pk)
#    context = {
#        'object': student_item
#    }
#    return render(request, 'main/student_detail.html', context)

