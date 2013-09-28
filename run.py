#!/usr/bin/env python
from markpad import app, init_db 

init_db()
app.run(debug=True)
