from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

class ListView(ListView):
    template_name = "object_list.html"

class DetailView(DetailView):
    template_name = "object_detail.html"

class CreateView(CreateView):
    template_name = "object_create.html"

class UpdateView(UpdateView):
    template_name = "object_update.html"

class DeleteView(DeleteView):
    template_name = "object_delete.html"
