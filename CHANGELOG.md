# Changelog

## 1.0.4 — LED day/night/off and restart (validated on DXP6800 Pro)

- Add `ugreen-led-control day`, `night`, `restart`; keep `on` as alias for `day`, plus `off` and `status`.
- DAY: Power purple brightness 50, disk and network monitors enabled.
- NIGHT: Power purple brightness 10, disk/network LEDs off, monitor services stopped.
- OFF: all LEDs off, including Power.
- Persist mode via `/var/lib/ugreen-led-complete/night` or `/var/lib/ugreen-led-complete/disabled`; defaults to DAY.
- systemd Power unit uses mode-aware ExecCondition; disks/network/hotplug are skipped in NIGHT and OFF.
- Preserve SATA udev hotplug monitor, suppress updates outside DAY.
- Restart reapplies the persisted mode. Setup now respects the selected mode instead of forcing DAY.
- Upgrade 1.0.3 → 1.0.4 tested on DXP6800 Pro with Debian 13 / OMV 8.
- Hardware validated: DAY↔NIGHT, NIGHT→OFF→DAY, RESTART in DAY and NIGHT, NIGHT survives NAS reboot, RAID 10 intact.
- Not yet individually verified: OFF persists after a reboot; actual hotplug after upgrading to 1.0.4.

Previous versions: see GitHub history and previous releases.
