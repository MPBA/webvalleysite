from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from forms import EditProfileForm

from website.models import UserProfile

@login_required
def my(request):
    return render(request, 'profile/my.html', {
        'page_title' : 'profile/view',
        'sidebar_item' : 'view-profile',
    })


@login_required
def edit(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/my/')
        else:
            form = EditProfileForm(request.POST, request.FILES, instance=profile)
            return render(request, 'profile/edit.html', {'form': form})

    else:
        form = EditProfileForm(instance=profile)
        return render(request, 'profile/edit.html',
                {'form': form,
                 'page_title': 'profile/edit',
                 'sidebar_item':'view-profile'})
