# Notes for a human-reviewed upstream report

An existing PR already covers the build problem:
https://github.com/BeardOverflow/msi-ec/pull/880

Do not open a duplicate issue or submit the local version guard as a general fix.

Locally observed facts:

- MSI GL75 Leopard 10SFR, EC `17E7EMS1.106`.
- Omarchy 4.0.6, kernel `7.2.8-9-omarchy`.
- msi-ec commit `d7fbbd8` failed to build with implicit declarations of `battery_hook_register` and `battery_hook_unregister`.
- The target kernel header declares `acpi_battery_hook_register` and `acpi_battery_hook_unregister`.
- Local aliases made the module compile, install and load. `win_key`/`fn_key` were present; swapping both directions worked.
- The owner's keyboard test confirmed the new mapping.
- The existing PR's implementation has NOT been built or tested here. Do not describe our workaround test as a test of PR #880.

The upstream README requires the contributor to review AI-assisted material personally, disclose model/tool involvement, and take responsibility. It disallows wholly AI-generated PRs and discourages wholly generated issue reports. The owner should write any upstream comment in their own words, using these facts, after reviewing them. No upstream post has been sent by this project.
