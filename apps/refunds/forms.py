from django import forms

from apps.refunds.models import RefundRequest


class RefundRequestForm(forms.ModelForm):
    order_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = RefundRequest
        exclude = ["user", "status", "iban_verified"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = getattr(user, "first_name", "")
            self.fields["last_name"].initial = getattr(user, "last_name", "")
            self.fields["email"].initial = getattr(user, "email", "")

            if user_profile := getattr(user, "userprofile", None):
                self.fields["phone_number"].initial = getattr(
                    user_profile, "phone_number", ""
                )

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")
        if len(iban) < 14:
            raise forms.ValidationError(
                "IBAN is too short. Check for correctly entered data."
            )
        return iban
