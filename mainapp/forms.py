from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import *

forms.DateInput.input_type = 'date'


class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model = Order
        fields = (
            'first_name', 'last_name', 'middle_name', 'phone', 'address', 'email', 'order_type', 'order_date', 'comment'
        )

    ORDER_TYPE_SELF = 'self-pickup'
    ORDER_TYPE_DELIVERY = 'delivery'

    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_SELF, 'Самовивіз'),
        (ORDER_TYPE_DELIVERY, 'Доставка'),
    )
    
    first_name = forms.CharField(widget=forms.TextInput, max_length=64, required=True)
    last_name = forms.CharField(widget=forms.TextInput, max_length=64, required=True)
    middle_name = forms.CharField(widget=forms.TextInput, max_length=64, required=False)
    phone = PhoneNumberField(required=True)
    address = forms.CharField(widget=forms.TextInput, required=True)
    email = forms.EmailField(widget=forms.EmailInput, max_length=255, required=False)
    order_type = forms.ChoiceField(widget=forms.Select, choices=ORDER_TYPE_CHOICES, required=True)
    order_date = forms.DateField(required=True)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    FORM_CONTROLS = {
        'text': ['first_name', 'last_name', 'middle_name', 'address', ],
        'email': ['email', ],
        'tel': ['phone', ],
        'textarea': ['comment', ],
        'select': ['order_type', ],
        'date': ['order_date', ],
    }
    
    FIELD_PLACEHOLDERS = {
        'first_name': 'Ім\'я',
        'last_name': 'Прізвище',
        'middle_name': 'По-батькові (необов\'язково)',
        'phone': 'Телефон',
        'address': 'Адреса',
        'email': 'Email (необов\'язково)',
        'comment': 'Коментар',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for control_type in self.FORM_CONTROLS:
            field_class = 'form-control' if control_type != 'select' else 'form-select'
            for field_name in self.FORM_CONTROLS[control_type]:
                placeholder = self.FIELD_PLACEHOLDERS.get(field_name)
                field_attributes = dict()
                field_attributes['class'] = field_class
                field_attributes['name'] = field_name
                field_attributes['aria-label'] = field_name.replace('_', '-')
                field_attributes['aria-describedby'] = 'basic-addon-' + field_name.replace('_', '-')
                
                if placeholder is not None:
                    field_attributes['placeholder'] = placeholder
                    
                if control_type == 'textarea':
                    field_attributes['style'] = 'min-height: 200px !important; height: 200px;'
                    
                self.fields[field_name].widget.attrs.update(field_attributes)
    
    