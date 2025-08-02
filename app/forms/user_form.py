
from wtforms import StringField, BooleanField , DateField
from wtforms.validators import Optional, Length

from app.forms import BaseForm
from app.forms.fields import OptionalStringField
from app.forms.validations import Birthdate

class UserForm(BaseForm):
    class Meta:
        csrf = False
    
    information_is_public = BooleanField()

    name = StringField(
        validators=[Length(max=64)],
        filters=[lambda input: input.strip() if isinstance(input, str) else input]
    )
    preferred_name = OptionalStringField(validators=[Length(max=64)])
    insurance_number = OptionalStringField(validators=[Length(max=128)])
    birthdate = DateField(format="%Y-%m-%d", validators=[Optional(), Birthdate()])
    address = OptionalStringField(validators=[Length(max=512)])
    phone = OptionalStringField(validators=[Length(max=20)])
    nationality = OptionalStringField(validators=[Length(max=64)])
    
    spoken_language = OptionalStringField(validators=[Length(max=128)])
    communication_method = OptionalStringField(validators=[Length(max=128)])
    needs_communication_assistant = BooleanField()
    needs_continuous_support = BooleanField()

    religion = OptionalStringField(validators=[Length(max=128)])
    spiritual_needs = OptionalStringField(validators=[Length(max=2048)])
    
    allergies = OptionalStringField(validators=[Length(max=2048)])
    medical_procedure_instructions = OptionalStringField(validators=[Length(max=4096)])
    feeding_instructions = OptionalStringField(validators=[Length(max=2048)])
    how_to_take_medication = OptionalStringField(validators=[Length(max=2048)])
    position_for_medication = OptionalStringField(validators=[Length(max=2048)])
    take_medication_with = OptionalStringField(validators=[Length(max=2048)])
    
    has_epilepsy = BooleanField()
    convulsive_crisis_description = OptionalStringField(validators=[Length(max=4096)])
    non_convulsive_crisis_description = OptionalStringField(validators=[Length(max=4096)])
    other_relevant_info = OptionalStringField(validators=[Length(max=4096)])
    
    anxiety_care_instructions = OptionalStringField(validators=[Length(max=4096)])
    pain_detection_cues = OptionalStringField(validators=[Length(max=4096)])
    fear_detection_cues = OptionalStringField(validators=[Length(max=4096)])
    anger_detection_cues = OptionalStringField(validators=[Length(max=4096)])
    communication_instructions = OptionalStringField(validators=[Length(max=4096)])
    mobility = OptionalStringField(validators=[Length(max=4096)])
    personal_care = OptionalStringField(validators=[Length(max=4096)])
    vision_hearing = OptionalStringField(validators=[Length(max=4096)])
    eating_instructions = OptionalStringField(validators=[Length(max=4096)])
    drinking_instructions = OptionalStringField(validators=[Length(max=4096)])
    safety_measures = OptionalStringField(validators=[Length(max=4096)])
    toileting = OptionalStringField(validators=[Length(max=4096)])
    sleep_rest_routine = OptionalStringField(validators=[Length(max=4096)])
    
    likes = OptionalStringField(validators=[Length(max=8192)])
    dislikes = OptionalStringField(validators=[Length(max=8192)])
    notes = OptionalStringField(validators=[Length(max=8192)])
    useful_contacts_and_sites = OptionalStringField(validators=[Length(max=4096)])
