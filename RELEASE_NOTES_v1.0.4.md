# UGREEN LED Complete 1.0.4 — Hardware-validated release

**Platform tested:** UGREEN NASync DXP6800 Pro, Debian 13 / OpenMediaVault 8, kernel `7.2.12+deb13-amd64`.

### New controls

```bash
ugreen-led-control day      # Purple Power 50; disk/network LEDs active
ugreen-led-control night    # Purple Power 10; disk/network LEDs off
ugreen-led-control off      # All LEDs off
ugreen-led-control on       # Alias for day
ugreen-led-control restart  # Reapply saved mode and appropriate services
ugreen-led-control status   # Show saved mode and service statuses
```

- Modes persist in `/var/lib/ugreen-led-complete/`. Existing `disabled` marker is respected during upgrades.
- Power LED uses a mode-aware systemd service; disk/network/hotplug monitors remain inactive in NIGHT and OFF.
- SATA hotplug continues using `ugreen-led-manager-hotplug.service` and the udev event monitor (no additional .rules file).
- Debian packaging preserves the local `/etc/ugreen-leds.conf` and does not force DAY in `postinst`.

### Installation / upgrade

```bash
apt -s install ./ugreen-led-complete_1.0.4_amd64.deb
apt install ./ugreen-led-complete_1.0.4_amd64.deb
systemctl daemon-reload
ugreen-led-control restart
```

### Hardware verification

Confirmed by real NAS command output: upgrade 1.0.3 → 1.0.4; DAY Power brightness 50 and five services active; NIGHT Power brightness 10, RGB `255 0 255`, activity monitors inactive; OFF brightness 0; NIGHT→DAY restores services; `restart` preserves DAY/NIGHT; NIGHT survives reboot; `/dev/md1` RAID10 remains `[4/4] [UUUU]`.

**Not individually verified:** OFF persistence through reboot and fresh SATA hotplug *after* this upgrade. Do not interpret service-active status alone as a new hotplug hardware test.

### Binary SHA-256

`c3a1101d87c3290728b56d5b29b3de5739db7b1893d6822a171c21d3d1610dd4` — `ugreen-led-complete_1.0.4_amd64.deb`

### Credits

Based on [miskcoo/ugreen_leds_controller](https://github.com/miskcoo/ugreen_leds_controller) (MIT); see LICENSE.
