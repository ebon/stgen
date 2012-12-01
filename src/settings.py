# -*- coding: utf-8  -*-
import os, sys, re
from os.path import join
from jinja2 import Environment, FileSystemLoader

# Base directories
try: 
    EXE_DIR = os.path.abspath(os.path.dirname(__file__))
except NameError,err:
    EXE_DIR = os.getcwd()

USR_DIR = os.path.dirname(EXE_DIR)
TMPL_DIR = join(USR_DIR, 'templates/')
CSV_DIR = join(USR_DIR, 'import/')
ENV = Environment(loader=FileSystemLoader(TMPL_DIR))
OUTPUT_BASEDIR = join(USR_DIR, 'output/')

# Log files
ERROR_LOG_preview = join(USR_DIR, 'presentation/log/') + 'log_preview.txt'
ERROR_LOG_generation = join(USR_DIR, 'presentation/log/') + 'log_generation.txt'

CHACODE = 'euc-jp'
CHACODE_STDOUT = 'utf_8'
