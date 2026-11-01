#!/usr/bin/env python3
"""Install/uninstall the widget as the desktop user; sudo is used for the helper only."""
import argparse
import datetime
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
HELPER = '/usr/local/sbin/omarchy-toggle-win-fn'
RULE = '/etc/sudoers.d/omarchy-msi-win-fn'
WIDGET_ID = 'msi-win-fn'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--uninstall', action='store_true')
    parser.add_argument('--fn-side', choices=['left', 'right'], default='left', help='Physical Fn key position')
    args = parser.parse_args()
    if os.geteuid() == 0:
        parser.error('Run as your desktop user, not with sudo.')
    user = pwd.getpwuid(os.getuid()).pw_name
    if not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_-]*', user):
        parser.error('Username requires a manually configured sudoers rule.')
    config_root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
    config_file = config_root / 'omarchy/shell.json'
    config = json.loads(config_file.read_text())
    layout = config['bar']['layout']
    destination = config_root / 'omarchy/bar/modules/msi-win-fn.qml'
    # Validate everything before making privileged changes.
    for entries in layout.values():
        if not isinstance(entries, list):
            raise ValueError('Unexpected bar layout')
    if not args.uninstall:
        state = Path('/sys/devices/platform/msi-ec/win_key').read_text().strip()
        if state not in ('left', 'right'):
            raise ValueError('Driver does not expose a recognized Win/Fn state')
        subprocess.run(['bash', '-n', str(ROOT / 'helper/toggle-win-fn')], check=True)
        with tempfile.TemporaryDirectory() as temp:
            rule = Path(temp) / 'sudoers'
            rule.write_text(f'{user} ALL=(root) NOPASSWD: {HELPER} ""\n')
            subprocess.run(['sudo', 'visudo', '-cf', str(rule)], check=True)
            subprocess.run(['sudo', 'install', '-o', 'root', '-g', 'root', '-m', '755', str(ROOT / 'helper/toggle-win-fn'), HELPER], check=True)
            subprocess.run(['sudo', 'install', '-o', 'root', '-g', 'root', '-m', '440', str(rule), RULE], check=True)
    else:
        subprocess.run(['sudo', 'rm', '-f', RULE, HELPER], check=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    shutil.copy2(config_file, str(config_file) + '.bak.' + stamp)
    for section, entries in layout.items():
        layout[section] = [entry for entry in entries if entry.get('id') != WIDGET_ID]
    if args.uninstall:
        destination.unlink(missing_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.copy2(destination, str(destination) + '.bak.' + stamp)
        shutil.copy2(ROOT / 'widget/msi-win-fn.qml', destination)
        layout.setdefault('right', []).insert(0, {
            'id': WIDGET_ID, 'type': 'qml', 'source': str(destination),
            'physicalFnSide': args.fn_side,
        })
    temporary = config_file.with_name('shell.json.tmp.' + str(os.getpid()))
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(config_file)
    print('Removed.' if args.uninstall else 'Installed.')
    print('Run: omarchy restart shell')

if __name__ == '__main__':
    main()
