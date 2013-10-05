import json
from flask import flash, render_template, redirect, request, session, abort, url_for

from markpad import app, models, logger

@app.route('/')
def home():
    "This will render a nice image, with a 'create a new document' button"
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/new')
def doc_new():
    "Creates a new document, and redirects to his URL"
    doc = models.new_document()
    logger.info("New document {doc_id} has been created".format(doc_id=doc.url_id))
    return redirect(url_for("doc_edit", doc_id=doc.url_id))

@app.route('/<doc_id>/edit')
def doc_edit(doc_id):
    "Main page to edit a document"
    if(doc_id not in app.deltas):
        app.deltas[doc_id] = []

    if('client_id' not in session):
        session['client_id'] = models.gen_random_str(32)
        app.client_states.update({
            session['client_id']: {
                doc_id: len(app.deltas[doc_id]) - 1
            }
        })
    if(session['client_id'] not in app.client_states):
        app.client_states.update({session['client_id']:{}})
    if(doc_id not in app.client_states[session['client_id']]):
        app.client_states[session['client_id']][doc_id] = len(app.deltas[doc_id])
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
    doc = models.get_document(doc_id)
    if('client_id' not in session):
        flash("an error occured. Please contact <contact@paullollivier.fr>, with all the information you can provide. Please do not forget to include the exact time at which this occured.")
        logger.error("on /update, we don't have any client_id information. document: {doc_id}".format(doc_id=doc_id))
        return abort()
    deltas_to_send = app.deltas[doc_id][
        app.client_states[session['client_id']][doc_id]:
    ]
    app.client_states[session['client_id']][doc_id] = len(app.deltas[doc_id])   
    if(request.json):
        doc.update(request.json['data'])

    return json.dumps({
            "events": deltas_to_send,
            "render":doc.render()
            })
