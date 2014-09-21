# web2py-mpd-gmproxy #
A quick and probably dirty [web2py](www.web2py.com/) interface to allow searching [google
music](https://music.google.com) and adding found songs to the current
[MPD](www.musicpd.org) playlist.

Licence : GPLv3 (Ask if other is needed).


## Usage ##

By pointing your web browser to the web2py application (http://localhost:777
with the default configuration of the provided systemd service)/, you get the
following form:

![Request Form](https://bytebucket.org/matclab/web2py-mpd-gmproxy/raw/tip/doc/form.png)

And after submitting a request, you get a result list looking like the
following:

![Results](https://bytebucket.org/matclab/web2py-mpd-gmproxy/raw/tip/doc/results.png)

You then can select the songs you want and add them to the current *mpd*
playlist by clicking on the *submit* button.

## Requirements ##

* a working [MPD](http://www.musicpd.org) installation,
* the [MPC](http://www.musicpd.org/client/mpc) command line client for mpd.

## Setup ##

1. Install the *web2py* framework (downloading the code at
   [web2py](http://www.web2py.com/init/default/download) may be enough).
2. Install *gmusicproxy* as explained on the [web
   site](http://gmusicproxy.net/#setup).
3. `cd web2py/applications`.
4. Clone the *web2py-mpd-gmproxy* application: `hg clone
   https://bitbucket.org/matclab/web2py-mpd-gmproxy gmproxy` or `git clone
   https://github.com/matclab/web2py-mpd-gmproxy.git`.
5. `cp gmproxy/models/conf.py.sample  gmproxy/models/conf.py` and edit `gmproxy/models/conf.py` to match your configuration.
5. Launch *gmusicproxy* (with  `--extended-m3u` option) and *web2py*. You may use the systemd services provided in the `systemd` directory as information on how to do it.

## Thanks ##

A lot of thanks to the authors of the great piece of software used by this
application.

[//]: # ( <script src="doc/jr.js"></script>)
