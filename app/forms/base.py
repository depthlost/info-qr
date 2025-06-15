
from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    class Meta:
        locales = ['es_AR', 'es']

    def __init__(self, model_object=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_object = model_object
