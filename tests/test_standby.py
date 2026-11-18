#!/usr/bin/env python3
"""Offline tests, no block-device or LED hardware access."""
import importlib.util
import tempfile
from pathlib import Path
from unittest import mock

SCRIPT=Path(__file__).parent.parent / 'package/usr/bin/ugreen-check-standby'
spec=importlib.util.spec_from_file_location('ugreen_check_standby', SCRIPT)
# File extensionless source: explicit loader
from importlib.machinery import SourceFileLoader
spec=importlib.util.spec_from_loader('ugreen_check_standby',SourceFileLoader('ugreen_check_standby',str(SCRIPT)))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.classify_smartctl(2, 'Device is in STANDBY mode, exit(2)') == 'standby'
assert m.classify_smartctl(0, 'Device is in ACTIVE or IDLE mode') == 'active'
assert m.classify_smartctl(0, 'Device Model: HGST example') == 'active'
assert m.classify_smartctl(2, 'Unable to detect device type') is None
assert m.classify_smartctl(0, 'random output') is None
assert m.main(['0','0 0 255','255 255 255','sda','disk1']) == 2
assert m.main(['30','0 0 255','255 255 255','sda']) == 2
with tempfile.TemporaryDirectory() as d:
    p=Path(d)
    (p/'disk1').mkdir()
    (p/'disk1'/'color').write_text('255 0 0\n')
    with mock.patch.object(m,'LED_ROOT',p), mock.patch.object(m,'disk_state',return_value='standby'):
        m.update_led('sda','disk1','0 0 255','255 255 255')
        assert (p/'disk1'/'color').read_text().strip() == '255 0 0'
    (p/'disk1'/'color').write_text('255 255 255\n')
    with mock.patch.object(m,'LED_ROOT',p), mock.patch.object(m,'disk_state',return_value='standby'):
        m.update_led('sda','disk1','0 0 255','255 255 255')
        assert (p/'disk1'/'color').read_text().strip() == '0 0 255'
    with mock.patch.object(m,'LED_ROOT',p), mock.patch.object(m,'disk_state',return_value='active'):
        m.update_led('sda','disk1','0 0 255','255 255 255')
        assert (p/'disk1'/'color').read_text().strip() == '255 255 255'
    with mock.patch.object(m,'LED_ROOT',p), mock.patch.object(m,'disk_state',return_value=None):
        m.update_led('sda','disk1','0 0 255','255 255 255')
        assert (p/'disk1'/'color').read_text().strip() == '255 255 255'
print('Standby helper offline tests: PASS')
