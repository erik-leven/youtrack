def all_nested_fields():

    # field types
    project = ['shortName','description','leader','archived','fromEmail','replyToEmail','template','iconUrl','name', 'id','Priority','Stage']
    user = ['id','login','fullName','email','jabberAccountName','ringId','guest','online','banned','tags(name,untagOnResolve)','savedQueries','avatarUrl','profiles']
    array_of_issuecomments = ['text','usesMarkdown','textPreview','created','updated','author(id,fullName)','attachments(name,created,updated,size,extension,charset,mimeType,metaData,draft,removed,base64Content,url,thumbnailURL)'] 
    array_of_issuecustomfields = ['name', 'id', 'projectCustomField(id,field(id,name)),value(avatarUrl,buildLink,color(id),fullName,id,isResolved,localizedName,login,minutes,name,presentation,text)']
    issuevoters = ['hasVote','original(id,fullName)','duplicate(issue(idReadable),user(id,fullName))']
    issuewatchers = ['hasStar','issueWatchers(user(id,fullName),issue(idReadable),isStarred),duplicateWatchers(user(id,fullName),issue(idReadable),isStarred)']
    array_of_issueattachments = ['name','author(id,fullName)','created','updated','size','extension','charset','mimeType','metaData','draft','removed','base64Content','url','issue(idReadable)','comment(name)','thumbnailURL']
    issuelink = ['direction','linkType(uid,name,localizedName,sourceToTarget,localizedSourceToTarget,targetToSource,localizedTargetToSource,directed,aggregation,readOnly),issues(idReadable),trimmedIssues(idReadable),id']
    externalissue = ['name','url','key']
    return {'Project':project, 'User':user, 'ArrayofIssueComments':array_of_issuecomments, 'ArrayofIssueCustomFields':array_of_issuecustomfields, 'IssueVoters':issuevoters, 'IssueWatchers':issuewatchers, 'ArrayofIssueAttachments':array_of_issueattachments, 'ArrayofIssueLinks':issuelink, 'ExternalIssue':externalissue}


def all_issue_fields():
    return ['idReadable', 'created', 'updated', 'resolved', 'numberInProject', 'project', 'summary', 'description','usesMarkdown','wikifiedDescription',
    'reporter','updater','draftOwner','isDraft','visibility','votes','comments','commentsCount','externalIssue','customFields','voters','watchers',
    'attachments','subtasks','parent','links']

def all_field_types():
    return {'idReadable':'Long', 'created':'Long', 'updated':'Long','resolved':'Long','numberInProject':'Long','project':'Project', 'summary':'String',
    'description':'String','usesMarkdown':'Boolean','wikifiedDescription':'String','reporter':'User','updater':'User','draftOwner':'User',
    'isDraft':'Boolean','visibility':'Visibility','votes':'Int','comments':'ArrayofIssueComments','commentsCount':'Long','links':'ArrayofIssueLinks',
    'externalIssue':' ExternalIssue','customFields':'ArrayofIssueCustomFields','voters':' IssueVoters','watchers':'IssueWatchers',
    'attachments':'ArrayofIssueAttachments','subtasks':'ArrayofIssueLinks','parent':'ArrayofIssueLinks'}


def make_issues_fields_query():
    nested_fields = all_nested_fields()
    issue_fields = all_issue_fields()
    field_types = all_field_types()

    query = 'fields='
    nested_keys = nested_fields.keys()

    for i, field in enumerate(issue_fields):
        query += field
        if field_types[field] in nested_keys:
            query += '(' + ",".join(nested_fields[field_types[field]]) + ')'
        if i != len(issue_fields) - 1:
            query += ','
    return query

def make_projects_fields_query():
    nested_fields = all_nested_fields()
    query = 'fields=' + ",".join(nested_fields['Project'])
    
    return query

def make_projects_fields_query_customfields():
    return 'fields=field(aliases,isAutoAttached,isUpdateable,name,id),canBeEmpty,isPublic,id'
    
def make_users_fields_query():
    nested_fields = all_nested_fields()
    query = 'fields=' + ",".join(nested_fields['User'])
    return query



#fields=project(shortName,description,archived,fromEmail,replyToEmail,template,iconUrl,name,id,Priority,Stage)

#fields=project(shortName,description,archived,fromEmail,replyToEmail,template,iconUrl,name,id,Priority,Stage),reporter(login,fullName,email,jabberAccountName,ringId,guest,avatarUrl),updater(login,fullName,email,jabberAccountName,ringId,guest,avatarUrl),draftOwner(login,fullName,email,jabberAccountName,ringId,guest,avatarUrl),comments(text,usesMarkdown,textPreview,created,updated),tags(name),externalIssue(name,url,key),customFields(name,id,projectCustomField(id,field(id,name)),value(avatarUrl,buildLink,color(id),fullName,id,isResolved,localizedName,login,minutes,name,presentation,text)),voters(hasVote),watchers(hasStar),attachments(name,created,updated,size,extension,charset,mimeType,metaData,draft,removed,base64Content,url,thumbnailURL),subtasks(direction),parent(direction),idReadable,created,updated,resolved,numberInProject,summary,description,usesMarkdown,wikifiedDescription,isDraft,visibility,votes,commentsCount