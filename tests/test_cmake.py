"""Testing for cmake_task.py."""

from .base import BaseTest
from celerybot import cmake_task


class TestCMakeBuild(BaseTest):

    """Testing for CMakeBuild."""
    
    def test_task_name_unique(self):
        """Make sure task names are unique."""
        task1 = cmake_task.CMakeBuild('')
        task2 = cmake_task.CMakeBuild('')
        self.assertNotEqual(task1, task2)
        
