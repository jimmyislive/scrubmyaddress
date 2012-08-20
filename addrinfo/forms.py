#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class AddrStdForm(forms.Form):
    firm_name = forms.CharField(max_length=38, required=False)
    address_line1 = forms.CharField(max_length=38, required=False)
    address_line2 = forms.CharField(max_length=38)
    city = forms.CharField(max_length=15, required=False)
    state = forms.CharField(max_length=2, required=False)
    urbanization = forms.CharField(max_length=28, required=False)
    #00501 is the lowest US zipcode
    zip5 = forms.IntegerField(min_value=500, max_value=99999, required=False)
    zip4 = forms.IntegerField(min_value=0, max_value=9999, required=False)
    usps_check = forms.BooleanField()
    
    def clean(self):
        cleaned_data = super(AddrStdForm, self).clean()
        #Either <City> and <State> or <Zip5> are required.
        if not ((cleaned_data.get('city') and cleaned_data.get('state')) or cleaned_data.get('zip5')):
            raise forms.ValidationError('Either City and State or Zip5 are required.')
        
        return cleaned_data
    
class ZipCodeLookupForm(forms.Form):
    firm_name = forms.CharField(max_length=38, required=False)
    address_line1 = forms.CharField(max_length=38, required=False)
    address_line2 = forms.CharField(max_length=38)
    city = forms.CharField(max_length=15)
    state = forms.CharField(max_length=2)
    urbanization = forms.CharField(max_length=28, required=False)
    usps_check = forms.BooleanField()
    
class CityStateForm(forms.Form):
    #00501 is the lowest US zipcode
    zip5 = forms.IntegerField(min_value=500, max_value=99999)

    
    
    
    
    