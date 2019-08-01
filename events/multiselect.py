from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms


def widget(model_reference, field, title, titlew):
    class WidgetForm(forms.ModelForm):
        fileds = forms.ModelMultipleChoiceField(
            queryset=model_reference.objects.all(),
            label=(title),
            widget=FilteredSelectMultiple((titlew), False,)
        )
        class Media:
            css = {
                'all':('/media/css/widgets.css',),
            }
            # jsi18n is required by the widget
            js = ('/admin/jsi18n/',)
     
        class Meta:
            model = model_reference
            
    return WidgetForm
