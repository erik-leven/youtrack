from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import quote as urlquote
from query_data import *
from auth import *
from youtrack_functions.IssuedAttributesQueries import *
app             = Flask(__name__)

node_id = 'datahub-0b08b50b'
sesam_issues_dataset_name = 'youtrack-issues'
sesam_projects_dataset_name = 'youtrack-projects'
Youtrack_headers     = {'Authorization': 'Bearer {}'.format(token),'Content-Type': 'application/json','Accept': 'application/json'}
#headers = {'Accept': 'application/json','Authorization': 'Bearer ' + token,'Content-Type': 'application/json'}
Sesam_headers = {'Authorization': "Bearer {}".format(sesam_jwt)}


@app.route('/youtrack_issues_to_sesam', methods=['GET'])
def youtrack_issues_to_sesam(issues):
    response = requests.post("https://datahub-0b08b50b.sesam.cloud/api/receivers/youtrack-issues-http/entities", headers=Sesam_headers, data=json.dumps(issues))
    return response.json()

@app.route('/youtrack_projects_to_sesam', methods=['GET'])
def youtrack_projects_to_sesam(projects):
    response = requests.post("https://datahub-0b08b50b.sesam.cloud/api/receivers/youtrack-projects-http/entities", headers=Sesam_headers, data=json.dumps(projects))
    return response.json()

@app.route('/get_sesam_issues_entities', methods=['GET'])
def get_sesam_issues_entities():
    Sesam_headers = {'Authorization': "Bearer {}".format(sesam_jwt)}
    response = requests.get("https://%s.sesam.cloud/api/datasets/%s/entities?history=false" % (node_id, sesam_issues_dataset_name), headers = Sesam_headers)
    return response.json()

@app.route('/get_sesam_projects_entities', methods=['GET'])
def get_sesam_projects_entities():
    Sesam_headers = {'Authorization': "Bearer {}".format(sesam_jwt)}
    response = requests.get("https://%s.sesam.cloud/api/datasets/%s/entities?history=false" % (node_id, sesam_projects_dataset_name), headers = Sesam_headers)
    return response.json()

@app.route('/post_youtrack_issues', methods=['GET','POST'])
def post_youtrack_issues(entities):
    fields_query = make_issues_fields_query()
    for i, entity in enumerate(entities):
        try:
            entity['idReadable']
            if entity['idReadable'] == None:
                del entity['idReadable']
                url = 'https://sesam.myjetbrains.com/youtrack/api/issues'#?{}'.format(fields_query)            
            else:
                #url = 'https://sesam.myjetbrains.com/youtrack/api/issues/{}?{}'.format(entity['idReadable'], fields_query)
                url = 'https://sesam.myjetbrains.com/youtrack/api/issues/{}'.format(entity['idReadable'])
        except KeyError:
            url = 'https://sesam.myjetbrains.com/youtrack/api/issues' 
        response = requests.post(url, headers = Youtrack_headers, json=entity)
        if response.status_code != 200:
            return print ('Entity {} failed with response {}'.format(i, response))
        else:
            print(response.status_code)
    #return print(response)

@app.route('/put_youtrack_projects', methods=['GET','POST','PUT'])
def put_youtrack_projects(entities):
    for i, entity in enumerate(entities):
        customfields = entity['customFields']
        print(entity)
        del entity['customFields']
        try:
            entity['id']
            entity['startingNumber'] = 1
            print(entity)
            if entity['id'] == None:
                del entity['id']
                url = 'https://sesam.myjetbrains.com/youtrack/api/projects'#?{}'.format(fields_query)            
            else:
                #url = 'https://sesam.myjetbrains.com/youtrack/api/issues/{}?{}'.format(entity['idReadable'], fields_query)
                print(1)
                print(entity)
                print(entity['id'])
                main_query = make_projects_fields_query() 
                print(main_query)
                url = 'https://sesam.myjetbrains.com/youtrack/api/admin/projects/{}'.format(entity['id'])
                print(url)
                #url = 'https://sesam.myjetbrains.com/youtrack/api/rest/admin/projects/0-10??projectName=Communism&startingNumber=1&projectLeadLogin=lenin&description=You+know'
        except KeyError:
            url = 'https://sesam.myjetbrains.com/youtrack/api/projects' 
        response = requests.put(url, headers = Youtrack_headers, json=entity)
        if response.status_code != 201:
            return print ('Entity {} failed with response {}'.format(i, response))
        else:
            print('----------------------------------')
            print(response.status_code)
    #return print(response)

