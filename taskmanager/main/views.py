from django.shortcuts import render
#from models import BenefitImages
# Create your views here.

from django.views.generic.edit import FormView
from .models import Contact, Files
from django.shortcuts import render, get_object_or_404
from .models import User, ActiveApplication, Document, DocumentsInApplication, BenefitSession
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie
import  uuid
import pdb # pdb.set_trace()


def home_page(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')
def user_detail(request, id, benefit):
    #user = get_object_or_404(User, id=id)
    user = User.objects.all()
    print(user)
    return render(request, 'user.html', {'product': user})


def show_application(request, chat_id, session_id, fio, benefit, sum):
    session = BenefitSession.objects.filter(session_id=session_id).first()

    if session:
        return render(request, 'benefit.html', {'chat_id': chat_id,
                                                'session_id': session_id,
                                                'fio': fio,
                                                'benefit': benefit,
                                                'sum': sum})
    else:
        return render(request, 'failure.html')

@ensure_csrf_cookie
def benefit_application(request):
    ##CHECK IF SESSION NOT CLOSED++++++++++
    #CHECK IF USER EXIST
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, request.GET)
        files = request.FILES.getlist('files')
        #user_id = request.GET.get('chat_id')
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            session = BenefitSession.objects.filter(session_id=session_id).first()

            if session:
                session.delete()
                chat_id = form.cleaned_data['chat_id']
                fio = form.cleaned_data['fio']
                benefit = form.cleaned_data['benefit']
                sum = form.cleaned_data['sum']
                print(chat_id)

                user = User.objects.filter(chat_id=chat_id).first()

                app = ActiveApplication.objects.create(chat_id=chat_id,
                                                       fio=fio,
                                                       benefit=benefit,
                                                       sum=sum)

                for f in files:
                    handle_uploaded_file(f, app.pk)
                context = {'msg': '<span style="color: green;">File successfully uploaded</span>'}
                print("render succes html")
                return render(request, "success.html")
            else:
                return render(request, 'failure.html')


    else:
        form = UploadFileForm()
        print("render benefit html")
    return render(request, 'benefit.html', {'form': form})

  #  user = User.objects.filter(chat_id=chat_id).first()
   # return render(request, 'benefit.html', {'chat_id': chat_id,
    #                                        'session_id': session_id,
     #                                       'fio': fio,
      #                                      'benefit': benefit,
       #                                     'sum': sum})

def test(request):
    return render(request, 'benefit.html')


@ensure_csrf_cookie
def upload_multiple_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, request.GET)
        files = request.FILES.getlist('files')
        #user_id = request.GET.get('chat_id')
        if form.is_valid():
            chat_id = form.cleaned_data['chat_id']
            benefit = form.cleaned_data['benefit']
            print(chat_id)

            user = User.objects.filter(chat_id=chat_id).first()

            app = ActiveApplication.objects.create(chat_id=chat_id,
                                                   fio=user.user_fio,
                                                   benefit=benefit,
                                                   sum=100)

            for f in files:
                handle_uploaded_file(f, app.pk)
            context = {'msg' : '<span style="color: green;">File successfully uploaded</span>'}
            return render(request, "list.html", context)
    else:
        form = UploadFileForm()
    return render(request, 'list.html', {'form': form})

def handle_uploaded_file(f, app_id):
    file_name = str(uuid.uuid4()) + ".jpg"
    src = "C:/Users/Operator11/Desktop/WTG/woodTGbot/taskmanager/media/" + \
          file_name

    document = Document.objects.create(document="Документ", image=file_name)
    DocumentsInApplication.objects.create(application_id=app_id, document_id=document.pk)

    with open(src, 'wb') as new_file:
        for chunk in f.chunks():
            new_file.write(chunk)
    #print(f.name)

   # with open(f.name, 'wb+') as destination:
    #    for chunk in f.chunks():
     #       destination.write(chunk)