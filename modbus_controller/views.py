from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def setup(request):
    template = loader.get_template('modbus_controller/instructions.html')
    return HttpResponse(template.render(context=None, request=request))