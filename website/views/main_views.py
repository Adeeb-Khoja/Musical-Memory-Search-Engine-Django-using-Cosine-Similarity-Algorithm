from .modules import *
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from website.forms import LoginForm

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'website/index.html', context)


class AuthView(View):
    form_class = LoginForm
    template_name = 'website/login.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, self.template_name, {'form': self.form_class()})
        else:
            return redirect('index_view')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                nextt = request.POST.get('next')
                return redirect(nextt) if nextt else redirect('index_view')
            else:
                context['error'] = 'Não foi possível lhe autenticar. Tem certeza que as informações estão corretas?'
        print(context)
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index_view')



def page_not_found(request):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 404
    return render(request, '404.html')
