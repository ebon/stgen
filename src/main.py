#!/usr/local/bin/python
# -*- coding: utf-8  -*-
import os, re, sys
import datetime
import json
import logging
import traceback
import utils.tmputil as ut
import utils.xmlutil as xut
import settings as st
import myfilters


class OutputPage(object):
    """The factory of main functions with a given dcrpath."""
    def __init__(self, dcrpath, settings=st):
        self.dcrpath = dcrpath
        self.dcrdict = xut.xmlfile2dict(self.dcrpath, enc='utf-8')
        self.st = settings

    @property
    def outputsetting(self):
        """Converted dictionary data of 'output_settings.tmpl'"""
        outputsetting_tmpl = self.st.ENV.get_template('output_settings.tmpl')
        outputsetting_source = outputsetting_tmpl.render(dcrpath=self.dcrpath,
                                                         **self.dcrdict)
        return json.loads(outputsetting_source)

    @property
    def outputpages(self): return self.outputsetting.keys()

    def get_source(self, pagename):
        tmpl = self.st.ENV.get_template(self.outputsetting[pagename]['tmpl'])
        source = tmpl.render(**self.dcrdict)
        return source

    def generate_page(self, pagename):
        source = self.get_source(pagename)
        outputpath = st.OUTPUT_BASEDIR + self.outputsetting[pagename]['outputpath']
        ut.write_file(outputpath, source.encode(st.CHACODE), mkdir=True)

    def generate_page_all(self):
        """Generate all pages contained in 'output_settings.tmpl'"""
        result = []
        for pagename in self.outputpages:
            try:
                self.generate_page(pagename)
            except:
                now = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
                logging.basicConfig(level=logging.ERROR,
                                    filename=st.ERROR_LOG_generation)
                logging.error("\n[" + now + "]\n" + traceback.format_exc())
                error_msg = pagename + traceback.format_exc()
                result.append((pagename, 'error'))
            else:
                result.append((pagename, 'success'))

        return result
