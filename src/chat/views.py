from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic import DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from .forms import ComposeForm
from .models import Thread, ChatMessage

class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return render(request, self.template_name, {'qs': self.get_queryset})

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'
    # def get_success_url(self):
    #     return redirect(success_url+self.kwargs.get("username"))

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user,other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        print("Posted")

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        other_username  = User.objects.filter(username=self.kwargs.get("username"))[0]
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user_from=user,user_to=other_username, thread=thread, message=message)
        return super().form_valid(form)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
