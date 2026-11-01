# MSI Win/Fn switch for the Omarchy bar

A small Omarchy/Quickshell widget showing which **physical key currently acts as Super**:

- **FN**: the key printed Fn acts as Super.
- **WIN**: the key printed Windows acts as Super.

Click to swap. The tooltip only identifies the current Super key. The widget polls the controller every three seconds and refreshes after a click. If the driver is unavailable, it shows `?`.

## Requirements

- Omarchy with the Quickshell bar and custom QML module support.
- A supported MSI laptop and the community [msi-ec driver](https://github.com/BeardOverflow/msi-ec).
- `/sys/devices/platform/msi-ec/win_key` must be readable and contain `left` or `right`.
- Python 3, Bash, sudo, util-linux (`flock`), and libnotify (`notify-send`).

This project does not install or force-load a kernel driver, access raw EC registers, or claim support for every MSI laptop. Follow the driver's supported-device instructions first.

## Install

Review `install.py` and `helper/toggle-win-fn`, then run as your normal desktop user:

```sh
python3 install.py
omarchy restart shell
```

The default assumes the **physical Fn key is on the left** and Windows is on the right. For the opposite physical arrangement:

```sh
python3 install.py --fn-side right
omarchy restart shell
```

The installer adds a widget to the right section of `~/.config/omarchy/shell.json` and makes a dated backup. It respects `XDG_CONFIG_HOME`. You can drag the widget to another position using the bar's normal controls.

## Permissions and persistence

The installer requests sudo to install a root-owned helper at `/usr/local/sbin/omarchy-toggle-win-fn` and a sudoers entry for your user. The entry allows **only that helper with no arguments**, without asking for a password on every click. It does not grant general passwordless sudo.

The helper takes a lock, toggles the driver's `win_key` attribute, and saves the selected position in `/etc/tmpfiles.d/msi-win-fn.conf`. It restores the original position if saving fails. Persistence requires `msi-ec` to be loaded before systemd-tmpfiles runs at boot. Suspend/resume persistence has not been verified.

If you previously installed a custom version of this widget, remove that bar entry before installing this package to avoid two indicators. Do not install multiple users' copies of the helper independently: its path is shared system-wide.

## Uninstall

```sh
python3 install.py --uninstall
omarchy restart shell
```

This removes this project's bar entry, QML file, helper and sudoers rule. It leaves the driver, current key mapping and persistence file intact. To stop restoring the mapping at boot, optionally remove `/etc/tmpfiles.d/msi-win-fn.conf`. To restore the usual physical labels first, write `right` to `win_key` when the physical Windows key is on the right (or `left` when it is on the left).

## Validation and limits

The original local implementation was tested on MSI GL75 Leopard 10SFR, EC firmware `17E7EMS1.106`, Omarchy 4.0.6, kernel `7.2.8-9-omarchy`, and msi-ec commit `d7fbbd8`. Both mapping directions and saved state were checked; the owner confirmed that the keyboard swap works. This portable installer and the configurable opposite physical arrangement have not yet been tested on another machine.

For this kernel, the driver needed a local battery-hook API compatibility change. An existing upstream [PR #880](https://github.com/BeardOverflow/msi-ec/pull/880) addresses that issue using feature detection. A version-number-only workaround is not portable across distro kernels; this widget does not bundle one.

## Credits

Hardware support comes from the **msi-ec contributors**; desktop components come from **Omarchy and Quickshell**. This widget, helper and installer were developed with OpenAI Codex assistance and tested locally by the owner. This is an independent community project.

MIT license for this repository's code; upstream projects retain their own licenses.
