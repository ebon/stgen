# -*- coding:utf-8 -*-

import xml2dict
from lxml import etree

def xmlfile2str(xmlfile, enc):
    tree = etree.parse(xmlfile)
    return etree.tostring(tree, encoding=enc)

def xmlstr2dict(xml_str):
    dxml = xml2dict.XML2Dict()
    return dxml.fromstring(xml_str)

def xmlfile2dict(xmlfile, enc='utf-8'):
    """convert xml to dict with encoding
    >>> xmlfile = './testxml.xml'
    >>> xml_dict = myxml2dict(xmlfile, enc='utf-8')
    """
    tree = etree.parse(xmlfile)
    xml_str = etree.tostring(tree, encoding=enc)
    dxml = xml2dict.XML2Dict()
    return dxml.fromstring(xml_str)

if __name__ == '__main__':
    xmlfile = './sample-dcr.xml'
    xml_dict = xmlfile2dict(xmlfile, enc='utf-8')
