from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import ImportData
import re 

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

        with open(csvfile, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        #loop over the lines and save them in db. If error , store as string and then display
        loop_count = 0
        with open(csvfile, encoding='utf-8',errors='ignore') as data_file:
            reader = csv.reader(data_file)
            for fields in reader:
                if loop_count >= 1:
                    error_log = ""
                    name = fields[0]
                    email = fields[1]
                    phone = fields[2]
                    city = fields[3]
                    country = fields[4]
                    
                    ############ RUN VALIDATIONS ##################
                    add_data = True
                    if not name:
                        messages.add_message(request, messages.ERROR, 'Name is Complusary.',fail_silently=True)
                        add_data = False
                    if not email:
                        messages.add_message(request, messages.ERROR, 'Please add email.',fail_silently=True)
                        add_data = False
                    if  not phone:
                        messages.add_message(request, messages.ERROR, 'Please add phone number.',fail_silently=True)
                        add_data = False
                    if  not city:
                        messages.add_message(request, messages.ERROR, 'Please add country.',fail_silently=True)
                        add_data = False
                    if  not country:
                        messages.add_message(request, messages.ERROR, 'Please add country.',fail_silently=True)
                        add_data = False        

                    if phone:
                        if len(phone) < 10 or len(phone) > 10:
                            messages.add_message(request, messages.ERROR, 'Wrong Phone Number.',fail_silently=True)
                            add_data = False

                    if not city.isalpha() or city.isspace():
                        messages.add_message(request, messages.ERROR, 'city should only in alpha.',fail_silently=True)
                        add_data = False 

                    # if not name.isalpha() or not name.isspace():
                    #     messages.add_message(request, messages.ERROR, 'name should only in alpha.',fail_silently=True)
                    #     add_data = False            

                    if not country.isalpha() or city.isspace():
                        messages.add_message(request, messages.ERROR, 'country should only in alpha.',fail_silently=True)
                        add_data = False   

                    if email:
                        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'   
                        if not re.search(regex,email):
                            messages.add_message(request, messages.ERROR, 'email should be in proper format.',fail_silently=True)
                            add_data = False 

                    if add_data == True:

                        import_data = ImportData()
                        import_data.name = name
                        import_data.email = email
                        import_data.phone = phone
                        import_data.city = city
                        import_data.country = country
                        import_data.save()
                            
                        csv_data_dict['name'] = name
                        csv_data_dict['email'] = email
                        csv_data_dict['phone'] = phone
                        csv_data_dict['city'] = city
                        csv_data_dict['country'] = country
                        csv_data_list.append(csv_data_dict.copy())

                loop_count += 1

    if request.POST.get('customer_import_save',False) == 'Validate CSV':
        if add_data == True:
            messages.add_message(request, messages.ERROR, 'Your data has been imported to the system.',fail_silently=True)
        else:    
            messages.add_message(request, messages.ERROR, 'Improper data imported to the system.',fail_silently=True)
    return render(request,template_name,locals())            