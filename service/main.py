from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import quote as urlquote
from query_data import *
from auth import *
from youtrack_functions.IssuedAttributesQueries import *
app             = Flask(__name__)

node_id = 'datahub-0b08b50b'
pipe_name = 'youtrack-issues'
Youtrack_headers     = {'Authorization': 'Bearer {}'.format(token),'Content-Type': 'application/json','Accept': 'application/json'}
#headers = {'Accept': 'application/json','Authorization': 'Bearer ' + token,'Content-Type': 'application/json'}
Sesam_headers = {'Authorization': "Bearer {}".format(sesam_jwt)}


@app.route('/youtrack_to_sesam', methods=['GET'])
def youtrack_to_sesam(issues):
    response = requests.post("https://datahub-0b08b50b.sesam.cloud/api/receivers/youtrack-http/entities", headers=Sesam_headers, data=json.dumps(issues))
    return response.json()


@app.route('/get_sesam_entities', methods=['GET'])
def get_sesam_entities():
    Sesam_headers = {'Authorization': "Bearer {}".format(sesam_jwt)}
    response = requests.get("https://%s.sesam.cloud/api/datasets/%s/entities?history=false" % (node_id, pipe_name), headers = Sesam_headers)
    return response.json()


@app.route('/post_youtrack_issues', methods=['GET','POST'])
def post_youtrack_issues(entities):
    all_nested_attributes, issue_attributes, nested_attributes = get_issue_attributes()
    fields_query = post_issues_fields_query(all_nested_attributes, issue_attributes, nested_attributes)

    ############### deleted:False virker ikke!
    entity_ok   = {'summary':'this is a testsummary','idReadable': 'TEST-9', 'comments': [{'$type': 'IssueComment','text':'checking update','textPreview': '<div class="wiki text prewrapped">checking update</div>\n'}], 'commentsCount': 1, 'description': 'ye', 'project': {'$type': 'Project', 'description': None, 'id':'0-4'}}
    #entity_ok1   = {'summary':'this is a testsummary2','idReadable': None,'comments': [{'$type': 'IssueComment','text':'checking update2','textPreview': '<div class="wiki text prewrapped">checking update2</div>\n'}], 'commentsCount': 1, 'description': 'ye', 'project': {'$type': 'Project', 'description': None, 'id':'0-4'}}
    #entity_fail = {'attachments': [], 'comments': [{'$type': 'IssueComment','deleted':False, 'created': 1568725990755, 'text': 'this is the first update comment', 'textPreview': '<div class="wiki text prewrapped">this is the first update comment</div>\n'}], 'commentsCount': 1, 'created': 1568722688398, 'customFields': [{'$type': 'SingleEnumIssueCustomField', 'id': '102-110', 'name': 'Priority', 'projectCustomField': {'$type': 'EnumProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-1', 'name': 'Priority'}, 'id': '102-110'}, 'value': {'$type': 'EnumBundleElement', 'color': {'$type': 'FieldStyle', 'id': '17'}, 'id': '81-3', 'localizedName': None, 'name': 'Normal'}}, {'$type': 'SingleUserIssueCustomField', 'id': '104-28', 'name': 'Assignee', 'projectCustomField': {'$type': 'UserProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-4', 'name': 'Assignee'}, 'id': '104-28'}, 'value': None}, {'$type': 'StateIssueCustomField', 'id': '102-109', 'name': 'Stage', 'projectCustomField': {'$type': 'StateProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-112', 'name': 'Stage'}, 'id': '102-109'}, 'value': {'$type': 'StateBundleElement', 'color': {'$type': 'FieldStyle', 'id': '0'}, 'id': '83-60', 'isResolved': False, 'localizedName': None, 'name': 'Backlog'}}, {'$type': 'SingleEnumIssueCustomField', 'id': '102-108', 'name': 'Kanban State', 'projectCustomField': {'$type': 'EnumProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-48', 'name': 'Kanban State'}, 'id': '102-108'}, 'value': {'$type': 'EnumBundleElement', 'color': {'$type': 'FieldStyle', 'id': '16'}, 'id': '81-252', 'localizedName': None, 'name': 'Ready to pull'}}], 'description': 'ye', 'draftOwner': None, 'externalIssue': None, 'idReadable': 'TEST-13', 'isDraft': False, 'numberInProject': 13, 'parent': {'$type': 'IssueLink', 'direction': 'INWARD'}, 'project': {'$type': 'Project', 'description': None, 'iconUrl': '/hub/api/rest/projects/1c2717b6-b9bc-4fce-956b-220b8c45db4c/icon?etag=MjYtNzg%3D', 'id': '0-4', 'name': 'test', 'shortName': 'TEST'}, 'reporter': {'$type': 'User', 'avatarUrl': '/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48', 'email': 'youtrack-admin@sesam.in', 'fullName': 'Sesam', 'guest': False, 'jabberAccountName': None, 'login': 'Sesam', 'ringId': '68698611-80a9-486e-aebb-aee1d5601fdf'}, 'resolved': None, 'subtasks': {'$type': 'IssueLink', 'direction': 'OUTWARD'}, 'summary': 'TEST-7', 'tags': [], 'updated': 1568807121576, 'updater': {'$type': 'User', 'avatarUrl': '/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48', 'email': 'youtrack-admin@sesam.in', 'fullName': 'Sesam', 'guest': False, 'jabberAccountName': None, 'login': 'Sesam', 'ringId': '68698611-80a9-486e-aebb-aee1d5601fdf'}, 'usesMarkdown': False, 'visibility': {'$type': 'UnlimitedVisibility'}, 'voters': {'$type': 'IssueVoters', 'hasVote': False}, 'votes': 0, 'watchers': {'$type': 'IssueWatchers', 'hasStar': False}, 'wikifiedDescription': '<div class="wiki text prewrapped">ye</div>\n'}
    entity_try = {'description': 'ye', 'project': {'$type': 'Project', 'description': None, 'id':'0-4'},'summary':'this is a testsummary','links': [{'direction': 'BOTH', '$type': 'IssueLink'}]}
    entities = [entity_try]#entity_ok]#, entity_fail]
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
    projects = get_youtrack_projects()
    print(projects)
    ss
    for project in projects:
        print(project)
    ss

    issues = get_youtrack_issues()
    for issue in issues:
        issue["_id"] = issue['idReadable']
    youtrack_to_sesam(issues)
    entities = get_sesam_entities()
    entities = remove_sesam_system_attributes(entities)
    post_youtrack_issues(entities)
    #print(issues)
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    circle_func()
