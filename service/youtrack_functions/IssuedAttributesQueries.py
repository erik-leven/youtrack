def set_pagination(skip, top):
    return '&$skip={}&$top={}'.format(skip, top)

def get_issue_attributes():
    issue_attributes        = ['idReadable', 'created', 'updated', 'resolved', 'numberInProject', 'project', 'summary', 'description','usesMarkdown','wikifiedDescription','reporter','updater','draftOwner','isDraft','visibility','votes','comments','commentsCount','tags','externalIssue','customFields','voters','watchers','attachments','subtasks','parent']
    nested_attributes       = ['project','reporter','updater','draftOwner','comments','tags','externalIssue','customFields','voters','watchers','attachments','subtasks','parent','projectCustomField','value'] 

    project_keys            = ['shortName','description','archived','fromEmail','replyToEmail','template','iconUrl','name', 'id','Priority','Stage']
    reporter_keys           = ['login','fullName','email','jabberAccountName','ringId','guest','avatarUrl']
    updater_keys            = reporter_keys
    draftOwner_keys         = reporter_keys
    comment_keys            = ['text','usesMarkdown','textPreview','created','updated']
    tags_keys               = ['name']
    externalIssue_keys      = ['name','url','key']
    customFields_keys       = ['name', 'id', 'projectCustomField(id,field(id,name)),value(avatarUrl,buildLink,color(id),fullName,id,isResolved,localizedName,login,minutes,name,presentation,text)']
    voters_keys             = ['hasVote']
    watcher_keys            = ['hasStar']
    attachments_keys        = ['name', 'created','updated','size','extension','charset','mimeType','metaData','draft','removed','base64Content','url','thumbnailURL']
    subtasks_keys           = ['direction']
    parent_keys             = subtasks_keys

    all_nested_attributes = {'project':project_keys,'reporter':reporter_keys,'updater':updater_keys,'draftOwner':draftOwner_keys,'comments':comment_keys,'tags':tags_keys,'externalIssue':externalIssue_keys,'customFields':customFields_keys,'voters':voters_keys,'watchers':watcher_keys,'attachments':attachments_keys,'subtasks':subtasks_keys,'parent':parent_keys}

    return all_nested_attributes, issue_attributes, nested_attributes

def get_agile_attributes():
    agile_attributes = ['name','owner','visibleFor','visibleForProjectBased','updateableBy','updateableByProjectBased','orphansAtTheTop','hideOrphansSwimlane','estimationField','projects(name)','sprints','currentSprint','columnSettings','swimlaneSettings','sprintsSettings','colorCodingstatus']

def diff(A, B):
  B = set(B)
  return [item for item in A if item not in B] 

def get_user_attributes():
    user_attributes = ['login','fullName','email','roleUrl','ringId','guest','online','banned','tags','savedQueries','avatarUrl','profiles']
    return user_attributes

def get_user_fields_query(user_attributes):
    fields = 'fields='
    num_user_attributes = len(user_attributes)
    for i, attribute in enumerate(user_attributes):
        fields += attribute
        if i != num_user_attributes-1:
            fields += ','
        else:
            return fields

def make_issues_fields_query_old(all_nested_attributes, issue_attributes, nested_attributes):
    all_nested_attributes = str(all_nested_attributes)
    all_nested_attributes = all_nested_attributes.replace("[", "(")
    all_nested_attributes = all_nested_attributes.replace("]", ")")
    all_nested_attributes = all_nested_attributes.replace(" ", "")
    all_nested_attributes = all_nested_attributes.replace("'", "")
    all_nested_attributes = all_nested_attributes.replace(":", "")
    all_nested_attributes = all_nested_attributes.replace("{", "")
    all_nested_attributes = all_nested_attributes.replace("}", "")

    not_nested_attributes = ",".join(diff(issue_attributes,nested_attributes))
    not_nested_attributes = str(not_nested_attributes)

    return 'fields=' + all_nested_attributes + ',' + not_nested_attributes


