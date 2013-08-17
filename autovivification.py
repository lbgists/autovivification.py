#!/usr/bin/env python
# Collected and testing code written by Yu-Jie Lin

from __future__ import print_function

# http://code.activestate.com/recipes/537637/
# @ 2007-12-19 by Mirko Dziadzka
class auto_dict(dict):
    def __getitem__(self, key):
        return self.setdefault(key, self.__class__())


# http://code.activestate.com/recipes/537637/#c1
# @ 2007-??-?? by Ruslan Spivak
# http://ruslanspivak.com/2008/04/14/autovivication-and-y-combinator-in-python/
# @ 2008-04-14 by Ruslan Spivak -- recursive function
from collections import defaultdict

tree = lambda: defaultdict(tree)


# http://ruslanspivak.com/2008/04/14/autovivication-and-y-combinator-in-python/
# @ 2008-04-14 by Ruslan Spivak -- Y combinator
def Y(g):
    return ((lambda f: f(f))
            (lambda f:
                 g(lambda x: f(f)
                   (x))))

defdict = Y(lambda mk_dict:
                lambda x=None: defaultdict(lambda x=None: mk_dict(x)))


# http://ruslanspivak.com/2008/04/14/autovivication-and-y-combinator-in-python/#comment-87
# @ 2011-07-15 by Adam
Y2 = lambda g: ( lambda f: f(f) )( lambda f: g( lambda *args: f(f)(*args) ) )
defdict2 = Y2(lambda mk_dict: lambda: defaultdict(mk_dict))


# http://c2.com/cgi/wiki?AutoVivification
# @ 2006-11-11 by Bill Kelly
class AutoObject(object):
    def __init__(self):
        self.__store = {}


    def __getattr__(self, name):
        # automatically create objects accessed via an_auto_object.name
        # Only get to this if normal lookup failed
        obj = AutoObject()
        setattr(self, name, obj)
        return obj


    def __getitem__(self, name):
        # Automatically create objects accessed via [name] if they
        # don't exist already.
        return self.__store.setdefault(name, AutoObject())
 

# http://blogs.fluidinfo.com/terry/2012/05/26/autovivification-in-python-nested-defaultdicts-with-a-specific-final-type/#comment-546295185
# @ 2012-06-03 by Roman Evstifeev
class objdict(defaultdict):
    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return self.__getitem__(key)
           
    __setattr__ = lambda self, k, v: self.__setitem__(k,v)

objtree = lambda: objdict(objtree)


# http://blogs.fluidinfo.com/terry/2012/05/26/autovivification-in-python-nested-defaultdicts-with-a-specific-final-type/#comment-546295185
# @ 2012-06-03 by Roman Evstifeev
# @ 2013-08-16 by Yu-Jie Lin
objtree2 = lambda: type('objdict2', (defaultdict, ), dict(__getattr__=lambda self, k: self.__dict__[k] if k in self.__dict__ else self.__getitem__(k), __setattr__=lambda self, k, v: self.__setitem__(k,v)))(objtree2)


########################################

def set_values(t):

    assignments = '''\
        t[1][2][3] = 4
        t[1][2]['test'] = 6
        t['foo']['bar'] = 'foobar'
        t['foo'][123] = 456
        t.foo.bar = 'blah'
        t.foo[123] = 999
        t[1].foo.bar = 'xyz'
        t[1].foo.bar.xyz = 123
        t[1].foo['456'].bar = 'xyz'
        t[1].foo['456'][789] = 'xyz'
    '''.split('\n')

    for l in assignments:
        l = l.strip()
        print(l)
        try:
            exec(l)
        except Exception as e:
            print('ERROR', e)


def dd2dr(dd):
    '''defaultdict to dict recursively'''
    return dict(
        (k, dd2dr(v) if isinstance(v, defaultdict) else v)
        for k, v in dd.items()
    )


def main():

    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=1, width=1).pprint

    
    items = ('auto_dict', 'tree', 'defdict', 'defdict2', 'AutoObject',
             'objtree', 'objtree2')
    for I in items:
        print('{:=^79s}\n'.format(' %s ' % I))
        t = eval(I)()
        set_values(t)
        if I != 'AutoObject':
           pp(dd2dr(t))
        print()


if __name__ == '__main__':
    main()
