#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Gregory Oschwald (based on linter by Aparajita Fishman)
# Copyright (c) 2013 Gregory Oschwald, Aparajita Fishman
#
# License: MIT
#

"""This module exports the PerlCritic linter class."""

import os
from SublimeLinter.lint import Linter


#-----------------------------------------------------------------------------
#
# sl3_util_climb & sl3_util_find_file
#
#   Sublime Linter 4 retired util.climb and util.find_file and by doing so
#   this linter was rendered unusable.  We are making copies of the retired
#   code here to still be able to find configuration files for perlcritic
#   looking upwards among directories in the project.
#

def sl3_util_climb(start_dir, limit=None):
    """
    Generate directories, starting from start_dir.

    If limit is None, stop at the root directory.
    Otherwise return a maximum of limit directories.
    """
    right = True

    while right and (limit is None or limit > 0):
        yield start_dir
        start_dir, right = os.path.split(start_dir)

        if limit is not None:
            limit -= 1


def sl3_util_find_file(start_dir, name, parent=False, limit=None, aux_dirs=[]):
    """
    Find the given file by searching up the file hierarchy from start_dir.

    If the file is found and parent is False, returns the path to the file.
    If parent is True the path to the file's parent directory is returned.

    If limit is None, the search will continue up to the root directory.
    Otherwise a maximum of limit directories will be checked.

    If aux_dirs is not empty and the file hierarchy search failed,
    those directories are also checked.
    """
    for d in sl3_util_climb(start_dir, limit=limit):
        target = os.path.join(d, name)

        if os.path.exists(target):
            if parent:
                return d

            return target

    for d in aux_dirs:
        d = os.path.expanduser(d)
        target = os.path.join(d, name)

        if os.path.exists(target):
            if parent:
                return d

            return target

#-----------------------------------------------------------------------------

class PerlCritic(Linter):

    """Provides an interface to perlcritic."""

    regex = r'\[.+\] (?P<message>.+?) at line (?P<line>\d+), column (?P<col>\d+).+?'

    defaults = {
        'selector': 'source.modernperl, source.perl'
    }

    def cmd(self):
        """Return a tuple with the command line to execute."""

        command = ['perlcritic', '--verbose', '8']

        config = sl3_util_find_file(
            os.path.dirname(self.filename), '.perlcriticrc'
        )

        if config:
            command += ['-p', config]

        return command
