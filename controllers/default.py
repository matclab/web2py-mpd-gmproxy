# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

gmproxyserver = 'localhost:9999'
M3UNAME = '_tmp.m3u'
M3UPATH = '/home/music/'
m3u = '%s%s' % (M3UPATH, M3UNAME)
import httplib, urllib
import subprocess

T.set_current_languages('en', 'en-en')

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    form = SQLFORM.factory(
            Field('search',
                requires=IS_IN_SET({'get_by_search':T('Standard'),
                    'get_new_station_by_search':T('Radio')}, zero=None),
                label=T('Radio or Standard'), default='get_by_search'),
        Field('searchtype', requires=IS_IN_SET({'artist':T('Artist'),
                'album': T('Album')}, zero=None), 
                label=T('Search type'), default='artist'),
        Field('title', 'string', label=T('Title')),
        Field('artist', 'string', label=T('Artist')),
        Field('num_tracks', 'integer', label=T('Number of results'),
            default=60),
        Field('exact', 'boolean', label=T('Exact search')),
        )
    if form.process().accepted:
        response.flash = T('form accepted')
        session.search = form.vars.search
        session.searchtype = form.vars.searchtype
        session.title = form.vars.title
        session.artist = form.vars.artist
        session.exact = form.vars.exact
        session.num_tracks = form.vars.num_tracks
        redirect(URL('default', 'result'))
    elif form.errors:
        response.flash = T('form has errors')
    return dict(form=form)

def result():
    if not len(request.args):
        db.m3u.truncate()
        args = []
        args.append(('type', session.searchtype))
        if session.artist:
            args.append(('artist', session.artist))
        if session.title:
            args.append(('title', session.title))
        if session.num_tracks:
            args.append(('num_tracks', session.num_tracks))


        reqstring = '/%s?%s' % (session.search, urllib.urlencode(args))
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
                maxtextlength=120, paginate=2000,
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
    with open(m3u, 'w') as f:
        f.write(res)
    rcode = subprocess.call(['/usr/bin/mpc', 'load', M3UNAME])
    if not rcode:
        session.flash = T('Songs append to queue')
    else:
        session.flash = T('Fail to append songs to queue')
    redirect(URL('default', 'index'))


