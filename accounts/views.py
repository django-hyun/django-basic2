from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from django.contrib.auth import login as auth_login



@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.add(follow_user)
    follow_user.follower_set.add(request.user)
    messages.success(request, f"{follow_user}님을 팔로우했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.remove(unfollow_user)
    unfollow_user.follower_set.remove(request.user)
    messages.success(request, f"{unfollow_user}님을 언팔했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)



from django.contrib.auth.views import (
    logout_then_login,  
    # AuthPasswordChangeView
    PasswordChangeView as AuthPasswordChangeView,
)
# PasswordChangeForm
from .forms import SignupForm, ProfileForm, PasswordChangeForm
# reverse_lazy
from django.urls import reverse_lazy


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy("accounts:password_change")
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다.")
            return redirect("accounts:profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        "form": form,
    })

def logout(request):
    messages.success(request, '로그아웃되었습니다.')
    return logout_then_login(request)



class ProfileView(LoginRequiredMixin, TemplateView):
   template_name="accounts/profile.html"
   
profile = ProfileView.as_view()



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # form.save()
            signed_user = form.save ()
            auth_login(request, signed_user)

            messages.success(request, "회원가입 환영합니다.")
            return redirect("/")
    else:
        form = SignupForm()
       
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })