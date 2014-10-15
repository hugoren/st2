try:
    import simplejson as json
except ImportError:
    import json

import os

from oslo.config import cfg
import unittest2

from st2actions.constants import LIBS_DIR as ACTION_LIBS_DIR
from st2actions.container.service import RunnerContainerService
import st2tests.config as tests_config


class RunnerContainerServiceTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        tests_config.parse_args()

    def test_get_entry_point_absolute_path(self):
        service = RunnerContainerService()
        orig_path = cfg.CONF.content.content_packs_base_path
        cfg.CONF.content.content_packs_base_path = '/tests/packs'
        acutal_path = service.get_entry_point_abs_path(pack='foo', entry_point='/foo/bar.py')
        self.assertEqual(acutal_path, '/foo/bar.py', 'Entry point path doesn\'t match.')
        cfg.CONF.content.content_packs_base_path = orig_path

    def test_get_entry_point_absolute_path_empty(self):
        service = RunnerContainerService()
        orig_path = cfg.CONF.content.content_packs_base_path
        cfg.CONF.content.content_packs_base_path = '/tests/packs'
        acutal_path = service.get_entry_point_abs_path(pack='foo', entry_point=None)
        self.assertEqual(acutal_path, None, 'Entry point path doesn\'t match.')
        acutal_path = service.get_entry_point_abs_path(pack='foo', entry_point='')
        self.assertEqual(acutal_path, None, 'Entry point path doesn\'t match.')
        cfg.CONF.content.content_packs_base_path = orig_path

    def test_get_entry_point_relative_path(self):
        service = RunnerContainerService()
        orig_path = cfg.CONF.content.content_packs_base_path
        cfg.CONF.content.content_packs_base_path = '/tests/packs'
        acutal_path = service.get_entry_point_abs_path(pack='foo', entry_point='foo/bar.py')
        expected_path = os.path.join(cfg.CONF.content.content_packs_base_path, 'foo', 'actions',
                                     'foo/bar.py')
        self.assertEqual(acutal_path, expected_path, 'Entry point path doesn\'t match.')
        cfg.CONF.content.content_packs_base_path = orig_path

    def test_get_action_libs_abs_path(self):
        service = RunnerContainerService()
        orig_path = cfg.CONF.content.content_packs_base_path
        cfg.CONF.content.content_packs_base_path = '/tests/packs'

        # entry point relative.
        acutal_path = service.get_action_libs_abs_path(pack='foo', entry_point='foo/bar.py')
        expected_path = os.path.join(cfg.CONF.content.content_packs_base_path, 'foo', 'actions',
                                     os.path.join('foo', ACTION_LIBS_DIR))
        self.assertEqual(acutal_path, expected_path, 'Action libs path doesn\'t match.')

        # entry point absolute.
        acutal_path = service.get_action_libs_abs_path(pack='foo', entry_point='/tmp/foo.py')
        expected_path = os.path.join('/tmp', ACTION_LIBS_DIR)
        self.assertEqual(acutal_path, expected_path, 'Action libs path doesn\'t match.')
        cfg.CONF.content.content_packs_base_path = orig_path

    def test_report_result_json(self):
        service = RunnerContainerService()
        result = '["foo", {"bar": ["baz", null, 1.0, 2]}]'
        service.report_result(result)
        self.assertEqual(json.dumps(service.get_result()), result,
                         'JON results aren\'t handled right')