def get_projects_fields_query(all_nested_attributes):
    project_attributes = all_nested_attributes['project']
    fields = 'fields='
    num_project_attributes = len(project_attributes)
    for i, attribute in enumerate(project_attributes):
        fields += attribute
        if i != num_project_attributes-1:
            fields += ','
        else:
            return fields

def get_issue_template():
    issue_template = {
    "description": "", 
    "summary": "",
    "project": {
      'id': ""
    },
    'idReadable':""
    }
    return issue_template


def remove_sesam_system_attributes(entities):
    for entity in entities:
        remove_attributes = []
        for key, value in entity.items():
            if key[0] == '_':
                remove_attributes.append(key)
        for attribute in remove_attributes:
            del entity[attribute]
    return entities

def create_new_issue(sesam_entities):
    # Assuming the entities from sesam have names like 'dataset-name:sesam-<property-name>'
    print(sesam_entities)
    issues = []
    for sesam_entity in sesam_entities:
        issue_template = get_issue_template()
        for key, value in sesam_entity.items():
            if key[0] == "_":
                if key == "_id":
                    issue_template['project']['id'] = value.split(':')[-1]
                else:
                    pass
            else:
                # remove 'dataset-name' from property
                key = key.split(":")[-1]
                # remove 'sesam' from property
                key = key.split('-')[-1]
                if key in issue_template.keys():
                    issue_template[key] = value
        issues.append(issue_template)
    #{"project":{"id":"0-4"}, "summary":"REST API lets you create issues!","description":"Let'\''s create a new issue using YouTrack'\''s REST API."}
    """
    issue_template = {
    "project":{"id":"0-0"},
    "summary":"REST API lets you create issues!",
    "description":"Let'\''s create a new issue using YouTrack'\''s REST API."
    }
    """
    return issues



def test_update():
    data = {
    "attachments": [], 
    "comments": [{'text':'this is the second update comment'}], 
    "commentsCount": 0, 
    "created": 1568722688398,  
    "description": "Let'''s create a new issue using YouTrack'''s REST API.", 
    "draftOwner": "", 
    "externalIssue": "", 
    "idReadable": "TEST-13", 
    "isDraft": ""
  }
    return data

