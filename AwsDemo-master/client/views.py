from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import ImportData
import re 

# Create your views here.
def sign_up(request,template_name='auth/signup.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        first_name = postdata.get('first_name','')
        last_name = postdata.get('last_name','')
        email = postdata.get('email','')
        dob = postdata.get('dob','')
        password = postdata.get('password','')
        print('*** first_name ***',first_name)
        print('*** last_name ***',last_name)
        print('*** email ***',email)
        print('*** dob ***',dob)
        print('*** password ***',password)
    return render(request,template_name,locals())

def hello(request,template_name='hello.html'):
    return render(request,template_name,locals())    

def csv(request,template_name='csv.html'):
    import logging
    import csv
    import os
    from TestProject.settings import BASE_DIR
    from django.conf import settings
    from django.core.files.storage import FileSystemStorage
    csv_data_list = []
    csv_data_dict = {}

    if request.method == 'POST':
        postdata = request.POST.copy()
        file = request.FILES["upload_csv"]
        if not file.name.endswith('.csv'):
            messages.add_message(request, messages.ERROR, 'Please upload a csv file.',fail_silently=True)
            url = urlresolvers.reverse('client:csv')
            return HttpResponseRedirect(url)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        csvfile = fs.url(filename)    
        # csvfile = BASE_DIR+'static/import_csv/' + filename

        with open(csvfile, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        #loop over the lines and save them in db. If error , store as string and then display
        loop_count = 0
        with open(csvfile, encoding='utf-8',errors='ignore') as data_file:
            reader = csv.reader(data_file)
            print('*** reader **',reader)
            for fields in reader:
                print('***** fields *****',fields)
                print('*** loop_count ***',loop_count )
                if loop_count >= 1:
                    error_log = ""
                    name = fields[0]
                    email = fields[1]
                    phone = fields[2]
                    city = fields[3]
                    country = fields[4]

                    print('***name****',name)
                    print('***email****',email)
                    print('***phone****',phone)
                    print('***city****',city)
                    print('***country****',country)
                    csv_data_dict['name'] = name
                    csv_data_dict['email'] = email
                    csv_data_dict['phone'] = phone
                    csv_data_dict['city'] = city
                    csv_data_dict['country'] = country
                    csv_data_list.append(csv_data_dict.copy())
                    ############ RUN VALIDATIONS ##################
                    add_data = True
                    if not name:
                        error_log += "- First Name is Complusary <br/>"
                        add_data = False
                    if not email:
                        error_log += "- Please add email <br/>"
                        add_data = False
                    if  not phone:
                        error_log += "- Please add phone number <br/>"
                        add_data = False
                    if  not city:
                        error_log += "- Please add country <br/>"
                        add_data = False
                    if  not country:
                        error_log += "- Please add country <br/>"
                        add_data = False        

                    if phone:
                        if len(phone) < 10 or len(phone) > 10:
                            error_log += "- Wrong Phone Number <br/>"
                            add_data = False

                    if not city.isalpha() or city.isspace():
                        error_log += "- city should only in alpha <br/>"
                        add_data = False 

                    if not name.isalpha() or name.isspace():
                        error_log += "- name should only in alpha <br/>"
                        add_data = False            

                    if not country.isalpha() or city.isspace():
                        error_log += "- country should only in alpha <br/>"
                        add_data = False   

                    if email:
                        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'   
                        if not re.search(regex,email):
                            error_log += "- email should be in proper format <br/>"
                            add_data = False   


                    import_data = ImportData()
                    import_data.name = name
                    import_data.email = email
                    import_data.phone = phone
                    import_data.city = city
                    import_data.country = country
                    import_data.save()

                loop_count += 1

        if os.path.exists(csvfile):
            os.remove(csvfile)
        else:
          print("The file does not exist")

    if request.POST.get('customer_import_save',False) == 'Validate CSV':
           messages.add_message(request, messages.SUCCESS, 'Your customers have been imported to the system.',fail_silently=True)
        #    url = reverse('client:csv')
        #    return HttpResponseRedirect(url)
    return render(request,template_name,locals())            