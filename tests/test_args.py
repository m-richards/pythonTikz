#!/usr/bin/python

"""
Test to check when arguments of functions get changed.

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""

from pythontikz import (TikzPicture, TikzRectCoord, TikzNode,
                        TikzAnchor, TikzUserPath, TikzPathList, TikzPath,
                        TikzDraw,
                        TikzScope, TikzOptions, TikZLibrary,
                        TikzPolCoord, TikzArc,
                        TikzCalcCoord, TikZCalcScalar, Plot, Axis)

from pythontikz.positions import _TikzCalcImplicitCoord


def test_tikz():
    # PGFPlots
    t = TikzPicture(data=None)
    repr(t)

    a = Axis(data=None, options=None)
    repr(a)

    p = Plot(name=None, func=None, coordinates=None, error_bar=None,
             options=None)
    repr(p)

    opt = TikzOptions(None)
    repr(opt)

    scope = TikzScope(data=None)
    repr(scope)
    b = (0, 1)
    c = TikzRectCoord.from_str("(0,0)")
    c = TikzRectCoord(x=0, y=0, relative=False)
    d = c + b
    e = c - b
    f = b + c
    c.distance_to(d)
    repr(c)
    repr(d)
    repr(e)
    repr(f)

    g = TikzPolCoord(angle=225, radius=1, relative=False)
    repr(g)

    h = TikzCalcCoord(handle='handle', options=None, at=c, text=None)
    hh = h.get_handle()

    repr(h)
    repr(hh)

    # coordinate handle checks
    s = TikZCalcScalar(value=3.4)
    s.dumps()
    repr(s)
    # scalar multiplication of TikzCoordinateHandle
    z = s * hh
    repr(z)


    a = TikzAnchor(node_handle=None, anchor_name=None)
    repr(a)

    n = TikzNode(handle=None, options=None, at=None, text=None)
    repr(n)

    p = n.get_anchor_point("north")
    repr(p)

    p = n.get_anchor_point('_180')
    repr(p)

    p = n.west
    repr(p)

    up = TikzUserPath(path_type="edge", options=TikzOptions('bend right'))
    repr(up)

    pl = TikzPathList('(0, 1)', '--', '(2, 0)')
    pl.append((0.5, 0))
    repr(pl)

    pt = TikzPath(path=None, options=TikzOptions("->"))
    pt.append(TikzRectCoord(0, 1, relative=True))
    repr(pt)
    pt.dumps()

    pt = TikzPath(path=[n.west, 'edge', TikzRectCoord(0, 1, relative=True),
                        '--', TikzNode(handle='handle',
                                       at=TikzRectCoord(0, 2, ))])
    repr(pt)

    pt = TikzPath(path=pl, options=None)
    repr(pt)

    try:
        TikzPath(path='z')
        raise Exception
    except TypeError:
        pass

    opt = TikzOptions('use Hobby shortcut')
    opt.append_positional('close=true')

    pt = TikzDraw(path=[TikzRectCoord(0, 0), '..', TikzRectCoord(1, 1), '..',
                        TikzRectCoord(1, 2)], options=opt)

    dr = TikzDraw(path=None, options=None)
    repr(dr)

    tl = TikZLibrary(name='', options=None)
    repr(tl)

    a = TikzArc(start_ang=0, finish_ang=300, radius=3,
                force_far_direction=True)
    a2 = TikzArc(start_ang=300, finish_ang=0, radius=3,
                 force_far_direction=True)
    a3 = TikzArc.from_str("(300:200:2)")
    repr(a)
    repr(a2)
    repr(a3)

    d1 = TikzDraw(path=[g, 'arc', a, '--', g])
    repr(d1)

    impl = _TikzCalcImplicitCoord(c, '+', c)

