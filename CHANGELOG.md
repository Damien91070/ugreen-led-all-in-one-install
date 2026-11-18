# Changelog

## v1.0.3 — Hardware tested on DXP6800 Pro (2026-11-18)
- Add `ugreen-check-standby` using `smartctl -n standby -i` for SATA standby detection.
- Apply configured standby/healthy LED colors, without overriding SMART/error colors or unknown states.
- Enforce **30-second minimum** poll interval (clamps older 1-second configurations).
- Fix background standby helper PID handling in `ugreen-diskiomon`.
- Verified upgrade from v1.0.2, standby detection and wake on `/dev/sde` → `disk6`: green `0 255 0` → blue `0 0 255` → green `0 255 0`.
- Fresh OMV 8 installation and other NAS models remain untested.

## v1.0.2
- Add `i2c-tools` as an APT dependency.
- Verify upgrade from v1.0.1 on UGREEN DXP6800 Pro with Debian 13 / OMV 8.

## v1.0.1
- Consolidate DKMS driver, LED utilities and manager; add power LED service and SATA hotplug monitoring.
