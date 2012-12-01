#!/usr/local/bin/python
# -*- coding: utf-8  -*-
import os, sys
from nose.tools import ok_, eq_

sys.path.append(os.pardir)
import settings as st
from main import OutputPage
from test_output_settings import sample_output_settings

test_dcr = os.path.abspath('../../data/_test/test')
test_pagename = 'fx_top_pc'

test_op = OutputPage(test_dcr)
test_pagepath = st.OUTPUT_BASEDIR + test_op.outputsetting[test_pagename]['outputpath']

def test_outputsetting():
    outputsetting = test_op.outputsetting
    eq_(outputsetting, sample_output_settings)

test_pagesource = test_op.get_source(test_pagename)

def test_generate_page():
    result = test_op.generate_page(test_pagename)

def test_generate_page_all():
    results = test_op.generate_page_all()
    expected_results = [
        (u'fx_fee_pc', 'success'), (u'fx_service_sp', 'success'),
        (u'fx_top_pc', 'success'), (u'fx_leverage_sp', 'success'),
        (u'fx_swap_pc', 'success'), (u'fx_point_pc', 'success'),
        (u'fx_support_sp', 'success'), (u'fx_trust_pc', 'success'),
        (u'fx_fee_sp', 'success'), (u'fx_pair_pc', 'success'),
        (u'fx_point_sp', 'success'), (u'fx_support_pc', 'success'),
        (u'fx_trust_sp', 'success'), (u'fx_pair_sp', 'success'),
        (u'fx_swap_sp', 'success'), (u'fx_top_sp', 'success'),
        (u'fx_leverage_pc', 'success'), (u'fx_service_pc', 'success')
        ]

    eq_(results, expected_results)
