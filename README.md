# UGREEN LED Complete — Debian 13 / OpenMediaVault 8

**A consolidated Debian package for UGREEN NAS front-panel LEDs**, combining the UGREEN kernel driver (DKMS), disk/network monitoring utilities, and a small systemd-based LED manager into one installable `.deb`.

> **Upstream credit:** Based on [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller). The original author reverse-engineered the LED controller protocol and provided the kernel driver, CLI, disk and network monitoring tools. This repository repackages and extends those components for a particular Debian/OMV installation. **This is an independent, unofficial packaging project, not an official upstream release or UGREEN product.**

## Verified environment

| Item | Tested configuration |
| --- | --- |
| NAS | **UGREEN DXP6800 Pro** |
| Operating system | **Debian 13 (Trixie)** |
| NAS management | **OpenMediaVault 8** |
| Kernel | `7.2.12+deb13-amd64` |
| Driver | `led-ugreen/0.3` via DKMS |
| Package | `ugreen-led-complete 1.0.2` (`amd64`) |
| Network LED monitoring | `enp89s0` on the tested machine |

**Tested:** upgrade from 1.0.1 to 1.0.2, systemd services, LED on/off, reboot persistence, DKMS installation, SATA hotplug detection and disk monitor refresh. **Not yet tested:** a completely fresh Debian 13 / OMV 8 installation or other NAS models/kernels. The package is not guaranteed to be plug-and-play on all configurations.

## What's included?

The package consolidates functionality previously distributed as:

- `led-ugreen-dkms` 0.3 — kernel module source, DKMS integration.
- `led-ugreen-utils` 0.3 — probing, disk activity and network activity monitoring, CLI.
- `ugreen-led-manager` 1.0.0 — power LED policy, SATA hotplug watcher, service orchestration and on/off control.

These are **integrated files**, not three nested `.deb` archives. The package declares `Conflicts`, `Replaces`, and `Provides` for the older package names.

### Layout

```text
ugreen-led-complete/
├── README.md
├── LICENSE
├── package/                      # Exact dpkg-deb -R extraction of v1.0.2
│   ├── DEBIAN/                    # control, preinst, postinst, prerm, postrm
│   ├── etc/                       # example config + systemd units
│   ├── lib/systemd/system/        # power and hotplug services
│   └── usr/
│       ├── bin/                  # upstream monitoring tools and CLI
│       ├── libexec/              # hotplug, lock and state helpers
│       ├── sbin/                 # setup, check, on/off/status
│       └── src/led-ugreen-0.3/   # DKMS driver sources
├── scripts/build-deb.sh
├── docs/GUIDE_FR.md               # Detailed French technical guide
└── .github/ISSUE_TO_UPSTREAM.md   # Suggested upstream discussion
```

## Quick start (Debian 13 / OMV 8)

Download `ugreen-led-complete_1.0.2_amd64.deb` from this repository's GitHub Releases (once published), then run as root:

```bash
apt update
apt install ./ugreen-led-complete_1.0.2_amd64.deb
ugreen-led-complete-setup
ugreen-led-complete-check
```

**Prerequisites:** configured Debian APT repositories, a compatible running kernel, and matching kernel headers/build tools so DKMS can compile the driver. Verify before installing:

```bash
uname -r
ls -ld "/lib/modules/$(uname -r)/build"
```

The `.deb` declares these APT dependencies: `dkms`, `dmidecode`, `smartmontools`, `bash`, `python3`, `systemd`, `udev`, `util-linux`, **`i2c-tools`**. APT resolves these from configured repositories. The probe script loads `i2c-dev` and `led-ugreen` as required; **`i2c-dev` is a kernel module, not an APT package**.

For a **fresh installation**, review the example configuration (`/etc/ugreen-leds.example.conf`), verify the actual network interface with `ip -br link`, and inspect disk-to-slot mapping. The setup tool configures services and migration state; review its changes before relying on it in production.

## Upgrade from previous packages

The new `.deb` is intended to replace the three legacy components. Back up `/etc/ugreen-leds.conf` and custom systemd overrides first. Install with `apt install ./...deb` and run `ugreen-led-complete-setup` to migrate/enable the new services. The setup creates a timestamped backup in `/var/backups/ugreen-led-complete/`.

**Avoid conflicting commands:** an older `/usr/local/sbin/ugreen-led-control` may shadow `/usr/sbin/ugreen-led-control`. Verify with `type -a ugreen-led-control`.

## LED management

```bash
ugreen-led-control status
ugreen-led-control off
ugreen-led-control on
ugreen-led-complete-check

dkms status
systemctl status ugreen-probe-leds.service
systemctl status ugreen-diskiomon.service
systemctl status ugreen-netdevmon@enp89s0.service
systemctl status ugreen-led-manager-hotplug.service
systemctl status ugreen-led-manager-power.service

journalctl -u ugreen-led-manager-hotplug.service -f
journalctl -u ugreen-diskiomon.service -f
```

Use your own interface name instead of `enp89s0` when necessary. Standard `systemctl start|stop|restart|enable|disable` operations apply, but disabling a unit may be overridden by the manager setup/control flow. Use `ugreen-led-control` for coordinated on/off operations.

The power service sets `/sys/class/leds/power/color` to `255 0 255` (purple) and `brightness` to `50`. Disk monitoring uses ATA-based enumeration by default; **verify physical slot mapping** before treating a particular disk LED as an authoritative failure indicator. `/dev/sdX` names are not persistent.

## Build the Debian package from the extracted payload

```bash
sudo apt install dpkg-dev
./scripts/build-deb.sh
# output: dist/ugreen-led-complete_1.0.2_amd64.deb
```

The `package/` directory is the **actual extracted v1.0.2 payload**, including `DEBIAN/` maintainer scripts and binary utilities. The build script reconstructs a Debian package from those files; it does **not** recompile the bundled upstream CLI binaries from C/C++ source. The DKMS kernel driver *is* compiled locally at installation time. A rebuilt archive may have a different SHA256 from the published binary due to packaging metadata.

## Troubleshooting

```bash
dpkg-query -W -f='${Package} ${Version}\n${Depends}\n' ugreen-led-complete
dpkg-query -W i2c-tools
command -v i2cdetect
lsmod | grep -E 'i2c_dev|led_ugreen'
dkms status
systemctl --failed
```

If DKMS fails after a kernel upgrade, check the matching kernel headers and DKMS build logs. Do not assume the package supports an untested kernel. A `lsmod` warning about an unrelated `/sys/module/.../holders` directory was observed on the tested NAS without preventing LED initialization.

## Attribution and licensing

The upstream LED controller, kernel module, CLI, and monitoring scripts originate from **[miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller)**, licensed under the **MIT License** (copyright © 2024 `miskcoo@gmail.com`). The original copyright and license notice are retained in [`LICENSE`](LICENSE). This repository's integration and packaging changes are provided under the same MIT terms insofar as they are distributable by the packager.

Please report core driver/protocol issues upstream; report packaging and manager issues to this project's issue tracker once created. The repository has no affiliation with UGREEN or the original author.
