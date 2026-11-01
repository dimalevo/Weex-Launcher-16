#!/usr/bin/env python3
"""Prevent legacy API-specific overrides breaking DesktopTaskView on Android 10+."""
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[2]
android_id = '{http://schemas.android.com/apk/res/android}id'
for relative in (
    'quickstep/res/layout/task_desktop.xml',
    'lawnchair/res/layout-v28/task_desktop.xml',
    'lawnchair/res/layout-v31/task_desktop.xml',
):
    tree = ET.parse(root / relative)
    content = [node for node in tree.iter()
               if node.attrib.get(android_id) == '@+id/desktop_content']
    assert len(content) == 1, f'{relative}: desktop_content missing or duplicated'
    assert content[0].tag == 'com.android.quickstep.views.DesktopTaskContentView', relative
    assert any(node.attrib.get(android_id) == '@+id/background'
               for node in content[0].iter()), f'{relative}: background must be inside content'
    assert any(node.tag == 'ViewStub' and node.attrib.get(android_id) == '@+id/icon'
               for node in tree.iter()), f'{relative}: icon stub missing'
print('All desktop layouts contain the views expected by DesktopTaskView.')
