#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response

from addrinfo.forms import AddrStdForm, CityStateForm, ZipCodeLookupForm
from usps.address_info import Address, USPS

def addr_std(request):
    '''Corrects errors in street addresses, including abbreviations and missing 
    information, and supplies ZIP Codes and ZIP Codes + 4'''
    
    c = {}
    c.update(csrf(request))
    c.update({'addr_active':'active'})
    
    if request.method == 'GET':
        
        return render_to_response('addr_std.html', c)
    elif request.method == 'POST':
        form = AddrStdForm(request.POST)
        if form.is_valid():
            try:
                urbanization = form.cleaned_data['urbanization']
            except KeyError:
                urbanization = None
            addr = Address(form.cleaned_data['firm_name'],
                           form.cleaned_data['address_line1'], 
                           form.cleaned_data['address_line2'], 
                           form.cleaned_data['city'], 
                           form.cleaned_data['state'], 
                           form.cleaned_data['zip5'], 
                           form.cleaned_data['zip4'], 
                           urbanization)
            usps_connector = USPS([addr])
            usps_connector.make_addr_std_request()
            
            c['address'] = addr 
            
            return render_to_response('addr_std_result.html', c)
        else:
            c.update({'form':form})
            return render_to_response('addr_std.html', c)


def zip_code_lookup(request):
    c = {}
    c.update(csrf(request))
    c.update({'zip_code_active':'active'})
    
    if request.method == 'GET':
        return render_to_response('zip_code.html', c)
    elif request.method == 'POST':
        form = ZipCodeLookupForm(request.POST)
        if form.is_valid():
            try:
                urbanization = form.cleaned_data['urbanization']
            except KeyError:
                urbanization = None
            addr = Address(form.cleaned_data['firm_name'],
                           form.cleaned_data['address_line1'], 
                           form.cleaned_data['address_line2'], 
                           form.cleaned_data['city'], 
                           form.cleaned_data['state'], 
                           '', #zip5 
                           '', #zip4
                           urbanization)
            usps_connector = USPS([addr])
            usps_connector.make_zip_code_lookup_request()
            
            c['address'] = addr 
            
            return render_to_response('zip_code_result.html', c)
        else:
            c.update({'form':form})
            return render_to_response('zip_code.html', c)

def city_state_lookup(request):
    c = {}
    c.update(csrf(request))
    c.update({'city_state_active':'active'})
    
    if request.method == 'GET':
        return render_to_response('city_state.html', c)
    elif request.method == 'POST':
        form = CityStateForm(request.POST)
        if form.is_valid():
            addr = Address('',
                           '', 
                           '', 
                           '', 
                           '', 
                           form.cleaned_data['zip5'], #zip5 
                           '', #zip4
                           '')
            usps_connector = USPS([addr])
            usps_connector.make_city_state_lookup_request()
            
            c['address'] = addr 
            
            return render_to_response('city_state_result.html', c)
        else:
            c.update({'form':form})
            return render_to_response('city_state.html', c)
        
        
        
    
