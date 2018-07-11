from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import ImportFile
from QuChemPedIA.models import Software
from QuChemPedIA.models import SoftwareVersion
from QuChemPedIA.models import ImportRule
from QuChemPedIA.QuChemPedIA_lib.import_file_lib import import_file, get_path_to_store
from QuChemPedIA.QuChemPedIA_lib import store_in_temp
import datetime
import json


def register_soft_and_version(path_to_file_to_register):
    """
    this method try to know what to do with a json file
    :param path_to_file_to_register: path to the json that could be processed
    :return: 0 for error, 1 for manual, 2 for automatic
    """
    #  on récupère les information pour enregistrer la machine à état
    jsonfile = open(path_to_file_to_register)
    loaded_json = json.load(jsonfile)
    try:
        name_software = loaded_json['comp_details']['general']['package'].strip()
    except Exception as error:
        print("error for getting the software : ")
        print(error)
        return 0
    # try to register the software
    try:
        # we check if it's already exist, if not we register it
        soft, created = Software.objects.get_or_create(name=name_software)
    except Exception as error:
        print("error for registering the software : ")
        print(error)
        return 0

    try:
        version_software = loaded_json['comp_details']['general']['package_version'].strip()
    except Exception as error:
        print("error for getting the version of the software : ")
        print(error)
        return 0

    # try to register the version of the software
    try:
        # we check if it's already exist, if not we register it
        soft_vers, created = SoftwareVersion.objects.get_or_create(version_number=version_software,
                                                                   id_software=soft)
    except Exception as error:
        print("error for registering the version of the software : ")
        print(error)
        return 0

    # try to register the new rules
    try:
        # we check if it's already exist, if not we register it
        rule, created = ImportRule.objects.get_or_create(id_version=soft_vers, id_software=soft)
    except Exception as error:
        print("error for registering the new rule : ")
        print(error)
        return 0
    if rule.rule == "manual":
        return 1
    elif rule.rule == "automatic":
        return 2


def update_status_in_db(result_of_import: int, import_object: ImportFile):
    """
    this function update the status of an import in database
    :param result_of_import: an integer which contains the result of the import function
    :param import_object : current object to update
    :return: nothing
    """
    if result_of_import == 0:
        import_object.status = "imported to database"
    elif result_of_import == 1:
        import_object.status = "calculation already in database"
    elif result_of_import == 2:
        import_object.status = "theory not supported yet"
    elif result_of_import == 3:
        import_object.status = "the opt is missing"
    else:
        import_object.status = "something goes wrong"
    import_object.save()


def import_view(request):
    """
    controler of the template account that allow the user to import file
    :param request: variable wich contains the value of the page
    :return: template html
    """
    path_prefix = 'media/'
    if request.method == 'POST':
        myfile = request.FILES['file']
        #todo add json transform
        temps = ImportFile.objects.create(path_file=path_prefix, id_user=request.user)  # register in database
        final_path = store_in_temp(id_calcul=str(temps.id_file), file=myfile)
        temps.path_file = final_path
        temps.save()
        # adding an import  for this day to the user*
        if request.user.is_authenticated:
            if request.user.last_date_upload != datetime.datetime.today().date() \
                    or request.user.last_date_upload is None:
                request.user.last_date_upload = datetime.datetime.today()
                request.user.number_of_upload_this_day = 1
                request.user.save()
            else:
                request.user.number_of_upload_this_day += 1
                request.user.save()
            request.user.refresh_from_db()
        else:
            #   user == anonymous
            pass
        code_return_pol = register_soft_and_version(path_prefix+final_path)
        if code_return_pol == 0:
            temps.status = "error can't define policy"
            temps.save()
        if code_return_pol == 2:
            #  automatic import
            try:
                path = "media/" + temps.path_file
                update_status_in_db(result_of_import=import_file(path=path, id_user=temps.id_user.id),
                                    import_object=temps)
            except Exception as error:
                print(error)
                temps.status = 'import failed'
                temps.save()
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect('query')
    return render(request, 'QuChemPedIA/import.html', {'query_form': query_form})


def launch_import(request, id_file, page):
    """
    controler from admin view to launch manuallly an import
    :param request: environment variable wich containt all value exchanged between client and server
    :param id_file: id of the file in DB o import in ES
    :param page: number of the page
    :return: html template
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')
    file = ImportFile.objects.get(id_file=id_file)
    path = "media/"+file.path_file
    id_user = file.id_user.id
    try:
        import_file(path=path, id_user=id_user)
        file.delete()
    except Exception as error:
        print(error)
        file.status = 'import failed'
        file.save()
    return HttpResponseRedirect('/QuChemPedIA/admin/list_of_import_in_database?page=' + str(page))
