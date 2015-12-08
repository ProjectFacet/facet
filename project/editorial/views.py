from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StoryForm
# Create your views here.

def index(request):
    # return static homepage for now
    return render(request, 'editorial/home.html')

def userprofile(request):
    # return user profile page with profile forms
    return render(request, 'editorial/user_profile_settings.html')

def story_new(request):
    # return edit story page
    form = StoryForm()
    if request.method == "POST":
        form = StoryForm(request.POST or None)
    if form.is_valid():
        story = form.save(commit=False)
        story.owner = request.user
        story.creation_date = timezone.now()
        story.save()
        return redirect('story_detail', pk=post.pk)
    else:
        form = StoryForm()
    return render(request, 'editorial/story.html', {'form': form})

def story_detail(request):
    return HttpResponse("I think it worked.")

def dashboard(request):
    # return dashboard view for logged in user.
    pass
