from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    if request.method == 'POST':

        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(
            user=request.user,
            title=title,
            content=content
        )

        return redirect('home')

    search = request.GET.get('search')

    if search:

        notes = Note.objects.filter(
            user=request.user,
            title__icontains=search
        )

    else:

        notes = Note.objects.filter(user=request.user)

    return render(
        request,
        'home.html',
        {'notes': notes}
    )


@login_required
def delete_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    note.delete()

    return redirect('home')


@login_required
def edit_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        note.title = request.POST['title']

        note.content = request.POST['content']

        note.save()

        return redirect('home')

    return render(
        request,
        'edit.html',
        {'note': note}
    )