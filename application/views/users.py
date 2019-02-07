

class UserCreate(LoginRequiredMixin, CreateView):
    form_class = UserForm
    model = BasicUser
    template_name = 'signup.html'
    login_url = '/admin/'

signup = UserCreate.as_view()