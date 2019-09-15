from django import forms


class RegisterSenderForm(forms.Form):
    email = forms.CharField()
    google_oauth2_client_id = forms.CharField()
    google_oauth2_secrete = forms.CharField()
    recovery_email = forms.CharField()
    phone_number = forms.CharField()
    last_location = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

    def on_register(self):
        pass