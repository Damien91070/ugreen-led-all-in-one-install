# UGREEN LED Complete — Debian 13 / OpenMediaVault 8

Unofficial, consolidated Debian package for the **UGREEN DXP6800 Pro** front-panel LEDs, integrating the DKMS LED driver, disk/network activity monitors, and an additional systemd-based LED manager.

> **Original source and attribution:** [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller) by miskcoo. Original driver/protocol work, CLI and monitoring utilities are derived from that project and retain its [MIT license](LICENSE). This project is not affiliated with UGREEN or the upstream author.

## Tested environment

| Component | Environment |
|---|---|
| Hardware | **UGREEN DXP6800 Pro** |
| OS | **Debian 13 (Trixie)** |
| NAS interface | **OpenMediaVault 8** |
| Tested kernel | `7.2.12+deb13-amd64` |
| LED driver | `led-ugreen/0.3` via DKMS |
| Consolidated package | `ugreen-led-complete 1.0.2` (`amd64`) |

**Verified:** upgrade from v1.0.1 to v1.0.2, LED on/off/status, services across a reboot, power LED, disk/network monitoring, DKMS installation, and SATA hotplug-triggered disk LED refresh.

**Not yet verified:** completely fresh Debian 13 / OMV 8 installation, all other UGREEN models, or future kernels. Matching kernel headers and toolchain remain prerequisites for DKMS.

## Project components

The single `.deb` combines the functions of three earlier packages:

1. `led-ugreen-dkms 0.3` — UGREEN LED kernel driver source and DKMS integration.
2. `led-ugreen-utils 0.3` — I²C probe, command-line tools, disk and network activity monitoring.
3. `ugreen-led-manager 1.0.0` — on/off control, power LED policy, hotplug watcher, migration/setup and diagnostics.

These components are merged into one Debian package; the three original `.deb` files are not nested inside it.

### Package structure

```text
ugreen-led-complete_1.0.2_amd64.deb
├── DEBIAN/                 # control, preinst, postinst, prerm, postrm
├── etc/
│   ├── ugreen-leds.example.conf
│   └── systemd/system/     # probe, disk, network services
├── lib/systemd/system/     # hotplug and power services
└── usr/
    ├── bin/                # upstream utilities and CLI
    ├── libexec/            # helper programs
    ├── sbin/               # ugreen-led-control, setup, check
    └── src/led-ugreen-0.3/ # DKMS C source and Makefile
```

## Installation (Debian 13 / OMV 8)

Download `ugreen-led-complete_1.0.2_amd64.deb` from this repository's **Releases** section when available. Run as root:

```bash
apt update
apt install ./ugreen-led-complete_1.0.2_amd64.deb
ugreen-led-complete-setup
ugreen-led-complete-check
```

The package declares APT dependencies on `dkms`, `dmidecode`, `smartmontools`, `bash`, `python3`, `systemd`, `udev`, `util-linux`, and **`i2c-tools`**. APT resolves missing packages from configured Debian repositories. `i2c-dev` is a **kernel module**, not an APT package: the probe attempts to load it via `modprobe`.

**Before installing on a new system**, make sure matching kernel headers are installed and accessible:

```bash
uname -r
ls -ld "/lib/modules/$(uname -r)/build"
```

The package has been tested on an existing machine, **not yet on a pristine installation**. Review `/etc/ugreen-leds.example.conf`, verify your interface with `ip -br link`, and verify physical disk-to-slot mapping rather than assuming that `/dev/sdX` names are stable.

## Migration from legacy packages

Back up `/etc/ugreen-leds.conf` and custom systemd overrides. Install the new `.deb` with APT and run `ugreen-led-complete-setup`. It creates a timestamped backup under `/var/backups/ugreen-led-complete/`. The package declares `Conflicts`, `Replaces`, and `Provides` for the three earlier package names.

If an old `/usr/local/sbin/ugreen-led-control` is installed, it may override the packaged command. Check with `type -a ugreen-led-control`.

## Commands

```bash
ugreen-led-control on
ugreen-led-control off
ugreen-led-control status
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

Substitute your real network interface name for `enp89s0`. The default power service sets a purple LED color (`255 0 255`) and brightness `50`. SATA hotplug handling triggers a disk LED monitor refresh; it does **not** make hot-removal safe for active RAID arrays.

## Sources, reproducibility, and release

The full v1.0.2 extracted Debian payload, including all maintainer scripts and driver sources, is provided in the separately prepared [repository import ZIP](https://github.com/Damien91070/ugreen-les-all-in-one-install). **The source tree must be uploaded from that archive; this README alone does not constitute a complete source release.**

Once `package/` and `scripts/build-deb.sh` have been imported:

```bash
./scripts/build-deb.sh
```

This reconstructs a Debian archive from the extracted payload. It does **not** rebuild the upstream CLI binary from original application source; DKMS compiles the kernel module locally at installation time.

## License and acknowledgements

Upstream: [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller). Original code is distributed under the **MIT License**; the copyright and permission notice are preserved in [LICENSE](LICENSE). Integration and packaging changes in this project are provided under compatible MIT terms. Please keep upstream attribution in redistributed copies.

This is a **community-made, unofficial** package, without warranty.