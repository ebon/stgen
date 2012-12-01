# -*- coding: utf-8  -*-
#
# Custome functions and Global valiables used in a jinja's templates.
# 

import csv
import os, re, sys
import utils.tmputil as ut
import utils.xmlutil as xut
import settings as st

################################################################################
# Global values 
################################################################################

################################################################################
# Filter funcs
################################################################################
def unidict_encoder(d, enc):
    return dict([(k.encode(enc), v.encode(enc)) for k,v in d.items()])

EUC_TABLE = {
    u'\uff0d' : u'&#xff0d;',  # zenkaku haifun
    u'\uff5e' : u'&#12316;',  # nami dash
    }
def eucconverter(d):
    try:
        f = ut.multiple_replace_cl(EUC_TABLE)
        return dict([(k, f(v)) for k,v in d.items()])
    except TypeError:
        return d

def myread_csvdata(csv_file, dec='cp932'):
    """Put csvdata into dictionary-list of the each records."""
    csv_path = st.CSV_DIR + os.path.basename(csv_file)
    items_dict = ut.csvread(csv_path, dec=dec, enc='utf_8')
    items_dict_uni = [eucconverter(ut.dict_unicoder(d, 'utf_8'))
                      for d in items_dict]
    return items_dict_uni

def mysorted(dictlist, cmpkey='', reverse=False):
    """wrapper for build-in sorted"""
    return sorted(dictlist,
                  cmp=lambda x,y:cmp(int(x[cmpkey]), int(y[cmpkey])),
                  reverse=reverse)

################################################################################
# Add Global values & Filter:
# - Each ones should be named with started the special prediction.
#   - filater funcs : '^my'
#   - global values: '^our'
################################################################################
globalvals = dict([(k,v) for k,v in locals().items() if re.match('^our', k)])
st.ENV.globals.update(**globalvals)
filterfuncs = dict([(k,v) for k,v in locals().items() if re.match('^my', k)])
st.ENV.filters.update(**filterfuncs)


################################################################################
# Test
################################################################################
if __name__ == "__main__":
    # xml's test with actual templates
    dcrpath = '../data/_test/test'
    dcrdict = xut.xmlfile2dict(dcrpath, enc='utf-8')
    pagename = 'fx_pair_pc'
    outputsetting_tmpl = st.ENV.get_template('output_settings.tmpl')
    outputsettings = outputsetting_tmpl.render(dcrpath=dcrpath,
                                               **dcrdict)
    test_tmpl = st.ENV.get_template(outputsettings[pagename]['tmpl'])
    test_source = test_tmpl.render(**dcrdict)
    print test_source

    # On csv's own test
    csvf = '../import/fxtable.csv'
    csvd = myread_csvdata(csvf, dec='cp932')
    csvs = mysorted(csvd, cmpkey='list_order')
