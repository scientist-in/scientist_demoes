from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from objectrecognition.models import Document
from objectrecognition.models import Contact
from objectrecognition.forms import DocumentForm
from objectrecognition.forms import ContactForm
from subprocess import call
import json

import os.path
import ipdb

#for runtime improvement
import os
from time import sleep
def list(request, fromPostFlag=0):
    # Handle file upload
    
    fromPostFlag = int(fromPostFlag)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            #call caffe and prediction
            #call(["python","/home/keeda/caffe/examples/00-classification.py"])
            
            #screen send command
            os.system("screen -S caffe -p 0 -X stuff \"run\\n\"")
            
            # Redirect to the document list after POST
            #ipdb.set_trace()
            url = reverse('objectrecognition.views.list',  kwargs = {'fromPostFlag':1})
            return HttpResponseRedirect(url)
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #ipdb.set_trace()
    documents = Document.objects.latest('id')
    if (fromPostFlag==1):
        while not os.path.isfile('result.json'):
            pass
        sleep(.2)
        with open('result.json', 'r') as infile:
            result = json.load(infile)
            #ipdb.set_trace() 
            if len(result)>1:
                mainResult = result[0]
                otherResults = result[1:5]
            else:
                mainResult =""
                otherResults =[""]            
        os.remove(os.path.join('result.json'))    
    else:
        result =[""]
        mainResult =""
        otherResults =[""]
    # Render list page with the documents and the form
    return render_to_response(
        'objectrecognition/index.html',
        {'documents': documents, 'form': form,'mainResult':mainResult,'otherResults':otherResults},
        context_instance=RequestContext(request)
    )
def contact(request):
    if request.method == 'POST':
        print 'reached here'
        #ipdb.set_trace()
        form = ContactForm()
        contact = Contact()
        contact.firstname,contact.surname,contact.phone, contact.email, contact.message = request.POST['firstname'],request.POST['surname'],request.POST['phone'], request.POST['email'], request.POST['message']
        contact.save()
        #ipdb.set_trace()
        return render_to_response('objectrecognition/contact-thanks.html',{},context_instance=RequestContext(request))
    else:
        form = ContactForm()
        return render_to_response(
            'objectrecognition/contact.html',
            {'form': form},
            context_instance=RequestContext(request))
            
def handler404(request):
    print 'came here'
    response = render_to_response('objectrecognition/error_redirect.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

# def index(request):
#     context = {"whatisay":["i","have","nothing"]}
    # return render(request,'objectrecognition/index.html',context)
# def upload_pic(request):
#         form = ImageUploadForm(request.POST, request.FILES)
#         m = ExampleModel.objects.get(pk=course_id)
#         m.model_pic = form.cleaned_data['image']
#         m.save()
#         return 