@app.route('/get_youtrack_issues', methods=['GET'])
def get_youtrack_issues():  
    #all_nested_attributes, issue_attributes, nested_attributes = get_issue_attributes()
    fields_query = make_issues_fields_query()
    pagination = set_pagination(0, 20)
    query = urlquote('updated: 2015-01-01T12:00 .. Today')
    url = 'https://sesam.myjetbrains.com/youtrack/api/issues?query={}&'.format(query) + fields_query + pagination
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)

@app.route('/get_youtrack_projects', methods=['GET'])
def get_youtrack_projects():  
    main_query = make_projects_fields_query()
    url = 'https://sesam.myjetbrains.com/youtrack/api/admin/projects?{}'.format(main_query)
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code != 200:
        #logger.error(...)
        print('Error code {}'.format(response.status_code))
    else:
        projects = response.json()

    costomfields_query = make_projects_fields_query_customfields()
    for project in projects:
        url = 'https://sesam.myjetbrains.com/youtrack/api/admin/projects/{}/fields?{}'.format(project['id'],costomfields_query)
        print(url)
        response = requests.get(url, headers = Youtrack_headers)
        if response.status_code != 200:
            #logger.error(...)
            print('Error code {}'.format(response.status_code))
        else:
            customfields = response.json()
            project['customFields'] = customfields
    return projects

@app.route('/get_youtrack_users', methods=['GET'])
def get_youtrack_users():  
    fields_query = make_users_fields_query()
    url = 'https://sesam.myjetbrains.com/youtrack/api/admin/users?{}'.format(fields_query)
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)

@app.route('/get_youtrack_telemetry', methods=['GET'])
def get_youtrack_telemetry():
    user_attributes  = get_user_attributes()
    fields_query = get_user_fields_query(user_attributes)
    url = 'https://sesam.myjetbrains.com/youtrack/api/admin/users?{}'.format(fields_query)
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)

@app.route('/get_youtrack_group', methods=['GET'])
def get_youtrack_group():  

    ############################### No groups exists"



    #user_attributes  = get_user_attributes()
    #fields_query = get_user_fields_query(user_attributes)
    url = 'https://sesam.myjetbrains.com/youtrack/api/admin/group'#?{}'.format(fields_query)
    response = requests.get(url, headers = Youtrack_headers)

    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return print('Error code {}'.format(response.status_code))

@app.route('/get_youtrack_roles', methods=['GET'])
def get_youtrack_roles():  
    url = 'https://sesam.myjetbrains.com/hub/api/rest/roles'
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return print('Error code {}'.format(response.status_code))

@app.route('/get_youtrack_agiles', methods=['GET'])
def get_youtrack_agiles():  
    user_attributes  = get_user_attributes()
    fields_query = get_user_fields_query(user_attributes)
    #url = 'https://sesam.myjetbrains.com/youtrack/api/admin/users?{}'.format(fields_query)
    url = 'https://sesam.myjetbrains.com/youtrack/api/agiles?fields=name,owner,visibleFor,visibleForProjectBased,updateableBy,updateableByProjectBased,orphansAtTheTop,hideOrphansSwimlane,estimationField,projects(name),sprints,currentSprint,columnSettings,swimlaneSettings,sprintsSettings,colorCodingstatus'
    
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)

