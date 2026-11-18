# UGREEN LED All-in-One v1.0.3

## Hardware-validated HDD standby LEDs

This update adds **automatic disk standby/wake LED status** to the consolidated UGREEN LED Debian package, based on the original [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller) project.

### Tested hardware

- **NAS:** UGREEN DXP6800 Pro
- **OS:** Debian 13 (Trixie) with OpenMediaVault 8
- **Kernel:** `7.2.12+deb13-amd64`
- **Architecture:** AMD64
- **Driver:** `led-ugreen/0.3` (DKMS)

### What's new in v1.0.3

- Bundled `ugreen-check-standby` for SMART-based ATA disk power-state monitoring.
- Read-only status checks via `smartctl -n standby -i` to avoid intentional wakeups of sleeping ATA disks.
- **Healthy / active → green (`0 255 0`), standby → blue (`0 0 255`), awake → green (`0 255 0`)** as observed on the test NAS (colors are configurable).
- Maintains existing SMART alert LED colors (red by default); unknown disk states do not change LED colors.
- Enforces a **30-second minimum monitoring interval**, even with older configuration values.
- Fixes standby helper background process PID tracking in `ugreen-diskiomon`.
- Retains the previous v1.0.2 APT dependencies, DKMS driver, SATA hotplug and systemd services.

### Real-world validation

The v1.0.3 package was successfully installed as an upgrade from v1.0.2 on a UGREEN DXP6800 Pro. A test HDD mapped `/dev/sde` to `disk6`. During standby, `smartctl -n standby -i /dev/sde` returned `Device is in STANDBY mode, exit(2)` and the LED was blue. After wakeup, the LED returned to green. All five LED services were active in the installation checks.

### Installation / upgrade

Download **`ugreen-led-complete_1.0.3_amd64.deb`** from the release assets and run as root:

```bash
apt update
apt install ./ugreen-led-complete_1.0.3_amd64.deb
ugreen-led-complete-setup
systemctl restart ugreen-diskiomon.service
ugreen-led-complete-check
```

Matching Linux kernel headers/build dependencies are required for DKMS. The package installs `i2c-tools` through APT dependencies. To harmonize older configuration:

```bash
sed -i 's/^STANDBY_CHECK_INTERVAL=.*/STANDBY_CHECK_INTERVAL=30/' /etc/ugreen-leds.conf
systemctl restart ugreen-diskiomon.service
```

### Checks

```bash
ugreen-led-control status
pgrep -af ugreen-check-standby
journalctl -u ugreen-diskiomon.service -n 50 --no-pager
```

### Known limitations

- Validated on DXP6800 Pro and one independent SATA test HDD, **not** on every NAS model or a completely fresh Debian 13/OMV 8 system.
- The network interface `enp89s0` remains hardcoded in the setup service configuration; adapt for other systems.
- Ensure physical disk-to-LED mapping is correct: `/dev/sdX` identifiers can change.
- **Do not force disks belonging to an active RAID array into standby** to test their LED behavior.
- The status helper does not initiate HDD standby or guarantee that other system services will not wake a disk.

### Attribution

Original project: [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller), MIT licensed; copyright attribution retained. This is an unofficial community integration, not affiliated with UGREEN.

**SHA-256 — `ugreen-led-complete_1.0.3_amd64.deb`:**

```
7f240cdcc30cd487b79da30adf61f2b55694c59140a12392dba5e18f7bc33b9a
```