from django import forms

ABOUT_CHOICES = (
    ("IDEA", "A story idea"),
    ("LETTER", "Letter to the editor"),
    ("FEED", "Feedback on our website"),
    ("OTHER", "Other feedback"))


class ContactUsForm(forms.Form):
    first_name = forms.CharField(label='FIRST NAME', max_length=100)
    last_name = forms.CharField(label='LAST NAME', max_length=100)
    email = forms.CharField(label='EMAIL', max_length=100)
    about = forms.ChoiceField(label="I AM WRITING ABOUT", choices=ABOUT_CHOICES)
    #  Todo:  should be rows=10 cols=40
    message = forms.CharField(label="MESSAGE", widget=forms.Textarea)
