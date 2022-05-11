from django.shortcuts import render, redirect  # redirectを追加

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

class IndexView(TemplateView):
    template_name = 'snsDjango/index.html'
