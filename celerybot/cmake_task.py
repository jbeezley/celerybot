#!/usr/bin/env python

"""A collection of CMake task helper methods and classes."""

from subprocess import Popen
import os
import tempfile
import datetime
_common = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'common.ctest'
    )
)


class CMakeBuild(object):

    """A support class for generating cmake build tasks for Celery."""

    def __init__(self, repo, source=None, 
                 git='git', cmake='cmake',
                 ctest='ctest', env={}):
        """Initialize build variables.

        :param str repo: The git repository url containing the project
        :param str source: The source path to use
        :param str git: The git binary
        :param str cmake: The cmake binary
        :param str ctest: The ctest binary
        :param dict env: Environment variables to set.
        """
        self._repo = repo
        self._git = git
        self._cmake = cmake
        self._ctest = ctest
        self._env = env
        self._opts_file = 'ctest_options.cmake'
        self._source = source

    def task_name(self, sha, **opts):
        """Return a unique name for the given task."""
        return sha + '_' + datetime.datetime.now().isoformat()

    def build_path(self, sha, **opts):
        """Return a build directory for the given task."""
        return self._build_path

    def write_options(self, pth, **opts):
        """Set variables in an options file used by the ctest script."""
        fname = os.path.join(
            pth,
            self._opts_file
        )
        lines = []
        for var in opts:
            lines.append('set(%s "%s")' % (var, str(opts[var])))
        open(fname, 'w').write('\n'.join(lines))
        return fname

    def run_cmd(self, args, cwd='.'):
        """Run a command given by the argument list and return exit status."""
        print cwd
        print ' '.join(args)
        p = Popen(args, cwd=cwd, env=self._env)
        # add logging...
        return p.wait()

    def checkout(self, source, sha):
        """Checkout the given sha or branch in the source directory."""
        if not os.path.exists(source):
            args = [self._git, 'clone', self._repo, source]
            self.run_cmd(args)
        else:
            args = [self._git, 'fetch', self._repo]
            self.run_cmd(args, cwd=source)
        args = [self._git, 'checkout', sha]
        return self.run_cmd(args, cwd=source)

    def run_test(self, source, binary='.', **defs):
        """Save options to a new file and run ctest."""
        opts_file = self.write_options(
            binary,
            CTEST_BINARY_DIRECTORY=binary,
            CTEST_SOURCE_DIRECTORY=source,
            **defs
        )
        self.run_cmd(
            [
                self._ctest,
                '-S', _common,
                '-D', 'ctest_options=' + opts_file
            ]
        )

    def __call__(self, sha, opts={}):
        """Run tests for the given sha and ctest definitions."""
        temp = os.path.join(
            tempfile.gettempdir(),
            self.task_name(sha, **opts)
        )
        source = self._source
        binary = os.path.join(
            temp, 'build'
        )
        os.makedirs(binary)
        if not source:
            source = os.path.join(
                temp, 'source'
            )
        try:
            self.checkout(source, sha)
            self.run_test(source, binary, **opts)
        finally:
            pass
            # shutil.rmtree(temp)
