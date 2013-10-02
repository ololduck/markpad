import markdown
import random
import datetime
import json
from markpad import db, app, logger
from sqlalchemy.exc import OperationalError

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n', 'o','p','q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z']
alphabet.append([l.upper() for l in alphabet])

def new_document():
    doc = Document()
    doc.created_on = doc.last_modified_on = datetime.datetime.utcnow()
    doc.url_id = gen_random_str(app.config.get('URL_ID_LEN', 10))
    doc.md_content = ""
    doc.save()
    return doc

def gen_random_str(nbr_chars=10):
    "Generate a string corresponding to [a-zA-Z]{10}"
    return "".join(
            [random.choice(alphabet) for i in xrange(1,
                nbr_chars)])

def get_document(doc_id):
    return Document.query.filter_by(url_id=doc_id).first()

def apply_microcommit(doc, mc):
    logger.info(json.dumps(mc, indent=4))
    d = doc.md_content.splitlines()
    print(d)
    start_pos = {'col': mc['range']['start']['column'], 'row': mc['range']['start']['row']}
    end_pos = {'col': mc['range']['end']['column'], 'row': mc['range']['end']['row']}
    if(mc['action'] == 'insertText'):
        try:
            d[start_pos['row']] = d[start_pos['row']][:start_pos['col']] + mc["text"] + d[end_pos['row']][end_pos['col']-len(mc["text"]):]
        except IndexError:
            d.append(mc["text"])
        logger.info("start_pos: {0}, end_pos: {1}".format(start_pos, end_pos))
    elif(mc['action'] == 'removeText'):
        d[start_pos['row']] = d[start_pos['row']][:start_pos['col']] + d[start_pos['row']][start_pos['col']:end_pos['col']].replace(mc['text'], "") + d[end_pos['row']][end_pos['col']:]
    elif(mc['action'] == 'insertLines'):
        d = d[:start_pos['row']] + mc['lines'] + d[end_pos['row']:]
    elif(mc['action'] == 'removeLines'):
        del d[start_pos['row']:end_pos['row']]
    else:
        logger.info("'action' is not recognized: {0}".format(mc['action']))
    doc.md_content = "\n".join(d)

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

    def update(self, micro_commit):
        apply_microcommit(self, micro_commit)
        self.save()


class ValidationError(Exception):
    pass
