# -*- coding: utf-8  -*-
import re, os, sys, csv
from functools import partial


def extract_noblankitems(d):
    """extract items except the item has a blank strings"""
    return dict([(k, v) for k, v in d.items() if not v == ''])


def mapfilter(predicate, ls):
    """Return both list with predicate result,
    1. predicate is true
    2. predicate is false
    * I'd like to do this at one-list-search path.
    >>> a = [5,3,6,1,4,8]
    >>> mapfilter(lambda x: x > 3, a)
    ([5, 6, 4, 8], [3, 1])
    """
    true_ls, false_ls = [], []
    for l in ls:
        if predicate(l):
            true_ls.append(l)
        else:
            false_ls.append(l)
    return true_ls, false_ls


def take(n, iterable):
    "Return first n items of the iterable as a list"
    from itertools import islice
    return list(islice(iterable, n))


def flatten(x):
    """flatten(sequence) -> list
    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).
    
    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
    """
    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if isinstance(el, list):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def dict_encoder(d, decodeing, encoding):
    return dict([(unicode(k, decodeing).encode(encoding),
                  unicode(v, decodeing).encode(encoding)) for k,v in d.items()])

def unidict_encoder(d, enc):
    return dict([(k.encode(enc), v.encode(enc)) for k,v in d.items()])

def dict_unicoder(d, encoding):
    return dict([(unicode(k), unicode(v, encoding)) for k,v in d.items()])


def update_dict(target, source):
    """ Return updated dictionary without destructive method.
    >>> d = {'id':1,'name':'hoge',}
    >>> update_dict(d, {'name':'fuga', 'size':'big'})
    {'size': 'big', 'id': 1, 'name': 'fuga'}
    >>> d
    {'id': 1, 'name': 'hoge'} # unchanged 
    """
    d = target.copy()
    d.update(source)
    return d


def dictsplit_bykey(dictionary, k, separater=None):
    """
    porpose : make copy dicts with given key contaied a delimiter.
    contract: f :: dict -> key --> [dict]
    example :
    >>> d = {'genre':['cd', 'dvd'], 'other':'otherelement'}
    >>> dictsplit_bykey(d, 'genre')
    {'genre':'cd', 'other':'otherelement'}, {'genre':'dvd', 'other':'otherelement'}
    """
    from itertools import repeat
    d = dictionary.copy()
    if separater: d.update(genre=d[k].split(separater))
    dl = [r for r in repeat(d, len(d[k]))]
    new = [update_dict(r, {k:r[k][i]}) for i,r in enumerate(dl)]
    return new


def groupby_list(iterable, key=None):
    """ wrap for itertools.groupby to preserve iterable object as a list.
        f(iterable, keyfunc) --> [(key,[groups])]
        * this is just for applying list() from groupby result.
    """ 
    from itertools import groupby
    return [(key, list(group)) for key,group in groupby(iterable, key)]


def csvread(file, dec='cp932', enc='utf_8'):
    """wrapper for csv.DictReader with encoding."""
    f = csv.DictReader(open(file, 'r'))
    rows = [dict_encoder(r, dec, enc) for r in f]
    return rows


def csvwrite_header(file, rows, filednames, mode="w"):
    """wraper for csv.DictWriter to write with HEADER."""
    header = dict([(v,v) for v in filednames])
    rows.insert(0, header)
    with open(file, mode) as f:
        writer = csv.DictWriter(f, filednames)
        writer.writerows(rows)


def sub_dict(somedict, somekeys, default=None):
    """Extract the subset of dict with given keys
    * un-distractively
    >>> d = {'a':5, 'b':6, 'c':7}
    >>> sub_dict(d, ['a', 'b'])
    {'a': 5, 'b': 6}
    >>> d
    {'a':5, 'b':6, 'c':7}
    """
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])


def keyslist2dict(keys, datas):
    """Return dict from key&data list.
    >>> datas = [('filea', 100), ('fileb', 80)]
    >>> keys = ('filename', 'size')
    >>> keyslist2dict(keys,  datas)
    [{'size': 100, 'filename': 'filea'}, {'size': 80, 'filename': 'fileb'}]
    """
    return [dict(zip(keys, l)) for l in datas]


def dict_ls2dict_withkey(key, dict_ls):
    """
    dictのlistを、あるkeyのvalueを新たなkeyとしたdictにする
    dict_ls2dict_withkey
    porpose : roll up each dict with given key common among the dicts.
    contract: f :: key -> [dict] --> {key:dict}
    example :
    >>> d_ls = [{'id':'1', 'b':'2'}, {'id':'3', 'b':'4'}]
    >>> dict_ls2dict_withkey('id', d_ls)
    {'1': {'id': '1', 'b': '2'}, '3': {'id': '3', 'b': '4'}}
    """
    return dict([(d[key], d) for d in dict_ls])


def write_file(filepath, data, mode='w', mkdir=True):
    """wrapper for open and write to file."""
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        if mkdir:
            os.makedirs(dirname)
        else:
            return "No such directory", dirname
    with open(filepath, mode=mode) as f:
        f.write(data)


class dict2obj(object):
    def __init__(self, d):
        self.__dict__['d'] = d
        
        def __getattr__(self, key):
            value = self.__dict__['d'][key]
            if type(value) == type({}):
                return dict2obj(value)
            
            return value


def list_reindex(x, ls):
    """Return the index in the list of the first item
    whose value is matched the patterns."""
    for i, ele in enumerate(ls):
        if re.match(ele, x):
            return i
    return i + 1

cmp_list_reindex = lambda ls, x, y: cmp(list_reindex(x, ls), list_reindex(y, ls))

def sort_dict_keyorder(d, keyorder_cond):
    """Retrun the dict sorted with the given key-order list.
    - those are alfabetical order if the items matched with the same regex pattern.
    - it is put to the last if there is no such item.
    >>> d = dict(bob='b', tito='t', jimmy='j', tarou='o', zach='z', adpage_a='a')
    >>> keyorder_cond = ('jimmy', 'bob', 'tito', r'ad.*', r'p.*')
    >>> sort_dict_keyorder(d, keyorder_cond)
    [('jimmy', 'j'), ('bob', 'b'), ('tito', 't'), ('adpage_a', 'a'), ('tarou', 'o')]
    """
    cmp_order_cond = partial(cmp_list_reindex, keyorder_cond)
    d_sorted = sorted(d.items(), lambda x,y: cmp_order_cond(x[0],y[0]))
    return d_sorted


def multiple_replace_cl(*args, **kwds):
    """
    porpose: replace multiple texts with doing one-path
             with closure base.
             for reusing replace-dict.
    example:
    text  = "Larry Wall is the creator of Perl"
    adict = {"Larry Wall":"Guido van Rossum", "Perl":"Python"}

    >>> transrate = multiple_replace_cl(adict) # make replace func.
    >>> transrate(text)
    "Guido van Rossum is the creator of Python"
    """
    adict = dict(*args, **kwds)
    rx = re.compile('|'.join(map(re.escape,adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    def xlat(text):
        return rx.sub(one_xlat, text)
    return xlat
