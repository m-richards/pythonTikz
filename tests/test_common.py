from pylatex import NoEscape

from pythontikz.common import Plot, TikzOptions


def test_plot():
    """Inherited class from pylatex code, same tests repeated."""
    p = Plot(name=None, func=None, coordinates=None, error_bar_deltas=None,
             options=None, use_auto_format=False)
    repr(p)
    assert p.dumps() == "\\addplot"

    p = Plot(name=NoEscape(r"$-\sin(x) + 4$"), func=r"-sin(\x r)+4",
             error_bar_deltas=None,
             options=TikzOptions({
                 'domain': NoEscape('-10:10'),
                 'samples': 80,
                 'mark size': '0.6pt'
             }),
             use_auto_format=True
             )
    repr(p)
    assert p.dumps() == '\\addplot+[domain=-10:10,samples=80,' \
                        'mark size=0.6pt]{-sin(\\x ' \
                        'r)+4};%\n%\n\\addlegendentry{$-\\sin(x) + 4$}'

    p = Plot(name=NoEscape(r"$-\sin(x) + 4$"),
             coordinates=list(zip(range(0, 5), [1, 4, 7, 2, -3])),
             error_bar_deltas=None,
             options=TikzOptions({
                 'domain': NoEscape('-10:10'),
                 'samples': 80,
                 'mark size': '0.6pt'
             }),
             use_auto_format=True
             )
    repr(p)
    assert p.dumps() == (
        '\\addplot+[domain=-10:10,samples=80,mark size=0.6pt] coordinates'
        ' {%\n(0,1)%\n(1,4)%\n(2,7)%\n(3,2)%\n(4,'
        '-3)%\n};%\n%\n\\addlegendentry{$-\\sin(x) + 4$}')

    error = [1 for i in range(5)]
    x = range(0, 5)
    y = [1, 4, 7, 2, -3]
    p = Plot(name=NoEscape(r"$-\sin(x) + 4$"),
             coordinates=list(zip(x, y)),
             error_bar_deltas=list(zip(error, error)),
             options=TikzOptions({
                 'domain': NoEscape('-10:10'),
                 'samples': 80,
                 'mark size': '0.6pt'
             }),
             use_auto_format=True
             )
    repr(p)
    assert p.dumps() == (
        '\\addplot+[domain=-10:10,samples=80,mark size=0.6pt] coordinates'
        ' {%\n'
        + "".join(f"({x},{y}) +- ({e},{e})%\n" for x, y, e in zip(x, y, error))
        + '};%\n%\n\\addlegendentry{$-\\sin(x) + 4$}')
