from pylatex import Package, Command
from pylatex.base_classes import LatexObject, Container
import re

from pythontikz.common import TikzObject


def build_markings(at=None, between=None, start=None, finish=None, step=None,
                   marking=None):
    """Convenience wrapper function to construct decorations markings object"""


_valid_string_unit = re.compile(r'(-\s?)?[0-9]+(.[0-9]+)?(\s)?(pt|cm)?')


def _check_valid_unit(input_):
    """Checks if input is of the format of a valid latex length or number"""
    if isinstance(input_, (float, int)):
        return True
    elif (isinstance(input_, str)
          and _valid_string_unit.match(input_) is not None):
        return True
    return False


class MarkingsAt(TikzObject):
    def __init__(self, at, marking):
        if _check_valid_unit(at):
            self.at = at
        else:
            raise TypeError(f"Argument '{at}' is invalid for 'at'.")
        self.marking = marking
        super().__init__()

    def dumps(self, include_decoration_enable=True):
        if include_decoration_enable:
            mark_dumps = self.marking if isinstance(self.marking, str) else \
                self.marking.dumps()

            if include_decoration_enable:
                ret_str = '{markings,\n\tmark='
                tail = '}'
            else:
                ret_str = ''
                tail = ''
            ret_str += f'at {self.at} with {mark_dumps}' + tail
            return ret_str


class MarkingsBetween(Container):
    packages = [Package('tikz'), Command('usetikzlibrary',
                                         'decorations.markings')]

    def __init__(self, start_pos, end_pos, step, marking):
        for i in (start_pos, end_pos, step):
            if _check_valid_unit(i) is False:
                raise TypeError(f"Argument '{i}' is invalid.")
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.step = step
        self.marking = marking
        super().__init__()

    def dumps(self, decoration_marking_already_enabled=False):
        mark_dumps = self.marking if isinstance(self.marking, str) else \
            self.marking.dumps()

        if decoration_marking_already_enabled is False:
            ret_str = '{markings,\n\tmark='
            tail = '}'
        else:
            ret_str = ''
            tail = ''
        ret_str += (f'between positions {self.start_pos} '
                    f'and {self.end_pos} step {self.step} \n\t\t'
                    f'with {{{mark_dumps} }}')
        ret_str += tail
        return ret_str
