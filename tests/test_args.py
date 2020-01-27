#!/usr/bin/python

"""
Test to check when arguments of functions get changed.

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""

from pythontikz import (TikZ, TikZCoordinate, TikZNode,
                        TikZNodeAnchor, TikZUserPath, TikZPathList, TikZPath,
                        TikZDraw,
                        TikZScope, TikZOptions, TikZLibrary,
                        TikZPolarCoordinate, TikZArc,
                        TikZCoordinateVariable, TikZCalcScalar, Plot, Axis)

from pythontikz.tikz import _TikZCoordinateImplicitCalculation


def test_tikz():
    # PGFPlots
    t = TikZ(data=None)
    repr(t)

    a = Axis(data=None, options=None)
    repr(a)

    p = Plot(name=None, func=None, coordinates=None, error_bar=None,
             options=None)
    repr(p)

    opt = TikZOptions(None)
    repr(opt)

    scope = TikZScope(data=None)
    repr(scope)
    b = (0, 1)
    c = TikZCoordinate.from_str("(0,0)")
    c = TikZCoordinate(x=0, y=0, relative=False)
    d = c + b
    e = c - b
    f = b + c
    c.distance_to(d)
    repr(c)
    repr(d)
    repr(e)
    repr(f)

    bool(c == (1, 1))
    bool(c == TikZCoordinate(1, 1))
    bool(TikZCoordinate(1, 1, relative=True) == (1, 1))
    bool(TikZCoordinate(1, 1, relative=False) == (1, 1))
    bool(TikZCoordinate(1, 1, relative=True) == TikZCoordinate(1,
                                                               1,
                                                               relative=False))
    t = TikZCoordinate(1, 1)
    # check invalid operations on coordinate fails
    case_list = [lambda: t == "test", lambda: t == object(), lambda: t + 42]
    for fail_case in case_list:
        try:
            fail_case()
            raise Exception
        except TypeError:
            pass
    g = TikZPolarCoordinate(angle=225, radius=1, relative=False)
    g2 = TikZPolarCoordinate(angle=225, radius=1, relative=True)
    try:
        TikZPolarCoordinate(225, -5)
        raise Exception
    except ValueError:
        pass

    h = TikZCoordinateVariable(handle='handle', options=None, at=c, text=None)
    h2 = TikZCoordinateVariable(handle=None, options=None, at=c, text="text")
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
        g = TikZCoordinate(0, 1, relative=True) + \
            TikZCoordinate(1, 0, relative=False)
        repr(g)
        raise Exception
    except ValueError:
        pass

    a = TikZNodeAnchor(node_handle=None, anchor_name=None)
    repr(a)

    n = TikZNode(handle=None, options=None, at=None, text=None)
    repr(n)

    try:
        TikZNode(handle=None, options=None, at=object())
        raise Exception
    except TypeError:
        pass

    p = n.get_anchor_point("north")
    repr(p)

    p = n.get_anchor_point('_180')
    repr(p)

    p = n.west
    repr(p)

    up = TikZUserPath(path_type="edge", options=TikZOptions('bend right'))
    repr(up)

    pl = TikZPathList('(0, 1)', '--', '(2, 0)')
    pl.append((0.5, 0))
    repr(pl)

    # generate a failure, illegal start
    try:
        pl = TikZPathList('--', '(0, 1)')
        raise Exception
    except TypeError:
        pass

    # fail with illegal path type
    try:
        pl = TikZPathList('(0, 1)', 'illegal', '(0, 2)')
        raise Exception
    except ValueError:
        pass

    # fail with path after path
    try:
        pl = TikZPathList('(0, 1)', '--', '--')
        raise Exception
    except ValueError:
        pass

    # other type of failure: illegal identifier after path
    try:
        pl = TikZPathList('(0, 1)', '--', 'illegal')
        raise Exception
    except (ValueError, TypeError):
        pass

    pt = TikZPath(path=None, options=TikZOptions("->"))
    pt.append(TikZCoordinate(0, 1, relative=True))
    repr(pt)
    pt.dumps()

    pt = TikZPath(path=[n.west, 'edge', TikZCoordinate(0, 1, relative=True),
                        '--', TikZNode(handle='handle',
                                       at=TikZCoordinate(0, 2, ))])
    repr(pt)

    pt = TikZPath(path=pl, options=None)
    repr(pt)

    try:
        TikZPath(path='z')
        raise Exception
    except TypeError:
        pass

    opt = TikZOptions('use Hobby shortcut')
    opt.append_positional('close=true')

    pt = TikZDraw(path=[TikZCoordinate(0, 0), '..', TikZCoordinate(1, 1), '..',
                        TikZCoordinate(1, 2)], options=opt)

    dr = TikZDraw(path=None, options=None)
    repr(dr)

    tl = TikZLibrary(name='', options=None)
    repr(tl)

    a = TikZArc(start_ang=0, finish_ang=300, radius=3,
                force_far_direction=True)
    a2 = TikZArc(start_ang=300, finish_ang=0, radius=3,
                 force_far_direction=True)
    a3 = TikZArc.from_str("(300:200:2)")
    repr(a)
    repr(a2)
    repr(a3)

    try:
        TikZArc.from_str("zzzz")
        raise Exception
    except ValueError:
        pass

    d1 = TikZDraw(path=[g, 'arc', a, '--', g])
    d2 = TikZDraw(path=[g, 'arc', "(300:200:2)", '--', g])
    repr(d1)
    repr(d2)
    case_list = [
        # 'arc' should be followed by TikZArc incorrect type
        (lambda: TikZDraw(path=[g, 'arc', g]), TypeError),
        # 'arc' should be followed by TikZArc  - string parsing throws
        # valueerror
        (lambda: TikZDraw(path=[g, 'arc', 'z']), ValueError)]
    for to_fail, err_type in case_list:
        try:
            to_fail()
            raise Exception
        except err_type:
            pass
    # test implicit coordinate exceptions (not that a user should see these)
    orig = TikZCoordinate(0, 0)
    impl = _TikZCoordinateImplicitCalculation(orig, '+', orig)
    case_list = [
        # invalid operator (not + or -)
        ((orig, 'z'), ValueError),
        # invalid operator following scalar
        ((3, 'z'), ValueError),
        # can't TikZCoordinateVariable - should use handle
        ((TikZCoordinateVariable(), '+', orig), TypeError),
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
            _TikZCoordinateImplicitCalculation(*fail_case)
            raise Exception
        except err_type:
            pass

    # pass cases
    case_list = [(3, '*', orig), ('(0,0)', '+', (0, 0)),
                 (TikZNode(at=orig, handle='h1'), '+', (0, 0)),
                 (impl, '-', impl)]

    for case in case_list:
        tmp = _TikZCoordinateImplicitCalculation(*case)
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