def raw_data():
    raw_data =  [{
    "$type": "Issue", 
    "attachments": [], 
    "comments": [
      {
        "$type": "IssueComment", 
        "created": 1568725990755, 
        "deleted": false, 
        "text": "this is the first update comment", 
        "textPreview": "<div class=\"wiki text prewrapped\">this is the first update comment</div>\n", 
        "updated": null, 
        "usesMarkdown": false
      }, 
      {
        "$type": "IssueComment", 
        "created": 1568726285827, 
        "deleted": false, 
        "text": "this is the first update comment", 
        "textPreview": "<div class=\"wiki text prewrapped\">this is the first update comment</div>\n", 
        "updated": null, 
        "usesMarkdown": false
      }, 
      {
        "$type": "IssueComment", 
        "created": 1568726349380, 
        "deleted": false, 
        "text": "this is the first update comment", 
        "textPreview": "<div class=\"wiki text prewrapped\">this is the first update comment</div>\n", 
        "updated": null, 
        "usesMarkdown": false
      }
    ], 
    "commentsCount": 3, 
    "created": 1568722688398, 
    "customFields": [
      {
        "$type": "SingleEnumIssueCustomField", 
        "id": "102-110", 
        "projectCustomField": {
          "$type": "EnumProjectCustomField", 
          "field": {
            "$type": "CustomField", 
            "id": "75-1", 
            "name": "Priority"
          }, 
          "id": "102-110"
        }, 
        "value": {
          "$type": "EnumBundleElement", 
          "color": {
            "$type": "FieldStyle", 
            "id": "17"
          }, 
          "id": "81-3", 
          "localizedName": null, 
          "name": "Normal"
        }
      }, 
      {
        "$type": "SingleUserIssueCustomField", 
        "id": "104-28", 
        "projectCustomField": {
          "$type": "UserProjectCustomField", 
          "field": {
            "$type": "CustomField", 
            "id": "75-4", 
            "name": "Assignee"
          }, 
          "id": "104-28"
        }, 
        "value": null
      }, 
      {
        "$type": "StateIssueCustomField", 
        "id": "102-109", 
        "projectCustomField": {
          "$type": "StateProjectCustomField", 
          "field": {
            "$type": "CustomField", 
            "id": "75-112", 
            "name": "Stage"
          }, 
          "id": "102-109"
        }, 
        "value": {
          "$type": "StateBundleElement", 
          "color": {
            "$type": "FieldStyle", 
            "id": "0"
          }, 
          "id": "83-60", 
          "isResolved": false, 
          "localizedName": null, 
          "name": "Backlog"
        }
      }, 
      {
        "$type": "SingleEnumIssueCustomField", 
        "id": "102-108", 
        "projectCustomField": {
          "$type": "EnumProjectCustomField", 
          "field": {
            "$type": "CustomField", 
            "id": "75-48", 
            "name": "Kanban State"
          }, 
          "id": "102-108"
        }, 
        "value": {
          "$type": "EnumBundleElement", 
          "color": {
            "$type": "FieldStyle", 
            "id": "16"
          }, 
          "id": "81-252", 
          "localizedName": null, 
          "name": "Ready to pull"
        }
      }
    ], 
    "description": "Let'''s create a new issue using YouTrack'''s REST API.", 
    "draftOwner": null, 
    "externalIssue": null, 
    "idReadable": "TEST-13", 
    "isDraft": false, 
    "links": [
      {
        "$type": "IssueLink", 
        "direction": "BOTH"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "OUTWARD"
      }, 
      {
        "$type": "IssueLink", 
        "direction": "INWARD"
      }
    ], 
    "numberInProject": 13, 
    "parent": {
      "$type": "IssueLink", 
      "direction": "INWARD"
    }, 
    "project": {
      "$type": "Project", 
      "description": null, 
      "iconUrl": "/hub/api/rest/projects/1c2717b6-b9bc-4fce-956b-220b8c45db4c/icon?etag=MjYtNzg%3D", 
      "id": "0-4", 
      "name": "test", 
      "shortName": "TEST"
    }, 
    "reporter": {
      "$type": "User", 
      "avatarUrl": "/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48", 
      "email": "youtrack-admin@sesam.in", 
      "fullName": "Sesam", 
      "guest": false, 
      "jabberAccountName": null, 
      "login": "Sesam", 
      "ringId": "68698611-80a9-486e-aebb-aee1d5601fdf"
    }, 
    "resolved": null, 
    "subtasks": {
      "$type": "IssueLink", 
      "direction": "OUTWARD"
    }, 
    "summary": "this is updated too", 
    "tags": [], 
    "updated": 1568726349379, 
    "updater": {
      "$type": "User", 
      "avatarUrl": "/hub/api/rest/avatar/68698611-80a9-486e-aebb-aee1d5601fdf?s=48", 
      "email": "youtrack-admin@sesam.in", 
      "fullName": "Sesam", 
      "guest": false, 
      "jabberAccountName": null, 
      "login": "Sesam", 
      "ringId": "68698611-80a9-486e-aebb-aee1d5601fdf"
    }, 
    "usesMarkdown": false, 
    "visibility": {
      "$type": "UnlimitedVisibility"
    }, 
    "voters": {
      "$type": "IssueVoters", 
      "hasVote": false
    }, 
    "votes": 0, 
    "watchers": {
      "$type": "IssueWatchers", 
      "hasStar": false
    }, 
    "wikifiedDescription": "<div class=\"wiki text prewrapped\">Let<strong>s create a new issue using YouTrack</strong>s REST API.</div>\n"
  }]
    return raw_data