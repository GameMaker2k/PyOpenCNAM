#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2020 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2020 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pyopencnam.py - Last Update: 10/22/2024 Ver. 1.2.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import imp
import os
import sys
import json
import base64
import platform

'''
if(sys.version_info[:2] <= (3, 4)):
    import imp;
else:
    import importlib;
'''

if __name__ == '__main__':
    import argparse
    get_input = input
    if(sys.version_info[:2] <= (2, 7)):
        get_input = raw_input

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    if(sys.version_info[:2] <= (3, 2)):
        from configparser import SafeConfigParser
    else:
        from configparser import ConfigParser as SafeConfigParser

try:
    imp.find_module('requests')
    haverequests = True
    import requests
except ImportError:
    haverequests = False
    havemechanize = False
try:
    imp.find_module('mechanize')
    havemechanize = True
    import mechanize
except ImportError:
    havemechanize = False

try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

__program_name__ = "PyOpenCNAM"
__project__ = __program_name__
__project_url__ = "https://github.com/GameMaker2k/PyOpenCNAM"
__version_info__ = (1, 2, 4, "RC 1", 1)
__version_date_info__ = (2024, 10, 22, "RC 1", 1)
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[
    1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2)

if(__version_info__[4] != None):
    __version_date_plusrc__ = __version_date__ + \
        "-"+str(__version_date_info__[4])
if(__version_info__[4] == None):
    __version_date_plusrc__ = __version_date__
if(__version_info__[3] != None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(
        __version_info__[2])+" "+str(__version_info__[3])
if(__version_info__[3] == None):
    __version__ = str(
        __version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])

geturls_ua_pyopencnam_python = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(
    proname=__project__, prover=__version__, prourl=__project_url__)
if(platform.python_implementation() != ""):
    geturls_ua_pyopencnam_python_alt = "Mozilla/5.0 (compatible; {osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system(
    )+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp=platform.python_implementation(), pyver=platform.python_version(), proname=__project__, prover=__version__)
if(platform.python_implementation() == ""):
    geturls_ua_pyopencnam_python_alt = "Mozilla/5.0 (compatible; {osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system(
    )+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp="Python", pyver=platform.python_version(), proname=__project__, prover=__version__)

master_phone_number = "+16786318356"
master_account_sid = None
master_auth_token = None
master_service_level = "standard"
master_casing = "caps"
master_mobile = "location"
master_no_value = "unknown"
master_geo = "wire"
master_http_lib = "urllib"

master_opencnam_url_old = "https://api.opencnam.com/v3/phone/{phone_number_str}?account_sid={account_sid_str}&auth_token={auth_token_str}&format=json&service_level={service_level_str}&casing={casing_str}&mobile={mobile_str}&no_value={no_value_str}&geo={geo_str}"
master_opencnam_url = "https://api.opencnam.com/v3/phone/{phone_number_str}?format=json&service_level={service_level_str}&casing={casing_str}&mobile={mobile_str}&no_value={no_value_str}&geo={geo_str}"

