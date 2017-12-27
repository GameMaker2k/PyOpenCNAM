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
    $FileInfo: pyopencnam-ui.py - Last Update: 12/23/2017 Ver. 1.0.0 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import os, sys, json, pyopencnam, platform;

try:
    from ConfigParser import SafeConfigParser;
except ImportError:
    from configparser import SafeConfigParser;

try:
    import Tkinter, tkMessageBox, tkFileDialog, tkColorChooser, tkSimpleDialog;
except ImportError:
    import tkinter as Tkinter;
    from tkinter import messagebox as tkMessageBox;
    from tkinter import filedialog as tkFileDialog;
    from tkinter import colorchooser as tkColorChooser;
    from tkinter import simpledialog as tkSimpleDialog;

try:
    from Tkinter import *;
except ImportError:
    from tkinter import *;

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

geturls_ua_pyopencnam_python = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(proname=__project__, prover=__version__, prourl=__project_url__);
if(platform.python_implementation()!=""):
    geturls_ua_pyopencnam_python_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp=platform.python_implementation(), pyver=platform.python_version(), proname=__project__, prover=__version__);
if(platform.python_implementation()==""):
    geturls_ua_pyopencnam_python_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp="Python", pyver=platform.python_version(), proname=__project__, prover=__version__);

master_phone_number = "+16786318356";
master_account_sid = None;
master_auth_token = None;
master_service_level = "standard";

if(os.path.exists("pyopencnam.ini") and os.path.isfile("pyopencnam.ini")):
    cfgparser = SafeConfigParser();
    cfgparser.read("pyopencnam.ini");
    master_phone_number = cfgparser.get("OpenCNAM", "phone_number");
    master_account_sid = cfgparser.get("OpenCNAM", "account_sid");
    if(len(master_account_sid)<=0):
        master_account_sid = None;
    master_auth_token = cfgparser.get("OpenCNAM", "auth_token");
    if(len(master_auth_token)<=0):
        master_auth_token = None;
    master_service_level = cfgparser.get("OpenCNAM", "service_level");

def QueryCNAM():
    queryresult.delete(0.0, END);
    opencnam_queryresult = pyopencnam.query_cnam_info(phonenumber.get(), accountsid.get(), authtoken.get(), servicelevel.get(ACTIVE));
    print(opencnam_queryresult);
    opencnam_result = "{\n  \"name\": \""+str(opencnam_queryresult['name'])+"\",\n  \"number\": \""+str(opencnam_queryresult['number'])+"\",\n  \"price\": "+str(opencnam_queryresult['price'])+",\n  \"uri\": \""+str(opencnam_queryresult['uri'])+"\"\n}\n";
    queryresult.insert(END, opencnam_result);
    return True;

root = Tk();
root.geometry("400x400");
root.resizable(width=False, height=False);
root.title(str(__program_name__)+" Query Tool "+str(__version__));
root.iconbitmap('pyopencnam-16x.ico');

phonenumber_label = Label(root, text="Phone Number", height=1);
phonenumber_label.pack(side=TOP, anchor="w");
phonenumber = Entry(root, width=40);
phonenumber.pack(side=TOP, anchor="w");
phonenumber.insert(END, master_phone_number);

accountsid_label = Label(root, text="Account SID", height=1);
accountsid_label.pack(side=TOP, anchor="w");
accountsid = Entry(root, width=40);
accountsid.pack(side=TOP, anchor="w");
accountsid.insert(END, master_account_sid);

authtoken_label = Label(root, text="Auth Token", height=1);
authtoken_label.pack(side=TOP, anchor="w");
authtoken = Entry(root, width=40);
authtoken.pack(side=TOP, anchor="w");
authtoken.insert(END, master_auth_token);

service_level = reversed(["standard", "plus"]);
servicelevel_label = Label(root, text="Service Level", height=1);
servicelevel_label.pack(side=TOP, anchor="w");
servicelevel = Listbox(root, width=40, height=2);
for item in service_level:
    servicelevel.insert(0, item);
servicelevel.pack(side=TOP, anchor="w");
if(master_service_level=="standard"):
    servicelevel.select_set(0);
elif(master_service_level=="plus"):
    servicelevel.select_set(1);
else:
    servicelevel.select_set(0);

button = Button(root, text="Run CNAM Query", command=QueryCNAM)
button.pack(pady=20, padx = 20)

queryresult_label = Label(root, text="Query Result", height=1);
queryresult_label.pack(side=TOP, anchor="w");
queryresult = Text(root, height=8, width=50);
queryresult.pack(side=TOP, anchor="w");
queryresult.delete(0.0, END);

root.mainloop();
