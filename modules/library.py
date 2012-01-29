from flask import Flask, render_template
import jsonrpclib

from Maraschino import app
from settings import *
from maraschino.noneditable import *
from maraschino.tools import *

@app.route('/xhr/library')
@requires_auth
def xhr_library():
    return render_library()

@app.route('/xhr/library/<item_type>')
@requires_auth
def xhr_library_root(item_type, expanded=False):
    api_address = server_api_address()

    if not api_address:
        return render_library(message="You need to configure XBMC server settings first.")

    try:
        xbmc = jsonrpclib.Server(api_address)
        library = []
        title = "Movies"

        if item_type == 'movies':
            library = xbmc.VideoLibrary.GetMovies(sort={ 'method': 'label', 'ignorearticle' : True }, properties=['playcount', 'thumbnail', 'fanart'],)

        if item_type == 'shows':
            title = "TV Shows"
            library = xbmc.VideoLibrary.GetTVShows(sort={ 'method': 'label', 'ignorearticle' : True }, properties=['playcount'])

    except:
        return render_library(message="There was a problem connecting to the XBMC server.")

    return render_library(library, title, expanded=expanded)

@app.route('/xhr/library/shows/<int:show>')
@requires_auth
def xhr_library_show(show, expanded=False):
    xbmc = jsonrpclib.Server(server_api_address())
    library = xbmc.VideoLibrary.GetSeasons(tvshowid=show, properties=['tvshowid', 'season', 'showtitle', 'playcount'])
    library['tvshowid'] = show

    title = library['seasons'][0]['showtitle']

    return render_library(library, title)

@app.route('/xhr/library/shows/<int:show>/<int:season>')
@requires_auth
def xhr_library_season(show, season, expanded=False):
    xbmc = jsonrpclib.Server(server_api_address())

    sort = { 'method': 'episode' }
    library = xbmc.VideoLibrary.GetEpisodes(tvshowid=show, season=season, sort=sort, properties=['tvshowid', 'season', 'showtitle', 'episode', 'plot', 'playcount'])

    episode = library['episodes'][0]
    title = '%s - Season %s' % (episode['showtitle'], episode['season'])

    return render_library(library, title)

def render_library(library=None, title="Media Library", message=None, expanded=False):
    if expanded:
        template = 'library_expanded.html'
        vfs_url = '%s/vfs/' % (safe_server_address())

    else:
        template = 'library.html'
        vfs_url = None

    return render_template(template,
        library = library,
        title = title,
        message = message,
        vfs_url = vfs_url,
    )





# expanded libary mode

@app.route('/xhr/library/expanded')
@requires_auth
def xhr_library_expanded():
    return xhr_library_root('movies', expanded=True)
