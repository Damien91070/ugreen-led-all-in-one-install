# UGREEN LED All-in-One for Debian 13 / OpenMediaVault 8

Unofficial integration of the UGREEN front-panel LED driver, monitoring tools, and systemd management into one Debian package, **`ugreen-led-complete`**.

> **Credits:** This project is based on @miskcoo [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller), which provides the original UGREEN LED driver and monitoring utilities. Original copyright and MIT license are preserved in [LICENSE](LICENSE). Unofficial community packaging; not affiliated with UGREEN.

## Table of contents

- [Hardware-tested configuration](#hardware-tested-configuration)
- [Features](#features)
- [Install / upgrade](#install--upgrade)
- [Repository files and reproducibility](#repository-files-and-reproducibility)
- [License](#license)
- [Quick reference — LED control and troubleshooting](#quick-reference--led-control-and-troubleshooting)

## Hardware-tested configuration

| Component | Environment |
|---|---|
| NAS | **UGREEN DXP6800 Pro** |
| OS | Debian 13 (Trixie) |
| NAS administration | OpenMediaVault 8 |
| Tested kernel | `7.2.12+deb13-amd64` |
| Driver | `led-ugreen/0.3`, built with DKMS |
| Current tested integration | **v1.0.3** |

v1.0.2 was tested for upgrade, driver setup, systemd services, LED controls, reboot persistence, and SATA hotplug. **v1.0.3 was additionally installed and hardware-tested** on the same NAS.

### Tested disk standby / wake sequence (v1.0.3)

The new `/usr/bin/ugreen-check-standby` runs under `ugreen-diskiomon.service` and uses `smartctl -n standby -i` to check disk power state without an intentional wakeup.

A real SATA HDD mapped **`/dev/sde → disk6`** was tested:

| State | Observed LED RGB |
|---|---|
| Healthy / active | **Green `0 255 0`** |
| Standby (verified by SMART `exit(2)`) | **Blue `0 0 255`** |
| Awake again | **Green `0 255 0`** |
| SMART / unavailable disk | Red `255 0 0` configured; the new helper does not override alert colors |

These are the **tested host's configuration values**: `COLOR_DISK_HEALTH="0 255 0"`, `COLOR_DISK_STANDBY="0 0 255"`. Other systems or the bundled example configuration may have different normal colors.

The polling interval is **at least 30 seconds**, even if a legacy config sets `STANDBY_CHECK_INTERVAL=1`. The helper does **not** command drives to sleep and never overrides unknown/alert LED colors.

## Features

- Consolidates three older packages: `led-ugreen-dkms 0.3`, `led-ugreen-utils 0.3`, and `ugreen-led-manager 1.0.0`.
- DKMS kernel driver, disk activity and SMART indication, network activity LEDs.
- SATA hotplug detection and disk LED monitor refresh.
- Power LED policy (purple, brightness 50), control `on|off|status`.
- New v1.0.3 disk standby / wake LED indicator.
- APT dependencies including `i2c-tools`, migration/setup, diagnostic scripts.

The original three `.deb` archives are not nested inside this package; their functions are integrated in one Debian archive.

## Install / upgrade

Download the v1.0.3 binary from the [Releases page](https://github.com/Damien91070/ugreen-led-all-in-one-install/releases) when it is published.

```bash
apt update
apt install ./ugreen-led-complete_1.0.3_amd64.deb
ugreen-led-complete-setup
systemctl restart ugreen-diskiomon.service
ugreen-led-complete-check
```

Matching Linux **kernel headers and build tools** are required for DKMS and may not be installed automatically. Verify `/lib/modules/$(uname -r)/build` exists.

```bash
ugreen-led-control on
ugreen-led-control off
ugreen-led-control status
pgrep -af ugreen-check-standby
journalctl -u ugreen-diskiomon.service -n 50 --no-pager
```

**Limitations:** Not verified on completely fresh OMV 8 installs or other UGREEN models; `ugreen-led-complete-setup` still selects network interface `enp89s0` on the tested installation, so verify and adapt it on other machines. Verify SATA device-to-LED mapping; `/dev/sdX` names can change.

Never force a disk in an active RAID array into standby just to test its LED. For an independent, unused test drive, a manual standby test can use `hdparm -y /dev/sdX` after confirming its use and mounting status.

## Repository files and reproducibility

`package/` contains the extracted Debian payload and maintainer scripts. `scripts/build-deb.sh` rebuilds the package from the payload after restoring executable permissions sometimes lost by ZIP/GitHub web uploads. `docs/GUIDE_FR.md` provides a full French Trilium reference.

The v1.0.3 source tree includes `package/usr/bin/ugreen-check-standby` and the updated `package/usr/bin/ugreen-diskiomon`. Before publishing, ensure the `v1.0.3` tag and release binary correspond to this source tree.

The package contains precompiled upstream userspace utilities. Rebuilding the Debian archive is **not** the same as compiling all upstream userspace binaries from their original sources. The DKMS kernel module is built at installation time.

## License

Original source: [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller) — MIT, copyright © 2024 miskcoo@gmail.com, with the original notice retained. Additional packaging/integration is shared on compatible MIT terms. No warranty or official UGREEN support.

## Quick reference — LED control and troubleshooting

Run these commands as `root` (or with `sudo`). These examples apply to the tested DXP6800 Pro under Debian 13 / OMV 8.

```bash
# Global LED power / state
ugreen-led-control on
ugreen-led-control off
ugreen-led-control status

# Full system diagnostics and DKMS
ugreen-led-complete-check
dkms status

# Display the current RGB color of every available disk, network and power LED
for led in /sys/class/leds/{disk*,netdev,power}; do
    [ -f "$led/color" ] && echo "$(basename "$led"): $(cat "$led/color")"
done

# Individual LED color (example: tested SATA drive /dev/sde -> disk6)
cat /sys/class/leds/disk6/color

# Standby detector and non-waking drive-state query
pgrep -af ugreen-check-standby
smartctl -n standby -i /dev/sde

# Disk/network monitoring services (change the interface if needed)
systemctl status ugreen-diskiomon.service
systemctl status ugreen-netdevmon@enp89s0.service
systemctl status ugreen-led-manager-hotplug.service
systemctl status ugreen-led-manager-power.service
systemctl status ugreen-probe-leds.service

# Follow disk and SATA hotplug logs
journalctl -u ugreen-diskiomon.service -f
journalctl -u ugreen-led-manager-hotplug.service -f
```

**Observed disk LEDs on the tested host:** green `0 255 0` = healthy/awake; blue `0 0 255` = standby; red `255 0 0` = SMART failure or unavailable (depending on monitoring/configuration). The helper never forces drives to sleep. Disk/LED slot mapping and network-interface names can differ on other machines. Do not force active RAID member drives into standby for testing.
