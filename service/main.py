from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import quote as urlquote
from youtrack_functions.IssuedAttributesQueries import *
app             = Flask(__name__)

sesam_jwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE1Njg3MTk1MTguNDA3ODQ4MSwiZXhwIjoxNjAwMzQxNzA4LCJ1c2VyX2lkIjoiNDI1YzQ3YTctNWE4Yi00ZjY1LWEyYzQtMTljNzNiZmRmNGQ3IiwidXNlcl9wcm9maWxlIjp7ImVtYWlsIjoiZXJpay5sZXZlbkBzZXNhbS5pbyIsIm5hbWUiOiJlcmlrLmxldmVuQHNlc2FtLmlvIiwicGljdHVyZSI6Imh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyLzZjYmQxYjkyNTQwNWMyOTVkN2ZmYWQ5M2Y2ODRlODQ2P3M9NDgwJnI9cGcmZD1odHRwcyUzQSUyRiUyRmNkbi5hdXRoMC5jb20lMkZhdmF0YXJzJTJGZWEucG5nIn0sInVzZXJfcHJpbmNpcGFsIjoiZ3JvdXA6RXZlcnlvbmUiLCJwcmluY2lwYWxzIjp7IjBiMDhiNTBiLTZkNDAtNGI4MC1iZDI4LWMzMDM2NjA2NWRhNSI6WyJncm91cDpBZG1pbiJdfSwiYXBpX3Rva2VuX2lkIjoiZjBmMDM0MjctZDdjNi00MGQ5LTk5ZDYtODcxZjgzNjc0Njk5In0.lnlhxqwFX28IK85pEEsL7S8lVqGU4-agM3cqRkhQ0cA8Km9-Gu3nhpPiW5lisY4WFjTrw_Fcnq7hffRKLEn4wCA1gJhMi0HAZ5Kboykb_2XMcKCxa21AZHg-wa0AM8x23-WZ9zrfMuXKZgJFHzjOEmqM19SZLMMG-hHY_56YQq5MFJ_HyURmbiO9XR7f6qwhDkvz8kHdT3DzZFxYMTeExVnVQeE3zL0p_zI3SsdcPE5fIPDlydwXr71Za79GGGkkgEzaJaULuz_IdKTyk0ZA7g5e7zId-ElVcjGXNURcGpL_op70N3A9jG1v8TaQon9PyCViCHIArbCadSreHtrNUw'
node_id = 'datahub-0b08b50b'
pipe_name = 'youtrack-issues'
token = 'perm:U2VzYW0=.NTgtMg==.18QKfjc5OrEm4WUR01PR1QfFh4FBfm'
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
    fields_query = post_fields_query(all_nested_attributes, issue_attributes, nested_attributes)

    ############### deleted:False virker ikke!
    entity_ok   = {'summary':'this is a testsummary','idReadable': 'TEST-9', 'comments': [{'$type': 'IssueComment','text':'checking update','textPreview': '<div class="wiki text prewrapped">checking update</div>\n'}], 'commentsCount': 1, 'description': 'ye', 'project': {'$type': 'Project', 'description': None, 'id':'0-4'}}
    entity_ok1   = {'summary':'this is a testsummary2','idReadable': None,'comments': [{'$type': 'IssueComment','text':'checking update2','textPreview': '<div class="wiki text prewrapped">checking update2</div>\n'}], 'commentsCount': 1, 'description': 'ye', 'project': {'$type': 'Project', 'description': None, 'id':'0-4'}}
    #entity_fail = {'attachments': [], 'comments': [{'$type': 'IssueComment','deleted':False, 'created': 1568725990755, 'text': 'this is the first update comment', 'textPreview': '<div class="wiki text prewrapped">this is the first update comment</div>\n'}], 'commentsCount': 1, 'created': 1568722688398, 'customFields': [{'$type': 'SingleEnumIssueCustomField', 'id': '102-110', 'name': 'Priority', 'projectCustomField': {'$type': 'EnumProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-1', 'name': 'Priority'}, 'id': '102-110'}, 'value': {'$type': 'EnumBundleElement', 'color': {'$type': 'FieldStyle', 'id': '17'}, 'id': '81-3', 'localizedName': None, 'name': 'Normal'}}, {'$type': 'SingleUserIssueCustomField', 'id': '104-28', 'name': 'Assignee', 'projectCustomField': {'$type': 'UserProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-4', 'name': 'Assignee'}, 'id': '104-28'}, 'value': None}, {'$type': 'StateIssueCustomField', 'id': '102-109', 'name': 'Stage', 'projectCustomField': {'$type': 'StateProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-112', 'name': 'Stage'}, 'id': '102-109'}, 'value': {'$type': 'StateBundleElement', 'color': {'$type': 'FieldStyle', 'id': '0'}, 'id': '83-60', 'isResolved': False, 'localizedName': None, 'name': 'Backlog'}}, {'$type': 'SingleEnumIssueCustomField', 'id': '102-108', 'name': 'Kanban State', 'projectCustomField': {'$type': 'EnumProjectCustomField', 'field': {'$type': 'CustomField', 'id': '75-48', 'name': 'Kanban State'}, 'id': '102-108'}, 'value': {'$type': 'EnumBundleElement', 'color': {'$type': 'FieldStyle', 'id': '16'}, 'id': '81-252', 'localizedName': None, 'name': 'Ready to pull'}}], 'description': 'ye', 'draftOwner': None, 'externalIssue': None, 'idReadable': 'TEST-13', 'isDraft': False, 'numberInProject': 13, 'parent': {'$type': 'IssueLink', 'direction': 'INWARD'}, 'project': {'$type': 'Project', 'description': None, 'iconUrl': '/hub/api/rest/projects/1c2717b6-b9bc-4fce-956b-220b8c45db4c/icon?etag=MjYtNzg%3D', 'id': '0-4', 'name': 'test', 'shortName': 'TEST'}, 'reporter': {'$type': 'User', 'avatarUrl': '/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48', 'email': 'youtrack-admin@sesam.in', 'fullName': 'Sesam', 'guest': False, 'jabberAccountName': None, 'login': 'Sesam', 'ringId': '68698611-80a9-486e-aebb-aee1d5601fdf'}, 'resolved': None, 'subtasks': {'$type': 'IssueLink', 'direction': 'OUTWARD'}, 'summary': 'TEST-7', 'tags': [], 'updated': 1568807121576, 'updater': {'$type': 'User', 'avatarUrl': '/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48', 'email': 'youtrack-admin@sesam.in', 'fullName': 'Sesam', 'guest': False, 'jabberAccountName': None, 'login': 'Sesam', 'ringId': '68698611-80a9-486e-aebb-aee1d5601fdf'}, 'usesMarkdown': False, 'visibility': {'$type': 'UnlimitedVisibility'}, 'voters': {'$type': 'IssueVoters', 'hasVote': False}, 'votes': 0, 'watchers': {'$type': 'IssueWatchers', 'hasStar': False}, 'wikifiedDescription': '<div class="wiki text prewrapped">ye</div>\n'}

    entities = [entity_ok, entity_ok1]#, entity_fail]
    for i, entity in enumerate(entities):
        if entity['idReadable'] == None:
            del entity['idReadable']
            url = 'https://sesam.myjetbrains.com/youtrack/api/issues?{}'.format(fields_query)            
        else:
            url = 'https://sesam.myjetbrains.com/youtrack/api/issues/{}?{}'.format(entity['idReadable'], fields_query)
        response = requests.post(url, headers = Youtrack_headers, json=entity)
        if response.status_code != 200:
            return print ('Entity {} failed with response {}'.format(i, response))
    return print(response)

@app.route('/get_youtrack_issues', methods=['GET'])
def get_youtrack_issues():  
    all_nested_attributes, issue_attributes, nested_attributes = get_issue_attributes()
    fields_query = get_fields_query(all_nested_attributes, issue_attributes, nested_attributes)
    pagination = set_pagination(0, 20)
    query = urlquote('updated: 2015-01-01T12:00 .. Today')
    url = 'https://sesam.myjetbrains.com/youtrack/api/issues?query={}&'.format(query) + fields_query + pagination
    response = requests.get(url, headers = Youtrack_headers)
    if response.status_code == 200:
       return response.json()#jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)

def circle_func():
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
