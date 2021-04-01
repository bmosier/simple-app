from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import os
import vtmodel

class Submissions(MethodView):
    def get(self):
        # headers = { 'x-apikey': os.environ.get('VTKEY') }
        model = vtmodel.get_model()

        vtsubs = [dict(
            analysis_id = row[0],
            file_name = row[1], 
            timestamp = row[2]
            ) for row in model.select()]

        return render_template('submissions.html', vtsubs=vtsubs)