if(os.path.exists("pyopencnam.ini") and os.path.isfile("pyopencnam.ini")):
    cfgparser = SafeConfigParser()
    cfgparser.read("pyopencnam.ini")
    master_phone_number = cfgparser.get("OpenCNAM", "phone_number")
    master_account_sid = cfgparser.get("OpenCNAM", "account_sid")
    if(len(master_account_sid) <= 0):
        master_account_sid = None
    master_auth_token = cfgparser.get("OpenCNAM", "auth_token")
    if(len(master_auth_token) <= 0):
        master_auth_token = None
    master_opencnam_url = cfgparser.get("OpenCNAM", "opencnam_url")
    master_service_level = cfgparser.get("OpenCNAM", "service_level")
    master_casing = cfgparser.get("OpenCNAM", "casing")
    master_mobile = cfgparser.get("OpenCNAM", "mobile")
    master_no_value = cfgparser.get("OpenCNAM", "no_value")
    master_geo = cfgparser.get("OpenCNAM", "geo")
    master_http_lib = cfgparser.get("OpenCNAM", "http_lib")

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description="Get cnam info from phone numbers from opencnam", conflict_handler="resolve", add_help=True)
    argparser.add_argument("-v", "--version", action="version",
                           version=__program_name__+" "+__version__)
    argparser.add_argument(
        "-p", "--phonenumber", default=master_phone_number, help="enter phone number to lookup")
    argparser.add_argument(
        "-a", "--accountsid", default=master_account_sid, help="enter account sid for lookup")
    argparser.add_argument(
        "-t", "--authtoken", default=master_auth_token, help="enter auth token for lookup")
    argparser.add_argument(
        "-s", "--servicelevel", default=master_service_level, help="enter service level for lookup")
    argparser.add_argument(
        "-o", "--opencnamurl", default=master_opencnam_url, help="enter url for lookup")
    argparser.add_argument(
        "-c", "--casing", default=master_opencnam_url, help="casing type for output vaule")
    argparser.add_argument(
        "-m", "--mobile", default=master_opencnam_url, help="output for mobile numbers")
    argparser.add_argument(
        "-n", "--novalue", default=master_opencnam_url, help="output for unknown numbers")
    argparser.add_argument(
        "-g", "--geo", default=master_opencnam_url, help="output for geo locations")
    argparser.add_argument("-h", "--httplib", default=master_http_lib,
                           help="select httplib to use for request")
    argparser.add_argument(
        "-i", "--input", action="store_false", help="get input from command prompt")
    getargs = argparser.parse_args()
    master_phone_number = getargs.phonenumber
    master_account_sid = getargs.accountsid
    master_auth_token = getargs.authtoken
    master_opencnam_url = getargs.opencnamurl
    master_service_level = getargs.servicelevel
    master_casing = getargs.casing
    master_mobile = getargs.mobile
    master_no_value = getargs.novalue
    master_geo = getargs.geo
    master_http_lib = getargs.httplib


def make_http_headers_from_dict_to_list(headers={'Referer': "https://www.opencnam.com/dashboard/delivery/query-tool", 'User-Agent': geturls_ua_pyopencnam_python_alt}):
    if isinstance(headers, dict):
        returnval = []
        if(sys.version[0] == "2"):
            for headkey, headvalue in headers.iteritems():
                returnval.append((headkey, headvalue))
        if(sys.version[0] >= "3"):
            for headkey, headvalue in headers.items():
                returnval.append((headkey, headvalue))
    elif isinstance(headers, list):
        returnval = headers
    else:
        returnval = False
    return returnval


def get_httplib_support(checkvalue=None):
    global haverequests, havemechanize
    returnval = []
    returnval.append("urllib")
    if(haverequests == True):
        returnval.append("requests")
    if(havemechanize == True):
        returnval.append("mechanize")
    if(not checkvalue == None):
        if(checkvalue == "urllib1" or checkvalue == "urllib2"):
            checkvalue = "urllib"
        if(checkvalue in returnval):
            returnval = True
        else:
            returnval = False
    return returnval


