import markdown
import random
import datetime
from markpad import db, app, logger
from sqlalchemy.exc import OperationalError

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n', 'o','p','q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z']
alphabet.append([l.upper() for l in alphabet])

def new_document():
    doc = Document()
    doc.created_on = doc.last_modified_on = datetime.datetime.utcnow()
    doc.url_id = gen_url()
    doc.md_content = ""
    doc.save()
    return doc

def gen_url():
    "Generate a string corresponding to [a-zA-Z]{10}"
    return "".join(
            [random.choice(alphabet) for i in xrange(1,
                app.config.get('DOC_ID_SIZE', 10))])

def get_document(doc_id):
    return Document.query.filter_by(url_id=doc_id).first()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.String, index=True)
    md_content = db.Column(db.String)
    created_on = db.Column(db.DateTime())
    last_modified_on = db.Column(db.DateTime())

    def __repr__(self):
        return '<Document: {0}>'.format(self.url_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        self = None

    def render(self):
        return markdown.markdown(self.md_content,
                extensions=app.config.get('MARKDOWN_EXTS', [
                    'extra',
                    'nl2br',
                    'wikilinks',
                    'headerid',
                    'codehilite',
                    'admonition'
                    ]))

class ValidationError(Exception):
    pass