def circle_func():
    entities = get_youtrack_projects()
    #ss
    #[{'fullName': '3020@statnett.no', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': '3020@statnett.no', 'avatarUrl': '/hub/api/rest/avatar/78ded999-838f-4bbe-be7a-1c06f50fc4d1?s=48', 'online': False, 'id': '1-215', '$type': 'User'}, {'fullName': 'Adam Somorjai', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'adam_somorjai', 'avatarUrl': '/hub/api/rest/avatar/eb94ec6e-749b-4e5d-be5c-a63aeb47e62b?s=48', 'online': False, 'id': '1-218', '$type': 'User'}, {'fullName': 'Adam Somorjai', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'somorjai.adam@gmail.com', 'avatarUrl': '/hub/api/rest/avatar/32faf286-7c9b-4389-a854-be5d9e0a4003?s=48', 'online': False, 'id': '1-228', '$type': 'User'}, {'fullName': 'Akanksha Sood', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'akanksha.sood', 'avatarUrl': '/hub/api/rest/avatar/a7341ea0-dd18-4ee0-b177-a6e2a90b251d?s=48', 'online': False, 'id': '1-210', '$type': 'User'}, {'fullName': 'Alf Lervåg [X]', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'alf.lervag', 'avatarUrl': '/hub/api/rest/avatar/c5798490-2475-4f7c-bb84-18a5d69508c1?s=48', 'online': False, 'id': '1-24', '$type': 'User'}, {'fullName': 'Anders Borud', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'anders.borud', 'avatarUrl': '/hub/api/rest/avatar/e03f72a7-84f2-4e4f-be48-76451b163935?s=48', 'online': False, 'id': '1-42', '$type': 'User'}, {'fullName': 'Anders Dolve', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'anders.dolve@statnett.no', 'avatarUrl': '/hub/api/rest/avatar/df4e7949-e5ee-4349-b824-bd676a067230?s=48', 'online': False, 'id': '1-212', '$type': 'User'}, {'fullName': 'Anders Volle', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'anders.volle', 'avatarUrl': '/hub/api/rest/avatar/faccccb1-4822-4adf-b3a7-422461ec88af?s=48', 'online': False, 'id': '1-33', '$type': 'User'}, {'fullName': 'anders.berg@statnett.no', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'anders.berg@statnett.no', 'avatarUrl': '/hub/api/rest/avatar/035429f7-8c12-490b-8da4-6241151be637?s=48', 'online': False, 'id': '1-207', '$type': 'User'}, {'fullName': 'Andreas Hysing', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'andreas.hysing', 'avatarUrl': '/hub/api/rest/avatar/b2a7779e-fb25-42d1-834e-0581cdecff53?s=48', 'online': False, 'id': '1-32', '$type': 'User'}, {'fullName': 'Andreas Minge', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'andreas.minge@embriq.no', 'avatarUrl': '/hub/api/rest/avatar/1c888bd7-f486-42d3-92a6-7ff60b537a11?s=48', 'online': False, 'id': '1-152', '$type': 'User'}, {'fullName': 'Andreas Stusvik Haug', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'andreas-stusvik.haug@capgemini.com', 'avatarUrl': '/hub/api/rest/avatar/1cabf266-a51b-4536-9d77-1c350c2dd19f?s=48', 'online': False, 'id': '1-219', '$type': 'User'}, {'fullName': 'Andreas.Minge@rejlers.no', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'andreas.minge@rejlers.no', 'avatarUrl': '/hub/api/rest/avatar/7396913d-4ec3-4586-ac30-0d470d3f8a61?s=48', 'online': False, 'id': '1-222', '$type': 'User'}, {'fullName': 'Anton Lavrentiev [X]', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'anton_lavrentiev', 'avatarUrl': '/hub/api/rest/avatar/fc5a279e-60cf-4ffa-a84e-6f47ad7d81af?s=48', 'online': False, 'id': '1-149', '$type': 'User'}, {'fullName': 'ARE RØSSUM-HAALAND', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'are.rossum-haaland@hafslund.no', 'avatarUrl': '/hub/api/rest/avatar/ed89a720-c5fb-41b4-9e97-58ea0a2588b7?s=48', 'online': False, 'id': '1-203', '$type': 'User'}, {'fullName': 'Arnar Lundesgaard', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'arnar.lundesgaard', 'avatarUrl': '/hub/api/rest/avatar/84ca9468-bcfd-4eab-91e6-e0464f2e95d6?s=48', 'online': False, 'id': '1-34', '$type': 'User'}, {'fullName': 'Arne Krossbakken', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'arne.krossbakken', 'avatarUrl': '/hub/api/rest/avatar/a436563d-20ee-452b-abf5-224eea4cc59d?s=48', 'online': False, 'id': '1-98', '$type': 'User'}, {'fullName': 'Ashkan Vahidishams', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'ashkan.vahidishams', 'avatarUrl': '/hub/api/rest/avatar/319298bd-3adf-4d01-9281-84eaeed340aa?s=48', 'online': False, 'id': '1-40', '$type': 'User'}, {'fullName': 'Ashkan.vahidishams@sesam.io', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'ashkan.vahidishams@sesam.io', 'avatarUrl': '/hub/api/rest/avatar/58faa225-ceca-48da-b175-c0a15aa31858?s=48', 'online': False, 'id': '1-157', '$type': 'User'}, {'fullName': 'Attila Tenkes', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'attila_tenkes', 'avatarUrl': '/hub/api/rest/avatar/1b79f28d-4e5c-4c74-8d3c-93af642b7574?s=48', 'online': False, 'id': '1-211', '$type': 'User'}, {'fullName': 'Axel Borge', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'axel.borge', 'avatarUrl': '/hub/api/rest/avatar/27562d66-f80d-410b-a633-26034aa5bc2c?s=48', 'online': False, 'id': '1-17', '$type': 'User'}, {'fullName': 'Axel Borge', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'axel.borge@gmail.com', 'avatarUrl': '/hub/api/rest/avatar/0dade354-f252-4246-a781-883f3dc2be43?s=48', 'online': False, 'id': '1-168', '$type': 'User'}, {'fullName': 'axel.borge@sesam.io', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'axel.borge@sesam.io', 'avatarUrl': '/hub/api/rest/avatar/59f6202a-6a08-40b9-b117-f2684718287a?s=48', 'online': False, 'id': '1-160', '$type': 'User'}, {'fullName': 'Baard Johansen', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'baard.johansen', 'avatarUrl': '/hub/api/rest/avatar/71279b91-ae53-4b3b-9c2e-3da943e84164?s=48', 'online': True, 'id': '1-2', '$type': 'User'}, {'fullName': 'baard.johansen@sesam.io', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'baard.johansen@sesam.io', 'avatarUrl': '/hub/api/rest/avatar/08783152-7f8f-43a1-8494-e640ba7365fb?s=48', 'online': False, 'id': '1-137', '$type': 'User'}, {'fullName': 'baardern@gmail.com', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'baardern@gmail.com', 'avatarUrl': '/hub/api/rest/avatar/cc2bd113-4d1d-431b-a83e-a3f8e545eb35?s=48', 'online': False, 'id': '1-245', '$type': 'User'}, {'fullName': 'Bjørn Erik Noraas [X]', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'bjorn_noraas', 'avatarUrl': '/hub/api/rest/avatar/0b8eb033-9969-4d01-a7d2-dafe57c530b3?s=48', 'online': False, 'id': '1-150', '$type': 'User'}, {'fullName': 'Bjørn-Ole Johansen', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'boj@ra.no', 'avatarUrl': '/hub/api/rest/avatar/860cc0fd-6584-4e45-8c00-50d09a8dd806?s=48', 'online': False, 'id': '1-133', '$type': 'User'}, {'fullName': 'Branislav Jenco', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'branislav.jenco', 'avatarUrl': '/hub/api/rest/avatar/eea89d70-2e8f-4079-95e6-f0813f02e7b8?s=48', 'online': True, 'id': '1-5', '$type': 'User'}, {'fullName': 'Camilla Jakobsen', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'camilla.jakobsen@statnett.no', 'avatarUrl': '/hub/api/rest/avatar/5b095ee7-a596-45d4-8507-0156604d1f19?s=48', 'online': False, 'id': '1-130', '$type': 'User'}, {'fullName': 'Carina Solito de Solis [X]', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'carina.desolis', 'avatarUrl': '/hub/api/rest/avatar/7e23d018-d43a-4d5a-bf58-310a364fbacc?s=48', 'online': False, 'id': '1-57', '$type': 'User'}, {'fullName': 'Cathrine.Kullebund@kreftforeningen.no', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'cathrine.kullebund@kreftforeningen.no', 'avatarUrl': '/hub/api/rest/avatar/0b132a92-cb71-4985-9b90-49754b718b97?s=48', 'online': False, 'id': '1-202', '$type': 'User'}, {'fullName': 'Christian Stensholt', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'christian.stensholt', 'avatarUrl': '/hub/api/rest/avatar/a2515944-04ad-41b9-b7c5-20316f7b3c46?s=48', 'online': False, 'id': '1-25', '$type': 'User'}, {'fullName': 'christian_valland', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'christian_valland', 'avatarUrl': '/hub/api/rest/avatar/a5123a61-7bf5-4012-84aa-6d338b6296bb?s=48', 'online': False, 'id': '1-136', '$type': 'User'}, {'fullName': 'Craig Seamons', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'craig.seamons', 'avatarUrl': '/hub/api/rest/avatar/1be6db9f-7976-4be7-92a1-012008c16308?s=48', 'online': False, 'id': '1-76', '$type': 'User'}, {'fullName': 'Cristina Lie [X]', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': True, 'login': 'cristina.lie', 'avatarUrl': '/hub/api/rest/avatar/482b1c41-5b3f-4517-b219-6183d22d2b08?s=48', 'online': False, 'id': '1-6', '$type': 'User'}, {'fullName': 'dale.ole.morten@gmail.com', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'dale.ole.morten@gmail.com', 'avatarUrl': '/hub/api/rest/avatar/0031cbda-3cb9-46f7-a85f-16599ad36ff9?s=48', 'online': False, 'id': '1-173', '$type': 'User'}, {'fullName': 'do-not-reply@stackoverflow.email', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'do-not-reply@stackoverflow.email', 'avatarUrl': '/hub/api/rest/avatar/5952f66e-2e1d-464f-b9f6-8d01655d2a0d?s=48', 'online': False, 'id': '1-227', '$type': 'User'}, {'fullName': 'Duy Dinh-Steffensen', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'duy.dinh', 'avatarUrl': '/hub/api/rest/avatar/da157935-f1c5-4161-a126-40f60cfaba83?s=48', 'online': False, 'id': '1-56', '$type': 'User'}, {'fullName': 'Eirik Sander-Fjeld', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'eirik.sander-fjeld', 'avatarUrl': '/hub/api/rest/avatar/18ab4a54-b0f3-42ee-8fe9-b256f9617003?s=48', 'online': False, 'id': '1-153', '$type': 'User'}, {'fullName': 'Eivind Engesæter', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'eivind.engeseter', 'avatarUrl': '/hub/api/rest/avatar/506999c1-e33a-4cec-818a-1162a37b531e?s=48', 'online': False, 'id': '1-50', '$type': 'User'}, {'fullName': 'Ekaterina Yurchenko', 'tags': [], 'savedQueries': [], 'profiles': {'$type': 'UserProfiles'}, 'banned': False, 'login': 'ekaterina.yurchenko', 'avatarUrl': '/hub/api/rest/avatar/ca2e7153-e309-48fd-ad9e-744f23f461b6?s=48', 'online': False, 'id': '1-165', '$type': 'User'}]

    projects = put_youtrack_projects(entities)
    print(projects)
    ss
    for project in projects:
        project["_id"] = project['id']
    youtrack_projects_to_sesam(projects)
    
    projects = get_sesam_projects_entities()
    projects = remove_sesam_system_attributes(projects)
    #print(entities)

    put_youtrack_projects(projects)
    #print(issues)
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    circle_func()