def query_cnam_info(phone_number=master_phone_number, account_sid=master_account_sid, auth_token=master_auth_token, opencnam_url=master_opencnam_url, service_level=master_service_level, casing=master_casing, mobile=master_mobile, no_value=master_no_value, geo=master_geo, httplibuse=master_http_lib):
    if(phone_number == None or account_sid == None or auth_token == None or service_level == None or (service_level != "standard" and service_level != "plus")):
        return False
    if(not get_httplib_support(httplibuse)):
        httplibuse = "urllib"
    if(httplibuse == "urllib"):
        opencnam_api_url = Request(opencnam_url.format(phone_number_str=phone_number, account_sid_str=account_sid, auth_token_str=auth_token,
                                   service_level_str=service_level, casing_str=casing, mobile_str=mobile, no_value_str=no_value, geo_str=geo))
        preb64_user_string = str(master_account_sid)+":"+str(master_auth_token)
        if(sys.version[0] == "2"):
            base64_user_string = base64.b64encode(preb64_user_string)
            opencnam_api_url.add_header(
                "Authorization", "Basic "+base64_user_string)
        if(sys.version[0] >= "3"):
            base64_user_string = base64.b64encode(preb64_user_string.encode())
            opencnam_api_url.add_header(
                "Authorization", "Basic "+base64_user_string.decode())
        opencnam_api_url.add_header(
            "User-Agent", geturls_ua_pyopencnam_python_alt)
        opencnam_api_url.add_header(
            "Referer", "https://www.opencnam.com/dashboard/delivery/query-tool")
        opencnam_api_data = urlopen(opencnam_api_url)
        outdata = json.load(opencnam_api_data)
    elif(httplibuse == "requests"):
        preb64_user_string = str(master_account_sid)+":"+str(master_auth_token)
        r_header = {}
        if(sys.version[0] == "2"):
            base64_user_string = base64.b64encode(preb64_user_string)
            r_header.update({'Authorization': base64_user_string})
        if(sys.version[0] >= "3"):
            base64_user_string = base64.b64encode(preb64_user_string.encode())
            r_header.update({'Authorization': base64_user_string.decode()})
        r_header.update({'User-Agent': geturls_ua_pyopencnam_python_alt})
        r_header.update(
            {'Referer': "https://www.opencnam.com/dashboard/delivery/query-tool"})
        opencnam_api_data = requests.get(opencnam_url.format(phone_number_str=phone_number, account_sid_str=account_sid, auth_token_str=auth_token,
                                         service_level_str=service_level, casing_str=casing, mobile_str=mobile, no_value_str=no_value, geo_str=geo), headers=r_header)
        outdata = opencnam_api_data.json()
    elif(httplibuse == "mechanize"):
        geturls_opener = mechanize.Browser()
        preb64_user_string = str(master_account_sid)+":"+str(master_auth_token)
        r_header = {}
        if(sys.version[0] == "2"):
            base64_user_string = base64.b64encode(preb64_user_string)
            r_header.update({'Authorization': base64_user_string})
        if(sys.version[0] >= "3"):
            base64_user_string = base64.b64encode(preb64_user_string.encode())
            r_header.update({'Authorization': base64_user_string.decode()})
        r_header.update({'User-Agent': geturls_ua_pyopencnam_python_alt})
        r_header.update(
            {'Referer': "https://www.opencnam.com/dashboard/delivery/query-tool"})
        r_header = make_http_headers_from_dict_to_list(r_header)
        geturls_opener.addheaders = r_header
        geturls_opener.set_handle_robots(False)
        print(r_header)
        opencnam_api_data = geturls_opener.open(opencnam_url.format(phone_number_str=phone_number, account_sid_str=account_sid, auth_token_str=auth_token,
                                                service_level_str=service_level, casing_str=casing, mobile_str=mobile, no_value_str=no_value, geo_str=geo))
        outdata = opencnam_api_data.json()
    else:
        outdata = None
    return outdata


if __name__ == '__main__':
    if(getargs.input == True):
        print(json.dumps(query_cnam_info(master_phone_number, master_account_sid, master_auth_token, master_opencnam_url,
              master_service_level, master_casing, master_mobile, master_no_value, master_geo, master_http_lib)))
    if(getargs.input == False):
        user_account_sid = get_input("enter account sid for lookup: ")
        if(len(user_account_sid) <= 0):
            user_account_sid = master_account_sid
        user_auth_token = get_input("enter auth token for lookup: ")
        if(len(user_auth_token) <= 0):
            user_auth_token = master_auth_token
        user_service_level = get_input("enter service level for lookup: ")
        if(len(user_service_level) <= 0):
            user_service_level = master_service_level
        user_phone_number = get_input("enter phone number to lookup: ")
        while(len(user_phone_number) > 0):
            print("\n")
            print(json.dumps(query_cnam_info(user_phone_number, user_account_sid, user_auth_token, master_opencnam_url,
                  user_service_level, master_casing, master_mobile, master_no_value, master_geo, master_http_lib)))
            print("\n")
            user_phone_number = get_input("enter phone number to lookup: ")
            if(len(user_phone_number) <= 0):
                break
