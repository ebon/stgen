#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys
import codecs
import logging
import traceback
from optparse import OptionParser
import settings as st
from main import OutputPage

def main():
    usage       = "usage: %prog [-p|g] -r dcrfile -t pagename"
    description = """Note :
    - you should be care options -p and -e are mutually exclusive
    """
    parser      = OptionParser(usage=usage, description=description)
    parser.add_option("-r", "--dcrfile",
                      action="store", dest="dcrfile",
                      help="")
    parser.add_option("-t", "--pagename",
                      action="store", dest="pagename",
                      help="")
    parser.add_option("-e", "--execute_generation", action="store_const",
                      const="exec_generation", dest="exec_generation",
                      help="")
    parser.add_option("-p", "--preview", action="store_const",
                      const="preview", dest="preview",
                      help="")

    try:
        (opt, args) = parser.parse_args()
        op = OutputPage(opt.dcrfile)

        if opt.preview:
            try:
                result = op.get_source(opt.pagename)
                print result.encode(st.CHACODE_STDOUT)
            except:
                logging.basicConfig(level=logging.ERROR,
                                    filename=st.ERROR_LOG_preview)
                logging.error(traceback.format_exc())
                result = 'error. :' + traceback.format_exc()
                print result
        elif opt.exec_generation:
            try:
                result = str(op.generate_page_all())
            except:
                logging.basicConfig(level=logging.ERROR,
                                    filename=st.ERROR_LOG_generation)
                logging.error(now + traceback.format_exc())
                result = 'error. please see: ' + st.ERROR_LOG_generation + traceback.format_exc()
            finally:
                print result.encode(st.CHACODE_STDOUT)

    except (IndexError, parser.error):
        usage(argv)
        return 1


if __name__ == "__main__":
    main()
