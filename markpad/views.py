import json
from flask import render_template, redirect, request, session, abort, url_for

from markpad import app, models, logger

@app.route('/')
def home():
    "This will render a nice image, with a 'create a new document' button"
    return render_template('home.html')

@app.route('/new')
def doc_new():
    "Creates a new document, and redirects to his URL"
    doc = models.new_document()
    return redirect(url_for("doc_edit", doc_id=doc.url_id))

@app.route('/<doc_id>/edit')
def doc_edit(doc_id):
    "Main page to edit a document"
    doc = models.get_document(doc_id)
    return render_template('doc.edit.html', doc=doc)

@app.route('/<doc_id>')
def doc_view(doc_id):
    """
    View a document. This renders a "definitive" HTML version of the
    document, and offers the possibility to download it, in pdf form,
    or maybe others.
    """
    doc = models.get_document(doc_id)
    return render_template('doc.view.html', rendered_md=doc.render())

@app.route('/<doc_id>/dl/pdf')
def download(doc_id):
    pass

@app.route('/<doc_id>/update', methods=['POST'])
def doc_update(doc_id):
    "JSON endpoint for document updates. I still have to define protocol."
    assert(request.method == 'POST')
    doc = models.get_document(doc_id)
    assert(request.json.get('data', None) is not None)
    try:
        doc.update(request.json['data'])
    except KeyError as e:
        logger.warn(
                "could not access key 'data' in request {request}: {error}".format(
                    request=request, error=e))
    return json.dumps({"render":doc.render()})
