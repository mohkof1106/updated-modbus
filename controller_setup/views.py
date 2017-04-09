import logging
logger = logging.getLogger("live_control")

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.core.urlresolvers import reverse

from controller_setup.models import Document
from controller_setup.forms import DocumentForm
from controller_setup.management.commands.templates import main as generate_templates


# Create your views here.
from .models import Template, LinkUserToPlant
from .tools_ssh import start_plant, restart_plant, stop_plant, status_plant, sync_plant

@login_required(login_url='/login/')
def index(request):
    template = loader.get_template('controller_setup/index.html')
    return HttpResponse(template.render(context=None, request=request))

def done(request, go_back=None, string_list=None):
    template = loader.get_template('controller_setup/done.html')
    context = {
        'go_back': go_back,
        'string_list': string_list,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def control(request):
    links = LinkUserToPlant.objects.all()
    template = loader.get_template('controller_setup/control.html')
    context = {
        'links': links,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def command(request, command, link_pk):
    link = LinkUserToPlant.objects.get(pk=link_pk)
    response = command(link)
    logger.info("for command %s, response %s" % (command, response))
    try:
        response = map(str, response)
    except:
        response = [str(response)]
    return done(request, go_back='control', string_list=response)

def start(request, link_pk):
    return command(request, start_plant, link_pk)
def restart(request, link_pk):
    return command(request, restart_plant, link_pk)
def stop(request, link_pk):
    return command(request, stop_plant, link_pk)
def status(request, link_pk):
    return command(request, status_plant, link_pk)

def sync(request, link_pk):
    return command(request, sync_plant, link_pk)

@login_required(login_url='/login/')
def templates(request):
    templates = Template.objects.all()
    template = loader.get_template('controller_setup/templates.html')
    context = {
        'templates': templates,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('controller_setup.views.upload'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'controller_setup/upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

@login_required(login_url='/login/')
def autotemplates(request):
    return done(request, go_back='templates', string_list=generate_templates())