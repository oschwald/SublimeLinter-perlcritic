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
from SublimeLinter.lint import Linter, persist, util


class PerlCritic(Linter):

    """Provides an interface to perlcritic."""

    syntax = 'perl'
    executable = 'perlcritic'
    regex = r'\[.+\] (?P<message>.+?) at line (?P<line>\d+), column (?P<col>\d+).+?'

    def cmd(self):
        """Return a tuple with the command line to execute."""

        command = [self.executable_path, '--verbose', '8']

        config = util.find_file(
            os.path.dirname(self.filename), '.perlcriticrc')

        if config:
            command += ['-p', config]

        return command
