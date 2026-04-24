from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, SignUpForm
from .models import Entry


def entry_list(request):
    entries = Entry.objects.order_by("-created_at")
    return render(request, "diary/entry_list.html", {"entries": entries})


def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, "diary/entry_detail.html", {"entry": entry})


def signup(request):
    if request.user.is_authenticated:
        return redirect("diary:entry_list")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "アカウントを作成しました。")
            return redirect("diary:entry_list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def entry_create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("diary:entry_detail", pk=entry.pk)
    else:
        form = EntryForm()

    return render(request, "diary/entry_form.html", {"form": form})

@login_required
def entry_update(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if request.user != entry.user:
        messages.error(request, "自分が作成した日記だけ編集できます。")
        return redirect("diary:entry_list")

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return redirect("diary:entry_detail", pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
    
    return render(request, "diary/entry_form.html", {"form": form})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if request.user != entry.user:
        messages.error(request, "自分が作成した日記だけ削除できます。")
        return redirect("diary:entry_list")

    if request.method == "POST":
        entry.delete()
        messages.success(request, "日記を削除しました。")
        return redirect("diary:entry_list")
    
    return render(request, "diary/entry_confirm_delete.html", {"entry": entry})
