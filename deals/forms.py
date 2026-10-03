from django import forms
from .models import Deal
from django.core.exceptions import ValidationError


class CreateDealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['pair', 'deal_type', 'from_price', 'to_price', 'is_followed_rules', 'description', 'img', 'result', 'amount']
        widgets = {
            "pair": forms.Select(attrs={
                'class': 'form-select',
            }),


            "deal_type": forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),

            "from_price": forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'The price at which the trade started...',
            }),

            "to_price": forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'The price at which the trade ended...',
            }),

            'is_followed_rules': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '20',
                'cols': '20',
            }),

            'img': forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'result': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'The Profit or the loss number...',
            })
        }




    def clean_from_price(self):
        from_price = self.cleaned_data.get('from_price')

        if from_price is None:
            raise ValidationError('The `from price` field should not be empty!')

        if from_price <= 0:
            raise ValidationError('The `from price` field should be more than zero!')
        return from_price


    def clean_to_price(self):
        to_price = self.cleaned_data.get('to_price')

        if to_price is None:
            raise ValidationError('The `to price` field should not be empty!')

        if to_price <= 0:
            raise ValidationError('The `to price` field should be more than zero!')
        return to_price


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise ValidationError('The `amount` field should not be empty!')

        if amount < 0:
            raise ValidationError('The `amount` field should be more or equal to zero!')
        return amount


    def clean(self):
        cleaned_data =  super().clean()

        from_price = cleaned_data.get('from_price')
        to_price = cleaned_data.get('to_price')
        result = cleaned_data.get('result')
        deal_type = cleaned_data.get('deal_type')
        amount = cleaned_data.get('amount')

        if from_price is None or to_price is None:
            return cleaned_data

        if deal_type is None or result is None:
            return cleaned_data

        if amount is None:
            return cleaned_data

        if from_price <= to_price and deal_type == "BUY" and result == "LOS":
            raise ValidationError('You lost a `buy` deal, the `from_price` must be higher than the `to_price`')

        if from_price >= to_price and deal_type == "BUY" and result == "PRF":
            raise ValidationError('You won a `buy` deal, the `from_price` must be less than the `to_price`')

        if from_price <= to_price and deal_type == "SELL" and result == "PRF":
            raise ValidationError('You won a `sell` deal, the `from_price` must be higher than the `to_price`')

        if from_price >= to_price and deal_type == "SELL" and result == "LOS":
            raise ValidationError('You lost a `sell` deal, the `from_price` must be less than the `to_price`')

        if result == "EVE":
            if from_price != to_price or amount != 0:
                raise ValidationError('An even deal must have the same `from` and `to` price, and `amount` must be zero!')

        if amount == 0 and result != "EVE":
            raise ValidationError('The `amount` can be zero only when the result is even!')
        

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['pair', 'deal_type', 'from_price', 'to_price', 'is_followed_rules', 'result', 'amount']
        self.fields['deal_type'].choices = [
            choice for choice in self.fields['deal_type'].choices
            if choice[0] != ''
        ]
        self.fields['is_followed_rules'].choices = [
            choice for choice in self.fields['is_followed_rules'].choices
            if choice[0] != ''
        ]
        self.fields['result'].choices = [
            choice for choice in self.fields['result'].choices
            if choice[0] != ''
        ]
        for name, field in self.fields.items():
            if name in required_fields:
                field.required = True
            else:
                field.required = False
            field.label = ''
            field.help_text = ''
