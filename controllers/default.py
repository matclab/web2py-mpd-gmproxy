# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

print db.__dict__
gmproxyserver = 'localhost:9999'
import httplib

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def result():
    if not len(request.args):
        db.m3u.truncate()
        reqstring = '/get_by_search?type=album&artist=Queen&title=Greatest%20Hits'
        conn = httplib.HTTPConnection(gmproxyserver)
        conn.request("GET", reqstring)
        r1 = conn.getresponse()
        print r1.status, r1.reason
        if r1.status == 200:
            res = r1.read().split('\n')[1:]
            for i in range(0, len(res)-1, 2):
                #print res[i]
                extinf = res[i].split(',', 1)[1]
                url = res[i+1]
                db.m3u.insert(url=url, extinf=extinf)
        conn.close()
        grid = SQLFORM.grid(db.m3u, editable=False, details=False,
                maxtextlength=120,
                 selectable = lambda ids : redirect(URL('default', 'selected',
                     vars=dict(ids=ids))))
        # Add select / unselect button
        heading=grid.elements('th')
        if heading:
            heading[0].append(INPUT(_type='checkbox',
            _onclick="""if (this.checked) {
                jQuery('input[type=checkbox]').each(function(k){jQuery(this).prop('checked', true);});
                } else {
                jQuery('input[type=checkbox]').each(function(k){jQuery(this).prop('checked', false);});
                }
                """))
#"checkboxes = document.getElementsByName('records');for each(var checkbox in checkboxes)checkbox.checked = this.checked;"))
    else:
        grid = SQLFORM.grid(db.m3u)
    return dict(grid=grid)
    #return dict(message=res)

def selected():
    
    selected_ids = request.vars.ids
    rows = db(db.m3u.id.belongs(selected_ids)).select()
    res = ['#EXTM3U']
    for r in rows:
        res.append("#EXTINF:%s,%s" % (r.id, r.extinf))
        res.append(r.url)
    res="\n".join(res)
    return res


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
