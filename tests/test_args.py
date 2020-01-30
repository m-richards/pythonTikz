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

    bool(c == (1, 1))
    bool(c == TikzRectCoord(1, 1))
    bool(TikzRectCoord(1, 1, relative=True) == (1, 1))
    bool(TikzRectCoord(1, 1, relative=False) == (1, 1))
    bool(TikzRectCoord(1, 1, relative=True) == TikzRectCoord(1,
                                                             1,
                                                             relative=False))
    t = TikzRectCoord(1, 1)
    # check invalid operations on coordinate fails
    case_list = [lambda: t == "test", lambda: t == object(), lambda: t + 42]
    for fail_case in case_list:
        try:
            fail_case()
            raise Exception
        except TypeError:
            pass
    g = TikzPolCoord(angle=225, radius=1, relative=False)
    g2 = TikzPolCoord(angle=225, radius=1, relative=True)
    try:
        TikzPolCoord(225, -5)
        raise Exception
    except ValueError:
        pass

    h = TikzCalcCoord(handle='handle', options=None, at=c, text=None)
    h2 = TikzCalcCoord(handle=None, options=None, at=c, text="text")
    hh = h.get_handle()
    # CoordinateVariables don't support arithmetic:
    o = object()
    for to_fail in [lambda: h - o, lambda: o * h]:
        try:
            to_fail()
            raise Exception
        except TypeError:
            pass

    repr(g)
    repr(g2)
    repr(h)
    repr(h2)
    h2.dumps()
    repr(hh)
    lst = [b, c, g, hh]
    for i in lst:
        for j in lst:
            if not (isinstance(i, tuple) and isinstance(j, tuple)):
                tmp1 = i + j
                tmp2 = (j + i)
                tmp3 = (i-j)
                tmp4 = (j-i)
                repr(tmp1)
                repr(tmp2)
                repr(tmp3)
                repr(tmp4)

        # test expected to fail
        try:
            i + h
            raise Exception
        except TypeError:
            pass

    # check invalid arithmetic with handles
    checks = [lambda: hh + object(), lambda: hh - object(),
              lambda: hh * object]
    for i in checks:
        try:
            i()
            raise Exception
        except TypeError:
            pass

    # coordinate handle checks
    s = TikZCalcScalar(value=3.4)
    s.dumps()
    repr(s)
    # scalar multiplication of TikzCoordinateHandle
    z = s * hh
    repr(z)

    # test expected to fail
    try:
        g = TikzRectCoord(0, 1, relative=True) + \
            TikzRectCoord(1, 0, relative=False)
        repr(g)
        raise Exception
    except ValueError:
        pass

    a = TikzAnchor(node_handle=None, anchor_name=None)
    repr(a)

    n = TikzNode(handle=None, options=None, at=None, text=None)
    repr(n)

    try:
        TikzNode(handle=None, options=None, at=object())
        raise Exception
    except TypeError:
        pass

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

    # generate a failure, illegal start
    try:
        pl = TikzPathList('--', '(0, 1)')
        raise Exception
    except TypeError:
        pass

    # fail with illegal path type
    try:
        pl = TikzPathList('(0, 1)', 'illegal', '(0, 2)')
        raise Exception
    except ValueError:
        pass

    # fail with path after path
    try:
        pl = TikzPathList('(0, 1)', '--', '--')
        raise Exception
    except ValueError:
        pass

    # other type of failure: illegal identifier after path
    try:
        pl = TikzPathList('(0, 1)', '--', 'illegal')
        raise Exception
    except (ValueError, TypeError):
        pass

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

    try:
        TikzArc.from_str("zzzz")
        raise Exception
    except ValueError:
        pass

    d1 = TikzDraw(path=[g, 'arc', a, '--', g])
    d2 = TikzDraw(path=[g, 'arc', "(300:200:2)", '--', g])
    repr(d1)
    repr(d2)
    case_list = [
        # 'arc' should be followed by TikZArc incorrect type
        (lambda: TikzDraw(path=[g, 'arc', g]), TypeError),
        # 'arc' should be followed by TikZArc  - string parsing throws
        # valueerror
        (lambda: TikzDraw(path=[g, 'arc', 'z']), ValueError)]
    for to_fail, err_type in case_list:
        try:
            to_fail()
            raise Exception
        except err_type:
            pass
    # test implicit coordinate exceptions (not that a user should see these)
    orig = TikzRectCoord(0, 0)
    impl = _TikzCalcImplicitCoord(orig, '+', orig)
    case_list = [
        # invalid operator (not + or -)
        ((orig, 'z'), ValueError),
        # invalid operator following scalar
        ((3, 'z'), ValueError),
        # can't TikZCoordinateVariable - should use handle
        ((TikzCalcCoord(), '+', orig), TypeError),
        # invalid string should throw typeError
        (("z", '+', 'z'), TypeError),
        # invalid type should throw typeError (outer context converts to Val
        ((orig, '+', object()), ValueError),
        # nested TikZImplicit operator should fail with invalid args
        ((impl, '-', 'z'), ValueError),
        # invalid +/- operator not of type string
        ((orig, object(), orig), ValueError),
    ]
    for fail_case, err_type in case_list:
        try:
            _TikzCalcImplicitCoord(*fail_case)
            raise Exception
        except err_type:
            pass

    # pass cases
    case_list = [(3, '*', orig), ('(0,0)', '+', (0, 0)),
                 (TikzNode(at=orig, handle='h1'), '+', (0, 0)),
                 (impl, '-', impl)]

    for case in case_list:
        tmp = _TikzCalcImplicitCoord(*case)
        repr(tmp)

    tmp2 = impl + orig
    tmp3 = impl + impl
    tmp4 = impl - impl
    tmp5 = impl - orig
    try:
        impl - "z"
        raise Exception
    except TypeError:
        pass
    repr(tmp2)
    repr(tmp3)
    repr(tmp4)
    repr(tmp5)
