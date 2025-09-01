import json
import secrets
import string
import time
from django.http import HttpResponse,JsonResponse,HttpResponseForbidden
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
from .tokens import email_verification_token
from django.contrib.auth import get_backends
from django.utils.html import strip_tags
# from django.core.mail.backends.smtp import SMTPException
from smtplib import SMTPException

# from datetime import datetime,date,timedelta

from django.shortcuts import render,redirect,get_object_or_404
from django.middleware.csrf import REASON_NO_CSRF_COOKIE

from zqUsers.models import *
from wallet.models import *
from zqapp.forms import *
from zqUsers.forms import UserForm
from zqapp.models import *
import requests
from django.db.models import Sum
import base64
from django.http import JsonResponse
import random
import string
from datetime import datetime,timedelta
from django.core.mail import EmailMessage,get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, connection




import os
import re
import logging
logger = logging.getLogger("django")


def custom_csrf_failure_view(request, reason=""):
    # Check the reason for failure and log it if necessary
    if reason == REASON_NO_CSRF_COOKIE:
        # Handle the specific case where there is no CSRF cookie
        pass

    # Redirect to the previous page if available, otherwise to the home page
    messages.warning(request,"Please fill all details carefully ")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def testitout(request):
    
    current_time = timezone.now()
    curr=datetime.now()
    return HttpResponse(f'<h1>Time is</h1><p>{current_time}</p><p>{curr}</p>')


def index(request):
    logger.debug("Test log entry")


    
    try:
        registered_user = request.get_signed_cookie('registered_user', salt='registration_salt')
        
    except Exception as e:
        registered_user=None
        print(str(e))
    
    if registered_user:
        # If the signed cookie is found, redirect to login page
        return redirect('login')
    
    referralId=request.GET.get('referralid')
    print(referralId)
    



    return render(request,'cointex/index.html', context={})


def boarding(request):
    logger.info("This is an INFO log entry")  # Should appear in `info.log`
  
    try:
        registered_user = request.get_signed_cookie('registered_user', salt='registration_salt')
        
    except Exception as e:
        registered_user=None
        print(str(e))
    
    if registered_user:
        # If the signed cookie is found, redirect to login page
        return redirect('login')
    return render(request,'cointex/boarding.html', context={})

def boarding2(request):
    
    logger.error("This is an ERROR log entry")  # Should appear in `error.log`
    try:
        registered_user = request.get_signed_cookie('registered_user', salt='registration_salt')
        
    except Exception as e:
        registered_user=None
        print(str(e))
    # registered_user = request.get_signed_cookie('registered_user', salt='registration_salt')
    
    if registered_user:
        # If the signed cookie is found, redirect to login page
        return redirect('login')
    return render(request,'cointex/boarding2.html', context={})

def about(request):
    return render(request,'zqapp/about.html')

def token(request):
    return render(request,'zqapp/token.html')

def termsCondition(request):
    return render(request,'zqapp/termsCondition.html')

# def 
def roadmap(request):
    return render(request,'zqapp/roadmap.html')

def mining(request):
    return render(request,'zqapp/mining.html')

def forgetpass(request):
    return render(request,'cointex/boarding2.html')

def success(request):
    return render(request,'zqapp/success.html')    

