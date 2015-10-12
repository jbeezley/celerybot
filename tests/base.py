"""Base testing class."""

import tempfile
import os
from shutil import rmtree
from datetime import datetime
from unittest import TestCase

class BaseTest(TestCase):

    """Defines helper methods for all tests."""

    def __init__(self, *arg, **kw):
        """Initialize."""
        super(BaseTest, self).__init__(*arg, **kw)
        self.tempdir = None

    def setUp(self):
        """Create and return a temporary directory."""
        if self.tempdir:
            self.tearDown()

        d = tempfile.gettempdir()
        d = os.path.join(d, datetime.now().isoformat())
        os.makedirs(d)
        self.tempdir = d

    def tearDown(self):
        """Remove the temporary directory."""
        if self.tempdir and os.path.exists(self.tempdir):
            rmtree(self.tempdir)
        self.tempdir = None
