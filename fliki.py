from glob import glob
from os.path import dirname, basename, exists, splitext, join
from time import time
import re

import git
from creole import creole2html
from flask import Flask, request, render_template, redirect, url_for


INDEX_PAGE = "home"
PAGES_DIRECTORY = "pages"

RE_PAGE_NAME = re.compile("^[_a-zA-Z0-9\-]+$")

GITREPOPATH=dirname(__file__)
PAGEPATH='%s/%s' % (GITREPOPATH, PAGES_DIRECTORY)

app = Flask(__name__)
repo = git.Repo(GITREPOPATH)

@app.route("/")
def page_show_index():
    """Show the home page.
    This view just calls the page_show() function with the home page."""
    return page_show(INDEX_PAGE)
    
@app.route("/<page_name>")
def page_show(page_name):
    """Show the page."""
    if _page_exists(page_name):
        text = _read_page(page_name)
        html = _convert_to_html(text)
        return render_template("page_show.html", content=html, page_name=page_name, title=humanize(page_name).title())
    else:
        return redirect("/%s/edit" % page_name)

@app.route("/<page_name>/edit", methods=["GET", "POST"])
def page_edit(page_name):
    """Edit the page."""
    if request.method == "GET":
        if _page_exists(page_name):
            text = _read_page(page_name)
        else:
            text = "= %s\n\nThis page does not exist yet. Replace this content and click Save to create it.\n\nThis wiki uses [[http://en.wikipedia.org/wiki/Creole_(markup)|creole]] dialect. There is a local cheatsheet available [[../static/html/creole_cheat_sheet.html|here]]." % humanize(page_name).title()
        return render_template("page_edit.html", text=text, page_name=page_name, title=humanize(page_name).title(), fname=_page_name_to_filename(page_name))
    else:
        text = request.form["text"]
        _write_page(page_name, text)
        return redirect("/%s" % page_name)
        
@app.route("/all-pages")
def page_list():
    """List all pages in the system."""
    pages = _list_pages()
    return render_template("page_list.html", pages=pages)

@app.route("/fragment", methods=["POST"])
def fragment():
  """Render a fragment of creole."""
  text = request.form["fragment"]
  return _convert_to_html(text)

def _page_name_to_filename(page_name):
    if RE_PAGE_NAME.match(page_name):
        return join(PAGES_DIRECTORY, "%s.creole" % page_name.lower())
    else:
        raise ValueError("Invalid page name %s." % page_name)

@app.template_filter()
def humanize(page_name):
    """Clean up the page name to a human-readable name."""
    return page_name.replace("-", " ").capitalize()
    
def _filename_to_page_name(fname):
    return splitext(basename(fname))[0]

def _page_exists(page_name):
    return exists(_page_name_to_filename(page_name))

def _read_page(page_name):
    fname = _page_name_to_filename(page_name)
    return open(fname).read()

def _write_page(page_name, text):
    fname = _page_name_to_filename(page_name)
    open(fname, "w").write(text)
    repo.index.add([fname])
    repo.index.commit("edited %s" % page_name)
    
def _list_pages():
    pages_glob = join(PAGES_DIRECTORY, "*.creole")
    return [_filename_to_page_name(fname) for fname in sorted(glob(pages_glob))]

def _convert_to_html(text):
    return creole2html(unicode(text))

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=8091)
