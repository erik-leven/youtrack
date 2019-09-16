from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import quote as urlquote

app             = Flask(__name__)

def set_pagination(skip, top):
    return '&$skip={}&$top={}'.format(skip, top)

def get_issue_attributes():
    issue_attributes        = ['idReadable', 'created', 'updated', 'resolved', 'numberInProject', 'project', 'summary', 'description','usesMarkdown','wikifiedDescription','reporter','updater','draftOwner','isDraft','visibility','votes','comments','commentsCount','tags','links','externalIssue','customFields','voters','watchers','attachments','subtasks','parent']
    nested_attributes       = ['project','reporter','updater','draftOwner','comments','tags','links','externalIssue','customFields','voters','watchers','attachments','subtasks','parent','projectCustomField','value'] 

    project_keys            = ['shortName','description','archived','fromEmail','replyToEmail','template','iconUrl','name']
    reporter_keys           = ['login','fullName','email','jabberAccountName','ringId','guest','avatarUrl']
    updater_keys            = reporter_keys
    draftOwner_keys         = reporter_keys
    comment_keys            = ['text','usesMarkdown','textPreview','created','updated','deleted']
    tags_keys               = ['name']
    links_keys              = ['direction']
    externalIssue_keys      = ['name','url','key']
    customFields_keys       = ['id', 'projectCustomField','value']
    projectCustomField_keys = ['id', 'field']
    value_keys              = ['avatarUrl','buildLink','color(id)','fullName','id','isResolved','localizedName','login','minutes','name','presentation','text']
    voters_keys             = ['hasVote']
    watcher_keys            = ['hasStar']
    attachments_keys        = ['name', 'created','updated','size','extension','charset','mimeType','metaData','draft','removed','base64Content','url','thumbnailURL']
    subtasks_keys           = ['direction']
    parent_keys             = subtasks_keys
    field_keys              = ['id','name']

    all_nested_attributes = {'project':project_keys,'reporter':reporter_keys,'updater':updater_keys,'draftOwner':draftOwner_keys,'comments':comment_keys,'tags':tags_keys,'links':links_keys,'externalIssue':externalIssue_keys,'customFields':customFields_keys,'voters':voters_keys,'watchers':watcher_keys,'attachments':attachments_keys,'subtasks':subtasks_keys,'parent':parent_keys,'projectCustomField':projectCustomField_keys,'value':value_keys, 'field':field_keys}

    return all_nested_attributes, issue_attributes, nested_attributes

def set_fields_query(all_nested_attributes, issue_attributes, nested_attributes):
    fields = 'fields='
    for i, issue_attribute in enumerate(issue_attributes):
        fields += issue_attribute
        num_issue_attributes = len(issue_attributes)-1
        if issue_attribute in nested_attributes:
            fields += '('
            num_nested_attributes = len(all_nested_attributes[issue_attribute])-1
            for j, nested_attribute in enumerate(all_nested_attributes[issue_attribute]):
                fields += nested_attribute
                if nested_attribute == 'projectCustomField':
                    fields += '('
                    num_projectCustomField = len(all_nested_attributes['projectCustomField'])-1
                    for k, projectCustomField in enumerate(all_nested_attributes['projectCustomField']):
                        fields += projectCustomField
                        if projectCustomField == 'field':
                            fields += '('
                            num_fiels = len(all_nested_attributes['field'])-1
                            for l, field in enumerate(all_nested_attributes['field']):
                                fields += field
                                if l != num_projectCustomField:
                                    fields += ','
                                else:
                                    fields += ')'

                        if k != num_projectCustomField:
                            fields += ','
                        else:
                            fields += ')'

                if nested_attribute == 'value':
                    fields += '('
                    num_value = len(all_nested_attributes['value'])-1
                    for k, value in enumerate(all_nested_attributes['value']):
                        fields += value
                        if k != num_value:
                            fields += ','
                        else:
                            fields += ')'
                if j != num_nested_attributes:
                    fields += ','
                else:
                    fields += ')'
        if i != num_issue_attributes:
            fields += ',' 

    return fields
  

@app.route('/get_youtrack', methods=['GET'])
def get_youtrack():  
    token = 'perm:ZXJpay5sZXZlbg==.NTgtMQ==.A1FHDuYUtnaJyxDtjXA0xnGDptSp3B'
    headers     = {'Authorization': "Bearer {}".format(token)}
    all_nested_attributes, issue_attributes, nested_attributes = get_issue_attributes()
    fields_query = set_fields_query(all_nested_attributes, issue_attributes, nested_attributes)
    pagination = set_pagination(0, 200)
    query = urlquote('updated: 2019-01-01T12:00 .. Today')
    url = 'https://sesam.myjetbrains.com/youtrack/api/issues?query={}&'.format(query) + fields_query + pagination
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return 'Error code {}'.format(response.status_code)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)