def register(request):
    


    currencies = [
        "Afghan Afghani (AFN)", "Albanian Lek (ALL)", "Algerian Dinar (DZD)", "Angolan Kwanza (AOA)", "Argentine Peso (ARS)",
        "Armenian Dram (AMD)", "Aruban Florin (AWG)", "Australian Dollar (AUD)", "Azerbaijani Manat (AZN)", "Bahamian Dollar (BSD)",
        "Bahraini Dinar (BHD)", "Bangladeshi Taka (BDT)", "Barbadian Dollar (BBD)", "Belarusian Ruble (BYN)", "Belgian Franc (BEF)",
        "Belize Dollar (BZD)", "Bermudian Dollar (BMD)", "Bhutanese Ngultrum (BTN)", "Bolivian Boliviano (BOB)", "Bosnia-Herzegovina Convertible Mark (BAM)",
        "Botswana Pula (BWP)", "Brazilian Real (BRL)", "British Pound (GBP)", "Brunei Dollar (BND)", "Bulgarian Lev (BGN)",
        "Burundian Franc (BIF)", "Cambodian Riel (KHR)", "Canadian Dollar (CAD)", "Cape Verdean Escudo (CVE)", "Cayman Islands Dollar (KYD)",
        "Central African CFA Franc (XAF)", "Chilean Peso (CLP)", "Chinese Yuan (CNY)", "Colombian Peso (COP)", "Comorian Franc (KMF)",
        "Congolese Franc (CDF)", "Costa Rican Colón (CRC)", "Croatian Kuna (HRK)", "Cuban Convertible Peso (CUC)", "Cuban Peso (CUP)",
        "Czech Koruna (CZK)", "Danish Krone (DKK)", "Djiboutian Franc (DJF)", "Dominican Peso (DOP)", "East Caribbean Dollar (XCD)",
        "Egyptian Pound (EGP)", "Eritrean Nakfa (ERN)", "Estonian Kroon (EEK)", "Eswatini Lilangeni (SZL)", "Ethiopian Birr (ETB)",
        "Euro (EUR)", "Falkland Islands Pound (FKP)", "Fijian Dollar (FJD)", "Gambian Dalasi (GMD)", "Georgian Lari (GEL)",
        "Ghanaian Cedi (GHS)", "Gibraltar Pound (GIP)", "Guatemalan Quetzal (GTQ)", "Guinean Franc (GNF)", "Guyanaese Dollar (GYD)",
        "Haitian Gourde (HTG)", "Honduran Lempira (HNL)", "Hong Kong Dollar (HKD)", "Hungarian Forint (HUF)", "Icelandic Króna (ISK)",
        "Indian Rupee (INR)", "Indonesian Rupiah (IDR)", "Iranian Rial (IRR)", "Iraqi Dinar (IQD)", "Israeli New Shekel (ILS)",
        "Jamaican Dollar (JMD)", "Japanese Yen (JPY)", "Jordanian Dinar (JOD)", "Kazakhstani Tenge (KZT)", "Kenyan Shilling (KES)",
        "Kuwaiti Dinar (KWD)", "Kyrgystani Som (KGS)", "Lao Kip (LAK)", "Latvian Lats (LVL)", "Lebanese Pound (LBP)",
        "Lesotho Loti (LSL)", "Liberian Dollar (LRD)", "Libyan Dinar (LYD)", "Lithuanian Litas (LTL)", "Macanese Pataca (MOP)",
        "Macedonian Denar (MKD)", "Malagasy Ariary (MGA)", "Malawian Kwacha (MWK)", "Malaysian Ringgit (MYR)", "Maldivian Rufiyaa (MVR)",
        "Mauritanian Ouguiya (MRU)", "Mauritian Rupee (MUR)", "Mexican Peso (MXN)", "Moldovan Leu (MDL)", "Mongolian Tögrög (MNT)",
        "Moroccan Dirham (MAD)", "Mozambican Metical (MZN)", "Myanmar Kyat (MMK)", "Namibian Dollar (NAD)", "Nepalese Rupee (NPR)",
        "Netherlands Antillean Guilder (ANG)", "New Taiwan Dollar (TWD)", "New Zealand Dollar (NZD)", "Nicaraguan Córdoba (NIO)", "Nigerian Naira (NGN)",
        "North Korean Won (KPW)", "Norwegian Krone (NOK)", "Omani Rial (OMR)", "Pakistani Rupee (PKR)", "Panamanian Balboa (PAB)",
        "Papua New Guinean Kina (PGK)", "Paraguayan Guaraní (PYG)", "Peruvian Sol (PEN)", "Philippine Peso (PHP)", "Polish Złoty (PLN)",
        "Qatari Riyal (QAR)", "Romanian Leu (RON)", "Russian Ruble (RUB)", "Rwandan Franc (RWF)", "Saint Helena Pound (SHP)",
        "Samoan Tala (WST)", "Sao Tome and Principe Dobra (STN)", "Saudi Riyal (SAR)", "Serbian Dinar (RSD)", "Seychellois Rupee (SCR)",
        "Sierra Leonean Leone (SLL)", "Singapore Dollar (SGD)", "Solomon Islands Dollar (SBD)", "Somali Shilling (SOS)", "South African Rand (ZAR)",
        "South Korean Won (KRW)", "South Sudanese Pound (SSP)", "Sri Lankan Rupee (LKR)", "Sudanese Pound (SDG)", "Surinamese Dollar (SRD)",
        "Swazi Lilangeni (SZL)", "Swedish Krona (SEK)", "Swiss Franc (CHF)", "Syrian Pound (SYP)", "Tajikistani Somoni (TJS)",
        "Tanzanian Shilling (TZS)", "Thai Baht (THB)", "Tongan Paʻanga (TOP)", "Trinidad and Tobago Dollar (TTD)", "Tunisian Dinar (TND)",
        "Turkmenistani Manat (TMT)", "Ugandan Shilling (UGX)", "Ukrainian Hryvnia (UAH)", "United Arab Emirates Dirham (AED)", "United States Dollar (USD)",
        "Uruguayan Peso (UYU)", "Uzbekistani Som (UZS)", "Vanuatu Vatu (VUV)", "Venezuelan Bolívar Soberano (VES)", "Vietnamese Đồng (VND)",
        "West African CFA Franc (XOF)", "Yemeni Rial (YER)", "Zambian Kwacha (ZMW)", "Zimbabwean Dollar (ZWL)"
        ]

    
    
    countries = [
    {"name": "Afghanistan", "code": "AF"},
    {"name": "Albania", "code": "AL"},
    {"name": "Algeria", "code": "DZ"},
    {"name": "Andorra", "code": "AD"},
    {"name": "Angola", "code": "AO"},
    {"name": "Antigua and Barbuda", "code": "AG"},
    {"name": "Argentina", "code": "AR"},
    {"name": "Armenia", "code": "AM"},
    {"name": "Australia", "code": "AU"},
    {"name": "Austria", "code": "AT"},
    {"name": "Azerbaijan", "code": "AZ"},
    {"name": "Bahamas", "code": "BS"},
    {"name": "Bahrain", "code": "BH"},
    {"name": "Bangladesh", "code": "BD"},
    {"name": "Barbados", "code": "BB"},
    {"name": "Belarus", "code": "BY"},
    {"name": "Belgium", "code": "BE"},
    {"name": "Belize", "code": "BZ"},
    {"name": "Benin", "code": "BJ"},
    {"name": "Bhutan", "code": "BT"},
    {"name": "Bolivia", "code": "BO"},
    {"name": "Bosnia and Herzegovina", "code": "BA"},
    {"name": "Botswana", "code": "BW"},
    {"name": "Brazil", "code": "BR"},
    {"name": "Brunei", "code": "BN"},
    {"name": "Bulgaria", "code": "BG"},
    {"name": "Burkina Faso", "code": "BF"},
    {"name": "Burundi", "code": "BI"},
    {"name": "Cabo Verde", "code": "CV"},
    {"name": "Cambodia", "code": "KH"},
    {"name": "Cameroon", "code": "CM"},
    {"name": "Canada", "code": "CA"},
    {"name": "Central African Republic", "code": "CF"},
    {"name": "Chad", "code": "TD"},
    {"name": "Chile", "code": "CL"},
    {"name": "China", "code": "CN"},
    {"name": "Colombia", "code": "CO"},
    {"name": "Comoros", "code": "KM"},
    {"name": "Congo, Democratic Republic of the", "code": "CD"},
    {"name": "Congo, Republic of the", "code": "CG"},
    {"name": "Costa Rica", "code": "CR"},
    {"name": "Croatia", "code": "HR"},
    {"name": "Cuba", "code": "CU"},
    {"name": "Cyprus", "code": "CY"},
    {"name": "Czech Republic", "code": "CZ"},
    {"name": "Denmark", "code": "DK"},
    {"name": "Djibouti", "code": "DJ"},
    {"name": "Dominica", "code": "DM"},
    {"name": "Dominican Republic", "code": "DO"},
    {"name": "Ecuador", "code": "EC"},
    {"name": "Egypt", "code": "EG"},
    {"name": "El Salvador", "code": "SV"},
    {"name": "Equatorial Guinea", "code": "GQ"},
    {"name": "Eritrea", "code": "ER"},
    {"name": "Estonia", "code": "EE"},
    {"name": "Eswatini", "code": "SZ"},
    {"name": "Ethiopia", "code": "ET"},
    {"name": "Fiji", "code": "FJ"},
    {"name": "Finland", "code": "FI"},
    {"name": "France", "code": "FR"},
    {"name": "Gabon", "code": "GA"},
    {"name": "Gambia", "code": "GM"},
    {"name": "Georgia", "code": "GE"},
    {"name": "Germany", "code": "DE"},
    {"name": "Ghana", "code": "GH"},
    {"name": "Greece", "code": "GR"},
    {"name": "Grenada", "code": "GD"},
    {"name": "Guatemala", "code": "GT"},
    {"name": "Guinea", "code": "GN"},
    {"name": "Guinea-Bissau", "code": "GW"},
    {"name": "Guyana", "code": "GY"},
    {"name": "Haiti", "code": "HT"},
    {"name": "Honduras", "code": "HN"},
    {"name": "Hungary", "code": "HU"},
    {"name": "Iceland", "code": "IS"},
    {"name": "India", "code": "IN"},
    {"name": "Indonesia", "code": "ID"},
    {"name": "Iran", "code": "IR"},
    {"name": "Iraq", "code": "IQ"},
    {"name": "Ireland", "code": "IE"},
    {"name": "Israel", "code": "IL"},
    {"name": "Italy", "code": "IT"},
    {"name": "Jamaica", "code": "JM"},
    {"name": "Japan", "code": "JP"},
    {"name": "Jordan", "code": "JO"},
    {"name": "Kazakhstan", "code": "KZ"},
    {"name": "Kenya", "code": "KE"},
    {"name": "Kiribati", "code": "KI"},
    {"name": "Korea, North", "code": "KP"},
    {"name": "Korea, South", "code": "KR"},
    {"name": "Kosovo", "code": "XK"},
    {"name": "Kuwait", "code": "KW"},
    {"name": "Kyrgyzstan", "code": "KG"},
    {"name": "Laos", "code": "LA"},
    {"name": "Latvia", "code": "LV"},
    {"name": "Lebanon", "code": "LB"},
    {"name": "Lesotho", "code": "LS"},
    {"name": "Liberia", "code": "LR"},
    {"name": "Libya", "code": "LY"},
    {"name": "Liechtenstein", "code": "LI"},
    {"name": "Lithuania", "code": "LT"},
    {"name": "Luxembourg", "code": "LU"},
    {"name": "Madagascar", "code": "MG"},
    {"name": "Malawi", "code": "MW"},
    {"name": "Malaysia", "code": "MY"},
    {"name": "Maldives", "code": "MV"},
    {"name": "Mali", "code": "ML"},
    {"name": "Malta", "code": "MT"},
    {"name": "Marshall Islands", "code": "MH"},
    {"name": "Mauritania", "code": "MR"},
    {"name": "Mauritius", "code": "MU"},
    {"name": "Mexico", "code": "MX"},
    {"name": "Micronesia", "code": "FM"},
    {"name": "Moldova", "code": "MD"},
    {"name": "Monaco", "code": "MC"},
    {"name": "Mongolia", "code": "MN"},
    {"name": "Montenegro", "code": "ME"},
    {"name": "Morocco", "code": "MA"},
    {"name": "Mozambique", "code": "MZ"},
    {"name": "Myanmar", "code": "MM"},
    {"name": "Namibia", "code": "NA"},
    {"name": "Nauru", "code": "NR"},
    {"name": "Nepal", "code": "NP"},
    {"name": "Netherlands", "code": "NL"},
    {"name": "New Zealand", "code": "NZ"},
    {"name": "Nicaragua", "code": "NI"},
    {"name": "Niger", "code": "NE"},
    {"name": "Nigeria", "code": "NG"},
    {"name": "North Macedonia", "code": "MK"},
    {"name": "Norway", "code": "NO"},
    {"name": "Oman", "code": "OM"},
    {"name": "Pakistan", "code": "PK"},
    {"name": "Palau", "code": "PW"},
    {"name": "Palestine", "code": "PS"},
    {"name": "Panama", "code": "PA"},
    {"name": "Papua New Guinea", "code": "PG"},
    {"name": "Paraguay", "code": "PY"},
    {"name": "Peru", "code": "PE"},
    {"name": "Philippines", "code": "PH"},
    {"name": "Poland", "code": "PL"},
    {"name": "Portugal", "code": "PT"},
    {"name": "Qatar", "code": "QA"},
    {"name": "Romania", "code": "RO"},
    {"name": "Russia", "code": "RU"},
    {"name": "Rwanda", "code": "RW"},
    {"name": "Saint Kitts and Nevis", "code": "KN"},
    {"name": "Saint Lucia", "code": "LC"},
    {"name": "Saint Vincent and the Grenadines", "code": "VC"},
    {"name": "Samoa", "code": "WS"},
    {"name": "San Marino", "code": "SM"},
    {"name": "Sao Tome and Principe", "code": "ST"},
    {"name": "Saudi Arabia", "code": "SA"},
    {"name": "Senegal", "code": "SN"},
    {"name": "Serbia", "code": "RS"},
    {"name": "Seychelles", "code": "SC"},
    {"name": "Sierra Leone", "code": "SL"},
    {"name": "Singapore", "code": "SG"},
    {"name": "Slovakia", "code": "SK"},
    {"name": "Slovenia", "code": "SI"},
    {"name": "Solomon Islands", "code": "SB"},
    {"name": "Somalia", "code": "SO"},
    {"name": "South Africa", "code": "ZA"},
    {"name": "South Sudan", "code": "SS"},
    {"name": "Spain", "code": "ES"},
    {"name": "Sri Lanka", "code": "LK"},
    {"name": "Sudan", "code": "SD"},
    {"name": "Suriname", "code": "SR"},
    {"name": "Sweden", "code": "SE"},
    {"name": "Switzerland", "code": "CH"},
    {"name": "Syria", "code": "SY"},
    {"name": "Taiwan", "code": "TW"},
    {"name": "Tajikistan", "code": "TJ"},
    {"name": "Tanzania", "code": "TZ"},
    {"name": "Thailand", "code": "TH"},
    {"name": "Timor-Leste", "code": "TL"},
    {"name": "Togo", "code": "TG"},
    {"name": "Tonga", "code": "TO"},
    {"name": "Trinidad and Tobago", "code": "TT"},
    {"name": "Tunisia", "code": "TN"},
    {"name": "Turkey", "code": "TR"},
    {"name": "Turkmenistan", "code": "TM"},
    {"name": "Tuvalu", "code": "TV"},
    {"name": "Uganda", "code": "UG"},
    {"name": "Ukraine", "code": "UA"},
    {"name": "United Arab Emirates", "code": "AE"},
    {"name": "United Kingdom", "code": "GB"},
    {"name": "United States", "code": "US"},
    {"name": "Uruguay", "code": "UY"},
    {"name": "Uzbekistan", "code": "UZ"},
    {"name": "Vanuatu", "code": "VU"},
    {"name": "Vatican City", "code": "VA"},
    {"name": "Venezuela", "code": "VE"},
    {"name": "Vietnam", "code": "VN"},
    {"name": "Yemen", "code": "YE"},
    {"name": "Zambia", "code": "ZM"},
    {"name": "Zimbabwe", "code": "ZW"}
]

    
            # print(data)
    # print("hello came here")
    
    
    
    referral_id = request.GET.get('referralid') 
    # if referral_id:
    #     # check whether user is active or not
    #     getmember=ZqUser.objects.filter(username=referral_id.strip())
        
    #     if getmember.count()>0:
    #         # check activation
    #         if not getmember.first().status:
                
    #             referral_id = '' 
                

    
    try:
        if request.method == 'POST':
            print("hello came here 1")
            
            
            fErrors = {}
         
            enteredUsername = request.POST.get('username', '').strip()
            enteredEmail = request.POST.get('email', '').strip()
            password1 = request.POST.get('password1', '').strip()
            password2 = request.POST.get('password2', '').strip()
            print("hello came here 2")
                
            if password1!=password2:
                fErrors['password2'] = 'password and confirm password do not match'
          
            if len(fErrors)>0:
                return render(request, 'cointex/register.html',context={'fErrors': fErrors,'logTab':'','regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})

                   
            print("hello came here 3")  

            try:
                
                print("hello came here to check")  
                doesUserAlreadyExistInDB=ZqUser.objects.get(email=enteredEmail)
                # doesUserAlreadyExistInDB=ZqUser.objects.get(email=enteredEmail)
            except:
                doesUserAlreadyExistInDB=None
                
            print("hello came to check condition")  
            if doesUserAlreadyExistInDB and  not doesUserAlreadyExistInDB.is_active and not doesUserAlreadyExistInDB.is_verfied:
                print("hello came to check  and condition passed")  

                if doesUserAlreadyExistInDB.username.strip()==enteredUsername.strip():
                    # print("hello came to check  and condition passed and agsin passed")  
                    doesUserAlreadyExistInDB.password=make_password(password2)
                    if sendMailVerificationEmail(request,doesUserAlreadyExistInDB,enteredEmail):
                        # print('came to redirect for uconfirmed email')

                        return redirect('unconfirmedEmail')
                else:
                    # print("hello came to check  and condition passed and agsin came to check else condition")  

                    try:
                        doesUserNameAlreadyExistInDB=ZqUser.objects.get(username=enteredUsername)
                        fErrors['username'] = 'Username already taken'
                        
                        # print('for with eerr')
                        return render(request,'cointex/register.html',context={'fErrors': fErrors,'logTab':'','regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})

                    except:
                        doesUserNameAlreadyExistInDB=None
                  
                    print("hello came to check---------------------- condition")  
 
                    try:
                            doesUserAlreadyExistInDB.username=enteredUsername
                            doesUserAlreadyExistInDB.password=make_password(password2)
                            doesUserAlreadyExistInDB.save()
                            # if doesUserAlreadyExistInDB.username.strip()==enteredUsername.strip():
                            if sendMailVerificationEmail(request,doesUserAlreadyExistInDB,enteredEmail):
                            
                            
                                return redirect('unconfirmedEmail')
                            
                    except Exception as e:
                        print(str(e))
              
            
            
            
            print("hello came here 4")  

            form = UserForm(request.POST)
            
            print('is form valid',form.is_valid())
            print('is form valid',form)

            if form.is_valid():
                
                # print('came to check if form is valid')

                
                
                try:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.is_verfied = False
                    user.save()
                    
                    # if user:
                    #     response.set_signed_cookie('registered_user', user.username, max_age=60*60*24*365*2, salt='registration_salt')

                except Exception as e:
                    print(e)
            
               
                print('came to send verification email')

                # mail_subject = 'Activate your account.'
                if sendMailVerificationEmail(request,user,form.cleaned_data.get('email')):
                    
                    
                    result={'success': True, 'msg': 'An activation link had been sent to your entered email please click on that link to activate your account','redirect_url':reverse('preConfirmEmail')}
                    return redirect('preConfirmEmail')
                    # return redirect('otp')
                else:
                    
                    # return render(request, 'zqapp/register.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
                    return render(request, 'cointex/register.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
                return render(request, 'zqapp/register.html',context={'form': form,'isActive':True,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False'})
                        
                    
          

            
            else:
                if referral_id:
                    # return render(request,reverse('index'),context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False'})
                    return render(request,reverse('login'),context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False'})
                return render(request, reverse('login'),context={'form': form,'isActive':True,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False'})
                
    except Exception as e:
        
            print(str(e))
            # return render(request, 'surveyappHome/index.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
            return render(request, 'cointex/register.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})





    form = UserForm()
    
    if referral_id:
        # return render(request, 'surveyappHome/index.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
        return render(request, 'cointex/register.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
  
  
    print("came here")
    # return render(request,'surveyappHome/index.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
    return render(request,'cointex/register.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries})
 

def activate(request, uidb64, token):
   
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = ZqUser.objects.get(pk=uid)
        
        print(uid,user)
    except(TypeError, ValueError, OverflowError, ZqUser.DoesNotExist):
        user = None
        print(user)
        print(email_verification_token.check_token(user, token))
    if user is not None and email_verification_token.check_token(user, token):
        
        user.is_active = True
        user.is_verfied = True
        usersIntroducersUsername=ZqUser.objects.get(memberid=user.introducerid.memberid)
        user.introducer_username=usersIntroducersUsername.username
        user.save()
        plainPass=user.plain_password
     

        newUser=user
                                    
        if newUser:
        
            
            creditToReceiverWallet=TransactionHistoryOfCoin.objects.create(
                        cointype='USD',
                        memberid=newUser,
                        name=newUser.username,
                        hashtrxn='SIGNUP BONUS',
                        amount=10,
                        coinvalue=90,
                        trxndate=datetime.now(),
                        status=1,
                        coinvaluedate=datetime.now(),
                        total=10,
                        amicoinvalue=90,
                        amifreezcoin=float(90),
                        amivolume=90,
                        totalinvest=10,
                        tran_type='CREDIT',
                        purpose="SIGNUP BONUS"
                    )
                                
            # bot purchase
            debitFromPayeeWallet=TransactionHistoryOfCoin.objects.create(
                        cointype='USD',
                        memberid=newUser,
                        name=newUser.username,
                        hashtrxn='INVESTMENT',
                        amount=10,
                        coinvalue=90,
                        trxndate=datetime.now(),
                        status=1,
                        coinvaluedate=datetime.now(),
                        total=10,
                        amicoinvalue=90,
                        amifreezcoin=float(90),
                        amivolume=90,
                        totalinvest=10,
                        tran_type='DEBIT',
                        purpose="SIGNUP INVESTMENT"	
                    )
            getLatestBot=Bot.objects.all().order_by('-bot_price_set_date').first()
            newBotPurchaseEntry=BotPurchaseDetails.objects.create(purchase_price=getLatestBot.price,purchased_by=newUser,bot_id=getLatestBot)

            newInvestmentWalletEntry=InvestmentWallet.objects.create(
                                            txn_by=newUser,
                                            amount=10,
                                            remark=f'USDT {10} is added  to your investment wallet',
                                            txn_date=timezone.now(),
                                            txn_type='CREDIT',
                                            wallet_type='INVESTMENT',
                                            zaan_rate=0,
                                            usd_rate=0,
                                            activated_by=newUser,
                                            is_signup_bonus=True
                                            )
        
            

            login(request, newUser, backend='django.contrib.auth.backends.ModelBackend')


        
        if 'newUserId' in request.session:
            del request.session['newUserId']
        # for backend in get_backends():
        #     print(backend)
        #     # if backend.user_can_authenticate(user):
                
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
       
        sendSuccessRegMail(request.user,plainPass )
            
         
        messages.success(request, 'Your email has been verified and  you are now logged in')
        return redirect('newmemberDashboard')
    else:
        return redirect('linkexpired')
  
 
 
def unconfirmedEmail(request):
    
    
    # if request.user.is_verfied:
    #      return redirect('newmemberDashboard')
    # if request.user.is_verfied:
    #    
    # return render(request,'zqUsers/member/unconfirmedEmail.html')
    return render(request,'cointex/uconfirmedemail.html')
 
 
def assignSocialJobs(user):
    
        allDummyUsersForTesting=ZqUser.objects.filter(id=user.id)
        # allDummyUsersForTesting=ZqUser.objects.filter(is_dummy=True,username='vagak1')
        for user in allDummyUsersForTesting:
            
            
            allPackages=InvestmentWallet.objects.filter(txn_by=user)
            allSocialJobs=SocialJobs.objects.all()
            # if allPackages.count()>0:
            #     isPaidUser=True
            # else:
            isPaidUser=False
            
            if isPaidUser:
                
                for package in allPackages:
                    for socialjob in  allSocialJobs:
                        assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=user,package_id=package,social_job_id=socialjob).count()
                        if assignedJobsForThisPackage>0:
                            continue
                        else:
                            allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=user,package_id=package)
                            
                            if allPreviousPackagesCount.count()>0:
                                
                                lastObj=allPreviousPackagesCount.order_by('-id').first()
                                newEntryForThisPackage=AssignedSocialJob(assigned_to=user,package_id=package,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
                                newEntryForThisPackage.save()
                            else:
                                newEntryForThisPackage=AssignedSocialJob(assigned_to=user,package_id=package,social_job_id=socialjob,valid_from=package.txn_date,valid_upto=package.txn_date+timedelta(days=5)+ timedelta(days=2))
                                newEntryForThisPackage.save()
            
            else:
                   
                for socialjob in  allSocialJobs:
                    
                    assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=user,social_job_id=socialjob).count()
                    if assignedJobsForThisPackage>0:
                        continue
                    else:
                        allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=user)
                        if allPreviousPackagesCount.count()>0:
                            lastObj=allPreviousPackagesCount.order_by('-id').first()
                            newEntryForThisPackage=AssignedSocialJob(assigned_to=user,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
                            newEntryForThisPackage.save()
                        else:
                            newEntryForThisPackage=AssignedSocialJob(assigned_to=user,social_job_id=socialjob,valid_from=user.date_joined,valid_upto=user.date_joined+timedelta(days=5)+ timedelta(days=2))
                            newEntryForThisPackage.save()                 
 
 
def sendMailVerificationEmail(request,user,email):
    # randNum=random.randint(100000,999999)
    
    
    # print('came here=============')
    # print(request.META['HTTP_HOST'])
    # print(request.META['HTTP_HOST'])
    # print('user id',user)
    # print('user is',urlsafe_base64_encode(force_bytes(user.pk)))
    # print(email_verification_token.make_token(user))
    html_content = render_to_string('zqapp/emailtemps/verifyEmailToRegister.html',{
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                })
    
    
    # print('came here=========>>',email)
    # print(settings.EMAIL_HOST,settings.EMAIL_PORT,settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD,settings.EMAIL_USE_TLS)
    
    
    try:
        
        print('came here ain=========>>>')

        with get_connection(  
                            
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
            subject = "Activate your account"  
            email_from = "noreply@infinitytrade.world" 
            recipient_list = [email]  
            # message ="This is testing email" 
            body=html_content 
            sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
            # body=html_content 
            # sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
            sendEmail.content_subtype = 'html'
            # print(sendEmail)
            # print('came here ain=========>>>>>')

            # print('came here to send mail=========>>')

            if sendEmail.send():
                print('mail sent successfully')
                request.session['newUserId'] = user.id
                current_time = timezone.now()
                request.session['otp_timestamp'] = current_time.timestamp()
                return True
            
            else:
                # print('')
                logger.error(f"{datetime.now()} :something went wrong while  sending email")
                return False

    except Exception as e:
        print(str(e))
        return False
    
 
def otpVerify(request):
        
    if request.method == 'POST':
        
        print("came here")
        print(json.loads(data))
        
        return
        
        form = OTPVerificationForm(request.POST or None,request=request)
        # print("========came here to verify OTP====",form.is_valid())
        if form.is_valid():
            del request.session['RegOTP']
            
            introId=ZqUser.objects.get(memberid=request.session.get('RegUserIntroID'))
            
            if introId:
                print(introId)
                user = ZqUser.objects.create(username=request.session.get('RegUserUsername'),email=request.session.get('regEmail'),introducerid=introId,password=make_password(request.session.get('RegUserPassword')), country=request.session.get('country'), local_currency=request.session.get('local_currency')) 

                user.is_verfied = True  # Set the field to True
                
                try:
                    user.save()
                except Exception as e:
                    # print(e)
                    logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
            

            # del request.session['new_user_pk']
            del request.session['regEmail']
            # request.session['regUserEmail']=email
            del request.session['RegUserUsername']
            del request.session['RegUserIntroID']
            del request.session['RegUserPassword']
            del request.session['country']
            del request.session['local_currency']

            messages.success(request,  'Thanks for being part of Rimberio Please Login to continue!')
# ===============================changes made here=====================================
            return redirect('index')
            # return None
            
        else:
            
            return render(request,'zqapp/user-otp-auth.html',context={
                
                'form':form
            })
                
    form = OTPVerificationForm(request.POST)
    return render(request, 'zqapp/user-otp-auth.html',context={
        'form':'form'
    })

def resetPassword(request):
    
    if request.method=="POST":
         
        ent_email_or_username=request.POST.get('email_or_username')
        # print(ent_email)

        try:
            if '@' in ent_email_or_username and '.' in ent_email_or_username:
                user = ZqUser.objects.filter(email=ent_email_or_username)
                if user.count()>1:
                    error_message = 'Multiple accounts exist with this email. Please reset  password through username.'

                    return render(request,'zqapp/reset-password.html',context={
                        'error_message':error_message
                    })
                else:
                    user=ZqUser.objects.get(email=ent_email_or_username)
                
            else:
                user = ZqUser.objects.get(username=ent_email_or_username)
                
        except ZqUser.DoesNotExist:
            user = None
            
        if user:
            

          
            sentOTP=send_otp(request=request,email=user.email,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='passwordReset')
 
            if sentOTP:
                    
                # newOTP=USEROTP.objects.create(email=ent_email,type='resetPass',otp_code=sentOTP)
                # newOTP.save()
                request.session['MEMID']=user.memberid
                # request.session['OTP']
                
                messages.success(request, "OTP sent successfully please verify it to change password")     
                return render(request,'zqapp/password-reset-otp-auth.html',context={
                    'email': user.email
                })
        else:
            messages.add_message(request,messages.WARNING, "member with this email doesn't exist")
            # messages.error(request, "member with this email doesn't exist")
            # redirect('passwordReset')
            error_message = 'member with this email or username does not exist please enter correct username or email'

            return render(request,'zqapp/reset-password.html',context={
                'error_message':error_message
            })
        
        
    
    return render(request,'zqapp/reset-password.html')
    
    
def resetOtpVerify(request):
    
    if request.method == 'POST':
        Otp =request.POST.get('otp')
 
        if str(Otp)==str(request.session.get('OTP')):

           
            del request.session['OTP']
            
            messages.success(request, "OTP verified successfully")
            return render(request,'zqapp/new-password.html')
        
        else:
            
            messages.warning(request, "Invalid OTP")
            return render(request,'zqapp/password-reset-otp-auth.html',context={
                'message':'Invalid OTP',
                
            })
        

    return render(request, 'zqapp/password-reset-otp-auth.html')


def newPassword(request):
    
    if request.method == 'POST':
        
 
        password =request.POST.get('password')
        confPassword =request.POST.get('confPassword')     
   
        if password==confPassword:


            try:
                user=ZqUser.objects.get(memberid=request.session.get('MEMID'))
                user.set_password(password)
                user.save()
            except Exception as e:
                logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
                # print(e)
            
            messages.success(request, "Password changed successfully please login to continue")
            return redirect('login')
        

        
        else:
            
             messages.warning(request, "Invalid Password")
             return render(request,'zqapp/new-password.html',context={
                    'message':'Password does not match'
                })
        
            
            

    return render(request, 'zqapp/new-password.html')
    

def send_mail(request,email,template):

    randNum=random.randint(100000,999999)
    html_content = render_to_string('zqapp/emailtemps/'+template, {'OTP': randNum})
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "This is testing email"  
        email_from = "noreply@infinitytrade.world" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
       
        # print(sendEmail)
        if sendEmail:
            # print('mail sent successfully')
            request.session['OTP'] = randNum
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False


def send_otp(request,email,subject,template,whatfor):
    
   
    randNum=random.randint(100000,999999)

    html_content = render_to_string('zqapp/emailtemps/'+template, {'OTP': randNum})
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = subject  
        email_from = "noreply@infinitytrade.world" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
       

        if sendEmail:
            
            if whatfor=="topup":
                
                obj = SendOTP()
                obj.email = email
                obj.otp = int(randNum)
                obj.trxndate = datetime.now()
                obj.status = 1
                obj.save()
                return True
            
            elif whatfor=="register":
                
                request.session['RegOTP'] = randNum
                print(randNum)
                
              
                return True
            elif whatfor=="send_otp_receive_wallet_address":
                
                # request.session['OTP'] = randNum
                return randNum
                
            elif whatfor=="passwordReset":
                
                request.session['OTP'] = randNum
                return randNum
                
            
            
            # print('mail sent successfully')
            
            
        
        else:
            
            logger.error(f"{datetime.now()} :An error occurred: something went wrong while  sending email")
            return False


def encrypt_otp(otp_value):
    # Replace 'your_secret_key' with a strong secret key
    secret_key = b'\x92#\xe4\xf7\x9a\x87\xc1\x1e\x9b\xbf\x87\xbb5w\x81'
    encrypted_value = base64.b64encode(otp_value.encode())
    return encrypted_value


def decrypt_otp(encrypted_value):
    secret_key = b'\x92#\xe4\xf7\x9a\x87\xc1\x1e\x9b\xbf\x87\xbb5w\x81'
    decrypted_value = base64.b64decode(encrypted_value)
    return decrypted_value.decode()


def set_otp_cookie(request, otp_value):
    encrypted_otp = encrypt_otp(otp_value)
    
    # print("OTP cookie set successfully")
    response = HttpResponse()
    response.set_cookie('OTP', encrypted_otp, max_age=None)  # Set max_age=None to make the cookie a session cookie
    return response


def get_otp_cookie(request):
    encrypted_otp = request.COOKIES.get('OTP')
    if encrypted_otp:
        decrypted_otp = decrypt_otp(encrypted_otp)
        return HttpResponse(f"Decrypted OTP value from cookie: {decrypted_otp}")
    else:
        return HttpResponse("OTP cookie not found")


def resendOTPResetPass(request):

    result={}
    user=ZqUser.objects.get(memberid=request.session.get('MEMID'))
    
    try:
        
        sentOTP=send_otp(request=request,email=user.email,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='passwordReset')

        if sentOTP:   
            result['status']=1
            result['message']='OTP resent to your email successfully'
            return JsonResponse(result)
        else:
            
            result['status']=0
            result['message']='Some error occured while sending email'
            return JsonResponse(result)
            
    except Exception as e:
        
        # print(e)
        logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        result['status']=0
        result['message']='Some error occured'
        return JsonResponse(result)
        
    
def resendOTPReg(request):
    result={}
    Regemail=request.session.get('regEmail')

    try:
        
        sentOTP=send_otp(request=request,email=Regemail,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='register')

        if sentOTP:   
            result['status']=1
            result['message']='OTP resent to your email successfully'
            return JsonResponse(result)
        else:
            
            result['status']=0
            result['message']='Some error occured while sending email'
            return JsonResponse(result)
            
    except Exception as e:
        
        # print(e)
        logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        result['status']=0
        result['message']='Some error occured'
        return JsonResponse(result)
        
                                
def returnMemberName(request):    
    result={}
    if request.method=='POST':
        
        enteredmemid=request.POST.get('memberid')
        fieldType=request.POST.get('fieldType')
        
        
        if not fieldType:
            
            result['status']=0
            result['msg']=''
            return JsonResponse(result)
        
        if enteredmemid:
            entMemId=enteredmemid.strip()
            
            if entMemId == '':
                
                result['status']=0
                result['msg']=''
                return JsonResponse(result)
                
            
        
        else:
            result['status']=0
            result['msg']=''
            return JsonResponse(result)
        
        if fieldType == 'introducerid':
    
        
            try:
                
                if  entMemId.strip().lower().startswith('rbo') or entMemId.strip().lower().startswith('ifo'):
                    entMemId=ZqUser.objects.get(memberid=entMemId)
                else:
                    entMemId=ZqUser.objects.get(username=entMemId)
                    
                if entMemId.bankname:
                    
                    result['memberName']=entMemId.bankname
                    
                else:
                    result['memberName']=entMemId.username
                    
                result['status']=1
                return JsonResponse(result)
                
            except:
                
                result['status']=0
                result['msg']="User with entered memberid doesn't exist"
                return JsonResponse(result)
                
                # entMemId=None
                

        if fieldType == 'username':
            
            userName=request.POST.get('username')
            
            
            try:
                
                # if entMemId.strip().lower().startswith('fb') or entMemId.strip().lower().startswith('zq'):
                entMemId=ZqUser.objects.get(username=userName)
              
                
                
            except Exception as e:
                
                entMemId=None
              
            
            if entMemId:
                result['status']=1
                result['msg']='Username already taken'
                return JsonResponse(result)
            else:
                result['status']=0
                result['msg']=''
                return JsonResponse(result)
        

def userLogin(request):
    
    
    
    if request.method == "POST":
        
        form=LoginForm(request.POST)
        
        if form.is_valid():
            
            email_or_username=form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']
            
        else:
            
            return render(request,'cointex/log-in.html',context={
                            'login_error': 'Invalid username or password',
                            # 'currencies':currencies, 'countries':countries,
                            'logTab':True
                            })

        if  '@' in email_or_username and '.' in  email_or_username :
            userInfo=ZqUser.objects.get(email=email_or_username)
        else:
            logger.info(f"username is {email_or_username}")
            userInfo=ZqUser.objects.get(username=email_or_username)
            logger.info(f"email is {userInfo.email}")

            
        if  userInfo.is_blocked:
            return redirect('login')


        if userInfo.is_verfied :
            
            
            
            if userInfo.userType=='member' :
            
                user = authenticate(request, username=email_or_username,password=password)
                logger.info(f"user is {user.username}, {user.password}")
                # print(user)
            
                if user is not None:
                    login(request, user)
                    
                    # messages.success(request, "You have been logged in successfully.")
                    # next_url = request.GET.get('next')
                    next_url = request.POST.get("next", "/") 
                    
                    
                    # print(next_url)
                    if next_url:
                        response=redirect(next_url)
                        response.set_signed_cookie('registered_user', user.memberid, max_age=60*60*24*365*2, salt='registration_salt')

                        return response
                        # redirect_url = next_url  # Change this to your desired URL
                        # return JsonResponse({'success': True, 'redirect_url': redirect_url})
                    else:
                    
                    
                        response=redirect('newmemberDashboard') 
                        response.set_signed_cookie('registered_user', user.memberid, max_age=60*60*24*365*2, salt='registration_salt')

                        return response
                        # return

                # return redirect('success')
                else:
                    # Return an error message
                    messages.error(request, "Invalid username or password.")


                    return render(request,'cointex/log-in.html',context={
                        'login_error': 'Invalid username or password',
                        # 'currencies':currencies, 'countries':countries,
                        'logTab':True
                        })
                    
            elif userInfo.userType=='admin':
                
                if 'email' in form.cleaned_data:
                # userInfo=ZqUser.objects.filter(email=email_or_username)
                    user = authenticate(request, email=email_or_username, password=password)
                else:
                # userInfo=ZqUser.objects.filter(username=email_or_username)
                    user = authenticate(request, username=email_or_username, password=password)
            
        
                if user is not None:
                    login(request, user)
            
                    # messages.success(request, "You have been logged in successfully.")
                    # next_url = request.GET.get('next')
                    next_url = request.POST.get('next') 
                    # print(next_url)
                    if next_url:
                        # return redirect(next_url)
                        return redirect(next_url)
                    else:
                    # If there's no next parameter, redirect to a default URL
                        # redirect_url = '/member/'  # Change this to your desired URL
                        return redirect('zqAdminDashboard') 
                        # return redirect('newmemberDashboard')  # R
                        
                        # return

                # return redirect('success')
                else:
                    # Return an error message
                    messages.error(request, "Invalid username or password.")
                    # messages.add_message(request, messages.WARNING, 'User logged out successfully')
                    
                    # error_message = "Invalid username or password."
                #    ============================== # chnages heer======================================================
                #     return render(request,'zqUsers/register.html',context={
                #     'login_error': 'Invalid username or password'
                # })
                    # return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
                #     return render(request,'zqapp/register.html',context={
                #     'login_error': 'Invalid username or password'
                # })
                    # return render(request, 'surveyappHome/index.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})
                    
                    return render(request, 'cointex/log-in.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})



    
    if True:
        
   
        email_or_username = request.GET.get("uid", "").strip()
        
        
        if  email_or_username and len(email_or_username)>4  :
            
            email_or_username=email_or_username
            logger.info(f"username is {request.GET}")
            # password = form.cleaned_data['password']
            
            # getUser=ZqUser.objects.get(username=email_or_username)

            try:
                if '@' in email_or_username and '.' in email_or_username:
                    userInfo = ZqUser.objects.get(email=email_or_username)
                else:
                    logger.info(f"username is {email_or_username}")
                    userInfo = ZqUser.objects.get(username=email_or_username)
                    logger.info(f"email is {userInfo.email}")
            except ZqUser.DoesNotExist:
                messages.error(request, "User does not exist.")
                return render(request, 'cointex/log-in.html', context={
                    'login_error': 'User does not exist',
                    'logTab': True
                })




            
            
        
            # if  '@' in email_or_username and '.' in  email_or_username :
            #     userInfo=ZqUser.objects.get(email=email_or_username)
            # else:
            #     logger.info(f"username is {email_or_username}")
            #     userInfo=ZqUser.objects.get(username=email_or_username)
            #     logger.info(f"email is {userInfo.email}")

             
            if  userInfo.is_blocked:
                return redirect('login')

        
            if userInfo.is_verfied :
                
                
                
                if userInfo.userType=='member' :
                
                    user = authenticate(request, username=email_or_username,password=userInfo.plain_password)
                    logger.info(f"user is {user.username}, {user.password}")
                    # print(user)
                
                    if user is not None:
                        login(request, user)
                        
                        messages.success(request, "You have been logged in successfully.")
                        # next_url = request.GET.get('next')
                        next_url = request.GET.get("next", "/") 
                       
                        
                        # print(next_url)
                        if next_url:
                            response=redirect(next_url)
                            response.set_signed_cookie('registered_user', user.memberid, max_age=60*60*24*365*2, salt='registration_salt')

                            return response
                            # redirect_url = next_url  # Change this to your desired URL
                            # return JsonResponse({'success': True, 'redirect_url': redirect_url})
                        else:
                       
                        
                            response=redirect('newmemberDashboard') 
                            response.set_signed_cookie('registered_user', user.memberid, max_age=60*60*24*365*2, salt='registration_salt')

                            return response
                            # return

                    # return redirect('success')
                    else:
                        # Return an error message
                        messages.error(request, "Invalid username or password.")
      

                        return render(request,'cointex/log-in.html',context={
                            'login_error': 'Invalid username or password',
                            # 'currencies':currencies, 'countries':countries,
                            'logTab':True
                            })
                        
                elif userInfo.userType=='admin':
                    
                    if 'email' in form.cleaned_data:
                    # userInfo=ZqUser.objects.filter(email=email_or_username)
                        user = authenticate(request, email=email_or_username, password=password)
                    else:
                    # userInfo=ZqUser.objects.filter(username=email_or_username)
                        user = authenticate(request, username=email_or_username, password=password)
                
            
                    if user is not None:
                        login(request, user)
                
                        messages.success(request, "You have been logged in successfully.")
                        # next_url = request.GET.get('next')
                        next_url = request.POST.get('next') 
                        # print(next_url)
                        if next_url:
                            # return redirect(next_url)
                            return redirect(next_url)
                        else:
                        # If there's no next parameter, redirect to a default URL
                            # redirect_url = '/member/'  # Change this to your desired URL
                            return redirect('zqAdminDashboard') 
                            # return redirect('newmemberDashboard')  # R
                            
                            # return

                    # return redirect('success')
                    else:
                        # Return an error message
                        messages.error(request, "Invalid username or password.")
                        # messages.add_message(request, messages.WARNING, 'User logged out successfully')
                        
                        # error_message = "Invalid username or password."
                    #    ============================== # chnages heer======================================================
                    #     return render(request,'zqUsers/register.html',context={
                    #     'login_error': 'Invalid username or password'
                    # })
                        # return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
                    #     return render(request,'zqapp/register.html',context={
                    #     'login_error': 'Invalid username or password'
                    # })
                        # return render(request, 'surveyappHome/index.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})
                        return render(request, 'cointex/log-in.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})


                        



    return render(request, 'cointex/log-in.html',context={'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true'})



def resendActivationEmail(request):
    
    
    current_time = timezone.now()
    otp_timestamp = request.session.get('otp_timestamp')
    print('otp is',otp_timestamp)
    if otp_timestamp:
        otp_time = timezone.make_aware(datetime.fromtimestamp(otp_timestamp))
        if current_time < otp_time + timedelta(minutes=1):
            return JsonResponse({'success': True,'msg':'You can request for new activation link after 60 seconds'})


    usrId=request.session.get('newUserId')
    print('user id is',usrId)
    if usrId:
        
        User=ZqUser.objects.get(id=usrId)

    else:
        User=None
    
    
    if User:
        
        if sendMailVerificationEmail(request,User,User.email):
            
            return JsonResponse({'success': True,'msg':'An activation link has been resent to your email succesfully'})
        
        else:
            return JsonResponse({'success': False,'msg':'Something went wrong'})
            
            
    else:
        
        return JsonResponse({'success': False,'msg':'Something went wrong'})
        

def sendRestPassLink(request,user,email):
    # randNum=random.randint(100000,999999)
    
    
    
    # print(request.META['HTTP_HOST'])
    html_content = render_to_string('zqapp/emailtemps/resetPassEmail.html',{
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
                    # 'domain': 'www.rimberio.world',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                })
    
    # print(https://{{ domain }}{% url 'activate' uidb64=uid token=token)
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Reset password request"  
        email_from = "noreply@infinitytrade.world" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        sendEmail.content_subtype = 'html'

        # print(sendEmail)
        if sendEmail.send():
            # print('mail sent successfully')
            request.session['newUserId'] = user.id
            current_time = timezone.now()
            request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False


def generate_random_string(length=10):
    # Define the possible characters in the string
    characters = string.ascii_letters + string.digits  # This includes lowercase, uppercase letters, and digits
    # Generate a random string using random.choices
    random_string = ''.join(random.choices(characters, k=length))
    return random_string



 
def resetPassConf(request, uidb64, token):
    # print("cam ehere")
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = ZqUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ZqUser.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        
        # retun redirect
        
        if 'newUserId' in request.session:
            del request.session['newUserId']
            
        uniqueIdentifier=generate_random_string()
        
        request.session[uniqueIdentifier]=user.id
            
        messages.success(request, 'Your email has been verified please change your password')
    
        return render(request,'cointex/confResetPass.html',context={
            'uniqueIdentifier':uniqueIdentifier
        })
        # for backend in get_backends():
        #     print(backend)
        #     # if backend.user_can_authenticate(user):
                
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #     break
        # login(request, user)
        # print(request.user.username)
        # messages.success(request, 'Your email has been verified and  you are now logged in')
        # return redirect('newmemberDashboard')
    else:
        messages.error(request, 'Invalid credentials please try again')
        return redirect('changePassword')
  
 
 


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def changePassword(request):
    
    
   
    if request.method=='POST':
        
       
        
        type = request.POST.get('type').strip()
        
        
        
        if type == "resetPass" :
            
            data = request.POST.get('email').strip()
            

            
            
            if data:
                
                
                # ent_email_or_username=request.POST.get('email_or_username')
                # print(ent_email)

                try:
                    if '@' in data and '.' in data:
                        
                        if not is_valid_email(data):
                    
                            return JsonResponse({
                                'status':0,
                                'msg':'Please enter a valid email'
                            })
                        member = ZqUser.objects.filter(email=data)
                        if user.count()>1:
                            error_message = 'Multiple accounts exist with this email. Please reset  password through username.'

                            return render(request,'zqapp/reset-password.html',context={
                                'error_message':error_message
                            })
                        else:
                            member=ZqUser.objects.get(email=data)
                        
                    else:
                        member = ZqUser.objects.get(username=data)
                        
                except ZqUser.DoesNotExist:
                    member = None
                
                

                    
            
                # try:
                    
                #     member=ZqUser.objects.get(email=data)
                # except Exception as e:
                #     member=None
                    
                if member:
                    # print("++++++came here")
                    if sendRestPassLink(request,member,member.email):
                            return JsonResponse({
                            'status':1,
                            'msg':'A reset passwowrd link has been sent to your email please click on it to reset your password'
                            })

                    else:
                            return JsonResponse({
                            'status':0,
                            'msg':'something went wrong plase try again '
                            })
                        
                
                else:
                    return JsonResponse({
                        'status':0,
                        'msg':'please enter email that is associated with your account'
                    })
            else:
                # else:
                    return JsonResponse({
                        'status':0,
                        'msg':'Email field is required'
                    })        
        
        elif type == "changePass":
            password = request.POST.get('password').strip()
            conf_password = request.POST.get('conf_password').strip()
            uIdentifier = request.POST.get('uIdentifier').strip()
            print(uIdentifier)
            if uIdentifier in request.session:
                
                userId= request.session.get(uIdentifier)
                try:
                   mem=ZqUser.objects.get(id=userId)
                   del request.session[uIdentifier]
                except:
                    mem=None
                    
                if mem:
                    mem.password=make_password(password)
                    mem.save()
                    
                    messages.success(request,'Your password has been reset successfully please login with your new credentials')
                    return redirect('login')
                
                else:
                    messages.error(request,'unauthenticated operation  was performed please try again')
                    return redirect('changePassword')
                    
            else:
                
                messages.error(request,'unauthenticated operation  was performed please try again')
                return redirect('changePassword')
                       
            
    
    
    return render(request,"surveyappHome/changePassword.html")
    
def resetPass(request):
    
    
    return render(request,"cointex/forget-password.html")
    
def mainConfirm(request):
    
    
    return render(request,"surveyappHome/mainConfirm.html")
    
  

def confirmEmail(request):
    
    # return render(request,"surveyappHome/preConfirmEmailPage.html")
    return render(request,"cointex/otp.html")
    
    
   
def hasUsernameAlreadyTaken(request):
    
    if request.method=='POST':
        ... 
   


def sendSuccessRegMail(user,plainPass):
    # user = ZqUser.objects.get(pk=user_id)
    # token = email_verification_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.pk))
    # asid = urlsafe_base64_encode(force_bytes(assignedSocialJobId))

    # token = long_email_verification_token.make_token(user)
    html_content = render_to_string('zqapp/emailtemps/regisuccess.html',{
                'username': user.username,
                'password': plainPass,
                # 'domain': request.META['HTTP_HOST'],
                # 'domain': 'www.rimberio.world',
                # 'uid': uid,
                # 'asid': asid,
                # 'token': email_verification_token.make_token(user),
            })


    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "InfinityTrade Onboarding"  
        email_from = "noreply@infinitytrade.world" 
        recipient_list = [user.email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        sendEmail.content_subtype = 'html'
       
        # print(sendEmail)
        if sendEmail.send():
            # print('mail sent successfully')
            # request.session['newUserId'] = user.id
            # current_time = timezone.now()
            # request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False



def sendtestmail(request):
    if sendMailTest(request):
        return JsonResponse({
            'success':'Mail sent successfully'
        })
        
    else:
         return JsonResponse({
            'error':'Something went wrong'
        })
         
         

def sendMailTest(request):
    
    
    html_content = render_to_string('zqUsers/emailtemps/testuseremail.html',{
                'username':'Abhishek',
                'password': 'Abhishek',
               
            })
    # Render the HTML template with context
    # html_content = render_to_string('email_template.html', {
    #     'recipient_name': 'John Doe'  # You can pass dynamic data here
    # })

    subject = 'test mail'
    recipient_list = ['amrevrp@gmail.com']
    email_from = settings.DEFAULT_FROM_EMAIL
                      
    # host=settings.EMAIL_HOST, 
    # port=settings.EMAIL_PORT,  
    # username=settings.EMAIL_HOST_USER, 
    # password=settings.EMAIL_HOST_PASSWORD, 

    # Create the email object
    email = EmailMessage(subject, html_content, email_from, recipient_list)
    
    # Specify that the email is HTML
    email.content_subtype = 'html'

    # Send the email
    email.send()

    return HttpResponse('HTML email sent successfully!')

def generate_password(length=10):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))

# Generate a 10-digit random password


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric symbols
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A,
        "\U000024C2-\U0001F251"
        "\U00002702-\U000027B0"
        "\U0001F1E0-\U0001F1FF"  # flags
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)




# def remove_emojis(text):
#     import re
#     emoji_pattern = re.compile(
#         "["
#         "\U0001F600-\U0001F64F"  # emoticons
#         "\U0001F300-\U0001F5FF"  # symbols & pictographs
#         "\U0001F680-\U0001F6FF"  # transport & map symbols
#         "\U0001F1E0-\U0001F1FF"  # flags
#         "\U00002702-\U000027B0"
#         "\U000024C2-\U0001F251"
#         "]+", flags=re.UNICODE
#     )
#     return emoji_pattern.sub(r'', text)


TELEGRAM_BOT_TOKEN = "7822819309:AAEHUsmEFusZAifsAbjM5NIS8dr7lwkR29o"

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print("data is",data)
        logger.info(f"text is {data} ")
        if "message" in data:
            message = data["message"]
            chat_id = message["from"]["id"]
            username = message["from"].get("username", "")
            getFirstName = remove_emojis(message["from"].get("first_name", ""))
            getLastName = remove_emojis(message["from"].get("last_name", ""))
            # getFirstName=message["from"].get("first_name", "")
            # getLastName=message["from"].get("last_name", "")
            bankname=f"{getFirstName} {getLastName}"
            logger.info(f"Bank name is {bankname}")
            logger.info(f"Received message from {username} with chat_id {chat_id} and text: {message} and username is { username} ")

            text = message.get("text", "")
            # print("text is",text)
            logger.info(f"text is {text} ")

            referrer_id = None
            
            # Check if the message contains /start with a referral ID
            allParams = text.split("/start ")
            if text.startswith("/start") and len(allParams)>1:
                
                
                
                try:
                    
                    # getMember=ZqUser.objects.get(username=chat_id)
                    # if getMember:
                    getMember = ZqUser.objects.get(username=chat_id)
                    login(request, getMember, backend='django.contrib.auth.backends.ModelBackend')
                    request.session['telegram_user'] = {
                        'id': chat_id,
                        'memberid': username,
                        'first_name': getFirstName,
                        'last_name': getFirstName,
                    }
                        # process login 
                    
                except Exception as e:
                    logger.error(f"exception occured {str(e)} ")
                    # pass
               
                
                    # allParams = text.split("/start ")
                    # referrer_id='IFO000001'
                    if True:
                        
                        referrer_id=allParams[1] if len(allParams)>1 else None
                        
                        
                        if True:

                            try:
                                with transaction.atomic():
                                

                                    # check whether the introducer is a valid introducer
                                    try:
                                        referredBy = ZqUser.objects.get(memberid=referrer_id) if referrer_id else ZqUser.objects.get(memberid="IFO000001")
                                    except ZqUser.DoesNotExist:
                                        referredBy = ZqUser.objects.get(memberid="IFO000001")
                                        
                                    logger.info(f"referredBy member is {str(referredBy)} ")
                                    # register the user
                                    # password = generate_password(10)
                                    genPass=generate_password(10)
                                    newUser=ZqUser.objects.create(
                                        plain_password=genPass,
                                        username=chat_id,
                                        introducerid=referredBy,
                                        bankname=bankname,
                                        password=make_password(genPass),
                                        introducer_username=referredBy.username,
                                        is_active=True,
                                        is_verfied=True,
                                        # status=True
                                    )
                                    
                                    if newUser:
                                   
                                        
                                        creditToReceiverWallet=TransactionHistoryOfCoin.objects.create(
                                                    cointype='USD',
                                                    memberid=newUser,
                                                    name=newUser.username,
                                                    hashtrxn='SIGNUP BONUS',
                                                    amount=10,
                                                    coinvalue=90,
                                                    trxndate=datetime.now(),
                                                    status=1,
                                                    coinvaluedate=datetime.now(),
                                                    total=10,
                                                    amicoinvalue=90,
                                                    amifreezcoin=float(90),
                                                    amivolume=90,
                                                    totalinvest=10,
                                                    tran_type='CREDIT',
                                                    purpose="SIGNUP BONUS"
                                                )
                                                            
                                        # bot purchase
                                        debitFromPayeeWallet=TransactionHistoryOfCoin.objects.create(
                                                    cointype='USD',
                                                    memberid=newUser,
                                                    name=newUser.username,
                                                    hashtrxn='INVESTMENT',
                                                    amount=10,
                                                    coinvalue=90,
                                                    trxndate=datetime.now(),
                                                    status=1,
                                                    coinvaluedate=datetime.now(),
                                                    total=10,
                                                    amicoinvalue=90,
                                                    amifreezcoin=float(90),
                                                    amivolume=90,
                                                    totalinvest=10,
                                                    tran_type='DEBIT',
                                                    purpose="SIGNUP INVESTMENT"	
                                                )
                                        getLatestBot=Bot.objects.all().order_by('-bot_price_set_date').first()
                                        newBotPurchaseEntry=BotPurchaseDetails.objects.create(purchase_price=getLatestBot.price,purchased_by=newUser,bot_id=getLatestBot)

                                        newInvestmentWalletEntry=InvestmentWallet.objects.create(
                                                                        txn_by=newUser,
                                                                        amount=10,
                                                                        remark=f'USDT {10} is added  to your investment wallet',
                                                                        txn_date=timezone.now(),
                                                                        txn_type='CREDIT',
                                                                        wallet_type='INVESTMENT',
                                                                        zaan_rate=0,
                                                                        usd_rate=0,
                                                                        activated_by=newUser,
                                                                        is_signup_bonus=True
                                                                        )
                                    
                                        

                                        login(request, newUser, backend='django.contrib.auth.backends.ModelBackend')




                            except Exception as e:
                                # print(str(e))\ 
                                logger.error(f"exception occured 2: {str(e)} ")
                            
                            

                    # Send Web App link
                send_web_app_button(chat_id,bankname)
                
            elif text.startswith("/webapp"):
                send_web_app_button(chat_id,bankname)

            

        return JsonResponse({"status": "ok"})




def send_telegram_message(chat_id, text):
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)
    
    
    
def send_web_app_button(chat_id,bankName=None):
    """Sends a button to open the Web App"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🚀 Dear {bankName},\n\nWelcome to our AI-powered bot trading platform! 🤖💰\n\n💹 Earn profits effortlessly with our automated trading system. \n📊 Our smart bots analyze the market 24/7 to maximize your gains. \n🔒 Secure & Transparent – Your funds, your control!\n\n👇 Click below to open the Web App and start your trading journey today! 🌟",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "🌗 Launch infinity Trade", "web_app": {"url": f"https://infinitytrade.cloud/accounts/login/?next=/member/&uid={chat_id}"}}
            ]]
        }
    }
    requests.post(url, json=payload)
    
    
