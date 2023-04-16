from datetime import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from .forms import PageForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def page_list(request):
    pages = Page.objects.all()
    return render(request, 'page_list.html', {'pages': pages})


def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk)
    return render(request, 'page_detail.html', {'page': page, 'date_published': page.date_created})


@login_required
def page_new(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            return redirect('pages:page_detail', pk=page.pk)
    else:
        form = PageForm()
    return render(request, 'page_form.html', {'form': form})



@login_required
def page_edit(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            return redirect('pages:page_detail', pk=page.pk)
    else:
        form = PageForm(instance=page)
    return render(request, 'page_edit.html', {'form': form, 'page': page})


@login_required
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    page.delete()
    return redirect('pages:page_list')


def page_detail_by_id(request, pk):
    page = get_object_or_404(Page, pk=pk)
    return render(request, 'page_detail.html', {'page': page})
