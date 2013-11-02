import json
from base64 import standard_b64encode, standard_b64decode
from flask import flash, stream_with_context, render_template, redirect, Response, request, session, abort, url_for
from werkzeug import secure_filename

from markpad import app, db, models, logger

@app.route('/')
def home():
    "This will render a nice image, with a 'create a new document' button"
    return render_template('home.html')

@app.route('/favicon.<ext>')
def favicon(ext):
    return "", 404

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/new')
def doc_new():
    "Creates a new document, and redirects to his URL"
    doc = models.new_document()
    logger.info("New document '{doc_id}' has been created".format(doc_id=doc.url_id))
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

@app.route('/<doc_id>/upload_file', methods=['GET', 'POST'])
def upload(doc_id):
    if(request.method == 'POST'):
        upload = request.files['file']
        if(upload):
            filename = secure_filename(upload.filename)
            binary_file = models.BinaryDocumentContent()
            binary_file.name = filename
            binary_file.mimetype = upload.mimetype
            if(app.config.get('IS_SQLITE', False)):
                binary_file.data = standard_b64encode(upload.stream.read())
            else:
                binary_file.data = upload.stream.read()
            upload.stream.flush()
            binary_file.document_id = doc_id
            binary_file.save()
            flash("file '{filename}' has successfully uploaded".format(filename=filename), 'info')
        else:
            logger.warning("upload error")
            return "Error 500", 500
    return render_template('file_upload.html', doc_id=doc_id)

        


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
    def generate():
        filename = gen_pdf_file(doc_id)
        with open(filename, 'rb') as f:
            data = f.read()
            yield data
    return Response(stream_with_context(generate()),
            mimetype='application/pdf',
            headers={
                "Content-Disposition": "attachment;filename=%s.pdf" % doc_id
                }
            )

@app.route('/<doc_id>/img/<fname>')
def image(doc_id, fname):
    bin_file = models.BinaryDocumentContent.query.filter_by(document_id=doc_id, name=fname).first()
    if(bin_file is None):
        return "404 Error", 404
    if(app.config.get('IS_SQLITE', False)):
        return Response(stream_with_context(standard_b64decode(bin_file.data)), mimetype=bin_file.mimetype)
    return Response(stream_with_context(bin_file.data), mimetype=bin_file.mimetype)

import subprocess
import tempfile
def gen_pdf_file(doc_id):
    cmd = []
    cmd.append('wkhtmltopdf')
    cmd.append('http://{host_url}/{doc_id}?stylesheet=print'.format(host_url=app.config.get('HOST_URL', 'localhost'), doc_id=doc_id))
    fname = '{tmpdir}/{doc_id}.pdf'.format(tmpdir=tempfile.gettempdir(), doc_id=doc_id)
    cmd.append(fname)
    logger.debug(cmd)
    try:
        subprocess.check_call(cmd)
        logger.info("generated {fname}".format(fname=fname))
    except subprocess.CalledProcessError as error:
        logger.error("Error trying to generate pdf file with command '{cmd}': {error}".format(error=error, cmd=error.cmd))
    return fname

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
