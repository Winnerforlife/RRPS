from django import forms

from apps.refunds.models import RefundRequest


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        exclude = ["user", "status", "iban_verified"]
    
    def clean_iban(self):
        iban = self.cleaned_data.get('iban')
        if len(iban) < 34:
            raise forms.ValidationError("IBAN is too short. Check for correctly entered data.")
        return iban
