#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.
    Copyright 2016 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2016 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski
    $FileInfo: pyopencnam.py - Last Update: 12/23/2017 Ver. 1.0.0 RC 1 - Author: cooldude2k $
'''

from __future__ import print_function;
import os, sys, json;

if __name__ == '__main__':
    import argparse;
    get_input = input;
    if(sys.version_info[:2] <= (2, 7)):
        get_input = raw_input;

try:
    from urllib2 import urlopen, Request;
except ImportError:
    from urllib.request import urlopen, Request;

__program_name__ = "PyOpenCNAM";
__project__ = __program_name__;
__project_url__ = "https://github.com/GameMaker2k/PyOpenCNAM";
__version_info__ = (1, 0, 0, "RC 1", 1);
__version_date_info__ = (2017, 12, 23, "RC 1", 1);
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2);

if(__version_info__[4]!=None):
    __version_date_plusrc__ = __version_date__+"-"+str(__version_date_info__[4]);
if(__version_info__[4]==None):
    __version_date_plusrc__ = __version_date__;
if(__version_info__[3]!=None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

master_phone_number = "+16786318356";
master_account_sid = None;
master_auth_token = None;
master_service_level = "standard";
master_opencnam_url = "https://api.opencnam.com/v3/phone/{phone_number_str}?account_sid={account_sid_str}&auth_token={auth_token_str}&format=json&&service_level={service_level_str}";

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get cnam info from phone numbers from opencnam", conflict_handler="resolve", add_help=True);
    parser.add_argument("-v", "--version", action="version", version=__program_name__+" "+__version__);
    parser.add_argument("-p", "--phonenumber", default=master_phone_number, help="enter phone number to lookup");
    parser.add_argument("-a", "--accountsid", default=master_account_sid, help="enter account sid for lookup");
    parser.add_argument("-t", "--authtoken", default=master_auth_token, help="enter auth token for lookup");
    parser.add_argument("-s", "--servicelevel", default=master_service_level, help="enter service level for lookup");
    parser.add_argument("-i", "--input", action="store_false", help="get input from command prompt");
    getargs = parser.parse_args();
    master_phone_number = getargs.phonenumber;
    master_account_sid = getargs.accountsid;
    master_auth_token = getargs.authtoken;
    master_service_level = getargs.servicelevel;

def query_cnam_info(phone_number = master_phone_number, account_sid = master_account_sid, auth_token = master_auth_token, service_level = master_service_level):
    global master_account_sid, master_auth_token;
    if(phone_number==None or account_sid==None or auth_token==None or service_level==None or (service_level!="standard" and service_level!="plus")):
        return False;
    opencnam_api_url = Request(master_opencnam_url.format(phone_number_str = phone_number, account_sid_str = account_sid, auth_token_str = auth_token, service_level_str = service_level));
    opencnam_api_data = urlopen(opencnam_api_url);
    return json.load(opencnam_api_data);

if __name__ == '__main__':
    if(getargs.input==True):
        print(json.dumps(query_cnam_info(master_phone_number, master_account_sid, master_auth_token, master_service_level)));
    if(getargs.input==False):
        user_account_sid = get_input("enter account sid for lookup: ");
        if(len(user_account_sid)<=0):
            user_account_sid = master_account_sid;
        user_auth_token = get_input("enter auth token for lookup: ");
        if(len(user_auth_token)<=0):
            user_auth_token = master_auth_token;
        user_service_level = get_input("enter service level for lookup: ");
        if(len(user_service_level)<=0):
            user_service_level = master_service_level;
        user_phone_number = get_input("enter phone number to lookup: ");
        while(len(user_phone_number)>0):
            print("\n");
            print(json.dumps(query_cnam_info(user_phone_number, user_account_sid, user_auth_token, user_service_level)));
            print("\n");
            user_phone_number = get_input("enter phone number to lookup: ");
            if(len(user_phone_number)<=0):
                break;
