# UGREEN DXP6800 Pro — Gestion complète des LED (Debian 13 / OMV 8)

> **Fiche Trilium — version de référence :** `ugreen-led-complete 1.0.3` (amd64)  
> **NAS :** UGREEN DXP6800 Pro — Debian 13, OpenMediaVault 8  
> **Noyau validé :** `7.2.12+deb13-amd64` — **DKMS :** `led-ugreen/0.3`  
> **Interface réseau surveillée :** `enp89s0`  
> **Validation terrain :** installation, migration, contrôle ON/OFF, redémarrage et événement Hotplug SATA et cycle veille/réveil HDD validés le 18/11/2026.

## Sommaire

- [1. À quoi sert ce paquet ?](#1-à-quoi-sert-ce-paquet-)
- [2. Schéma d'architecture (TXT)](#2-schéma-darchitecture-txt)
- [3. Fonctionnement interne](#3-fonctionnement-interne)
  - [3.1. Initialisation matérielle](#31-initialisation-matérielle)
  - [3.2. LED disques](#32-led-disques)
  - [3.3. LED réseau](#33-led-réseau)
  - [3.4. Power LED](#34-power-led)
  - [3.5. Hotplug SATA](#35-hotplug-sata)
  - [3.6. Verrou anti-double-instance](#36-verrou-anti-double-instance)
  - [3.7. Persistance du mode ON/OFF](#37-persistance-du-mode-onoff)
- [4. Installation neuve (aucun ancien paquet UGREEN LED)](#4-installation-neuve-aucun-ancien-paquet-ugreen-led)
  - [4.1. Prérequis](#41-prérequis)
  - [4.2. Simulation et installation](#42-simulation-et-installation)
  - [4.3. Configuration avant activation](#43-configuration-avant-activation)
  - [4.4. Activer les services](#44-activer-les-services)
  - [4.5. Validation](#45-validation)
- [5. Migration depuis les anciens paquets / scripts personnalisés](#5-migration-depuis-les-anciens-paquets--scripts-personnalisés)
  - [5.1. Sauvegarder avant de migrer](#51-sauvegarder-avant-de-migrer)
  - [5.2. Simuler le remplacement](#52-simuler-le-remplacement)
  - [5.3. Installer](#53-installer)
  - [5.4. Exécuter le setup de migration](#54-exécuter-le-setup-de-migration)
  - [5.5. Corriger la priorité des anciens scripts](#55-corriger-la-priorité-des-anciens-scripts)
  - [5.6. Vérification après redémarrage](#56-vérification-après-redémarrage)
- [6. Commandes principales de gestion LED](#6-commandes-principales-de-gestion-led)
- [7. Référence exhaustive des services systemd](#7-référence-exhaustive-des-services-systemd)
  - [7.1. Commandes applicables à chaque service](#71-commandes-applicables-à-chaque-service)
  - [7.2. Exemples copiables, service par service](#72-exemples-copiables-service-par-service)
  - [7.3. Anciens services à laisser désactivés](#73-anciens-services-à-laisser-désactivés)
- [8. Configuration `/etc/ugreen-leds.conf`](#8-configuration-etcugreen-ledsconf)
  - [8.1. Paramètres des disques](#81-paramètres-des-disques)
  - [8.2. Paramètres réseau](#82-paramètres-réseau)
  - [8.3. Modifier et appliquer la configuration](#83-modifier-et-appliquer-la-configuration)
- [9. Contrôle direct des LED par sysfs (avancé)](#9-contrôle-direct-des-led-par-sysfs-avancé)
  - [9.1. Lire les valeurs sans modifier](#91-lire-les-valeurs-sans-modifier)
  - [9.2. Modifier temporairement une LED](#92-modifier-temporairement-une-led)
  - [9.3. Afficher les attributs disponibles](#93-afficher-les-attributs-disponibles)
- [10. DKMS, noyau et mises à jour](#10-dkms-noyau-et-mises-à-jour)
- [11. Journaux, erreurs courantes et dépannage](#11-journaux-erreurs-courantes-et-dépannage)
  - [11.1. Diagnostic rapide](#111-diagnostic-rapide)
  - [11.2. `lsmod: ERROR ... /sys/module/sunrpc/holders`](#112-lsmod-error--sysmodulesunrpcholders)
  - [11.3. `UGREEN: removed stale diskiomon lock`](#113-ugreen-removed-stale-diskiomon-lock)
  - [11.4. Service Power `inactive (dead)`](#114-service-power-inactive-dead)
  - [11.5. Mapping disques incorrect](#115-mapping-disques-incorrect)
  - [11.6. Les LED restent éteintes](#116-les-led-restent-éteintes)
  - [11.7. Vérifier l'ancien script prioritaire](#117-vérifier-lancien-script-prioritaire)
- [12. Sauvegardes et désinstallation](#12-sauvegardes-et-désinstallation)
  - [12.1. Où sont les sauvegardes ?](#121-où-sont-les-sauvegardes-)
  - [12.2. Examiner le contenu des sauvegardes](#122-examiner-le-contenu-des-sauvegardes)
  - [12.3. Désinstaller (à préparer, pas à faire sans raison)](#123-désinstaller-à-préparer-pas-à-faire-sans-raison)
- [13. Exemple d'intégration Home Assistant par SSH](#13-exemple-dintégration-home-assistant-par-ssh)
- [14. Fiche mémo — commandes essentielles](#14-fiche-mémo--commandes-essentielles)
- [15. Historique de validation — DXP6800 Pro](#15-historique-de-validation--dxp6800-pro)
- [16. Mise à jour 1.0.2 — installation autonome et vérifications I²C](#16-mise-à-jour-102--installation-autonome-et-vérifications-i²c)
  - [16.1. Changement par rapport à la 1.0.1](#161-changement-par-rapport-à-la-101)
  - [16.2. Procédure recommandée après réinstallation complète d’OMV 8](#162-procédure-recommandée-après-réinstallation-complète-domv-8)
  - [16.3. Vérification après installation ou mise à niveau](#163-vérification-après-installation-ou-mise-à-niveau)
  - [16.4. Messages APT non bloquants rencontrés](#164-messages-apt-non-bloquants-rencontrés)
  - [16.5. Portée de la validation](#165-portée-de-la-validation)
- [17. Nouveautés v1.0.3 — Détection de veille des HDD (validée sur le NAS)](#17-nouveautés-v103--détection-de-veille-des-hdd-validée-sur-le-nas)
- [18. Commandes de rappel — Référence rapide (v1.0.3)](#18-commandes-de-rappel--référence-rapide-v103)

## 1. À quoi sert ce paquet ?

`ugreen-led-complete_1.0.3_amd64.deb` regroupe dans **un seul paquet Debian** les trois composants auparavant séparés :

| Ancien paquet | Fonction |
|---|---|
| `led-ugreen-dkms 0.3` | Pilote noyau pour exposer les LED UGREEN à Linux |
| `led-ugreen-utils 0.3` | Utilitaires de surveillance des disques et du réseau |
| `ugreen-led-manager 1.0.0` | Orchestration systemd, Power LED, Hotplug SATA, contrôle ON/OFF |

**Ce n'est pas un firmware UGREEN.** Le paquet installe un module noyau compilé localement via DKMS et des programmes Linux. Il pilote les LED exposées sous `/sys/class/leds/`.

**Dépendances déclarées dans la 1.0.2 (vérifiées dans le `.deb` et sur le NAS) :** `dkms`, `dmidecode`, `smartmontools`, `bash`, `python3`, `systemd`, `udev`, `util-linux`, **`i2c-tools`**. APT installe les dépendances manquantes depuis les dépôts configurés. La compilation DKMS exige également les outils de compilation et les **en-têtes correspondant exactement au noyau actif** ; leur disponibilité n’est pas garantie par cette liste. Les commandes `ip`, `ping` et `modprobe` proviennent respectivement de `iproute2`, `iputils-ping` et `kmod` : contrôler leur présence sur une installation vierge.

**Compatibilité :** le paquet est en architecture `amd64`, conçu et testé ici sur DXP6800 Pro. Ne pas supposer qu'il fonctionne sur tous les NAS UGREEN ni sur tous les futurs noyaux sans test.

## 2. Schéma d'architecture (TXT)

```text
                       Debian 13 / OMV 8
                               |
                  ugreen-led-complete 1.0.3
                               |
            +------------------+------------------+
            |                  |                  |
       PILOTE DKMS        UTILITAIRES         ORCHESTRATION
            |                  |                  |
   /usr/src/led-ugreen-0.3   /usr/bin/*        /usr/sbin/*
            |                  |                  |
      compilation DKMS        |          ugreen-led-control
            |                 |             on / off / status
    led-ugreen.ko.xz          |                  |
            |                 |             systemd + état
    module led_ugreen         |                  |
            |                 |     +------------+------------+
            |                 |     |            |            |
      Bus I²C SMBus           |  Hotplug       Power       Monitoring
            |                 |     |            |            |
     /sys/class/leds/ <-------+-----+------------+------------+
            |
       +----+----------+--------------------+
       |               |                    |
     power           netdev              disk1..disk8
     violet         trafic/lien          activité/SMART
     50 %           réseau               disques SATA
```

### Arborescence réelle des fichiers contenus dans le `.deb`

```text
ugreen-led-complete_1.0.2_amd64.deb
|
+-- DEBIAN/                          [métadonnées et scripts d'installation]
|   +-- control                     dépendances, conflits, version
|   +-- preinst                     sauvegarde préinstallation
|   +-- postinst                    configuration, DKMS, daemon-reload
|   +-- prerm                       arrêt manager et suppression DKMS si retrait
|   +-- postrm                      daemon-reload
|
+-- etc/
|   +-- ugreen-leds.example.conf    modèle de configuration
|   +-- systemd/system/
|       +-- ugreen-probe-leds.service
|       +-- ugreen-diskiomon.service
|       +-- ugreen-diskiomon.service.d/
|       |   +-- 99-ugreen-led-complete.conf
|       +-- ugreen-netdevmon@.service
|
+-- lib/systemd/system/
|   +-- ugreen-led-manager-hotplug.service
|   +-- ugreen-led-manager-power.service
|
+-- usr/
    +-- bin/
    |   +-- ugreen-probe-leds        initialise I²C + module
    |   +-- ugreen-diskiomon        surveille disques / SMART
    |   +-- ugreen-blink-disk       clignotement activité disques
    |   +-- ugreen-netdevmon        LED réseau
    |   +-- ugreen_leds_cli         utilitaire bas niveau (binaire)
    +-- libexec/
    |   +-- ugreen-led-enabled              condition ON/OFF
    |   +-- ugreen-led-manager-hotplug      surveillance udev SATA
    |   +-- ugreen-led-manager-lockcheck    contrôle verrou diskiomon
    +-- sbin/
    |   +-- ugreen-led-control       commande ON/OFF/status
    |   +-- ugreen-led-complete-setup       migration / activation
    |   +-- ugreen-led-complete-check       diagnostic
    +-- src/led-ugreen-0.3/
        +-- Makefile
        +-- dkms.conf
        +-- led-ugreen.c
        +-- led-ugreen.h
```

**Remarque :** `/etc/ugreen-leds.conf` est créé à l'installation s'il n'existe pas ; le paquet contient le fichier *exemple* et non une configuration locale prédéfinie. Les sauvegardes et fichiers d'état sont générés à l'exécution, pas embarqués dans l'archive.

## 3. Fonctionnement interne

### 3.1. Initialisation matérielle

1. `ugreen-probe-leds.service` exécute `/usr/bin/ugreen-probe-leds`.
2. Le script vérifie/charge `i2c_dev` et `led_ugreen` (`modprobe -v i2c-dev`, `modprobe -v led-ugreen` si nécessaire).
3. Il cherche l'adaptateur `SMBus I801` avec `i2cdetect -l`.
4. Il enregistre si nécessaire le périphérique I²C `led-ugreen` à l'adresse **`0x3a`**.
5. Le pilote expose les LED dans `/sys/class/leds/` : `power`, `netdev`, `disk1` à `disk8`.

Le module DKMS est compilé dans l'arborescence DKMS, puis installé sous `/lib/modules/$(uname -r)/updates/dkms/`. Le fichier peut être compressé en `.ko.xz`.

### 3.2. LED disques

`ugreen-diskiomon.service` lance `/usr/bin/ugreen-diskiomon` ; ce script lit `/etc/ugreen-leds.conf`, associe les disques aux emplacements LED, surveille activité et états (SMART si activé), puis lance notamment `/usr/bin/ugreen-blink-disk`.

**Important :** `disk1` est une LED d'emplacement physique ; `/dev/sda` est un nom Linux susceptible de changer. Avec `MAPPING_METHOD=ata`, le programme reconstitue les associations depuis les chemins ATA. Après ajout/retrait de disque, vérifier que l'emplacement physique reste correct.

### 3.3. LED réseau

`ugreen-netdevmon@enp89s0.service` exécute `/usr/bin/ugreen-netdevmon enp89s0`. Le script configure le déclencheur noyau `netdev` pour la LED réseau (trafic TX/RX, état du lien) et, si activé, ajuste la couleur selon la vitesse du lien. Il peut aussi tester la connectivité à la passerelle si configuré.

### 3.4. Power LED

`ugreen-led-manager-power.service` est un service **`Type=oneshot` avec `RemainAfterExit=yes`**. Il écrit :

```text
/sys/class/leds/power/blink_type  <- none
/sys/class/leds/power/color       <- 255 0 255
/sys/class/leds/power/brightness  <- 50
```

Il attend jusqu'à environ 30 secondes que l'attribut `brightness` soit accessible. Son état normal est **`active (exited)`**, et non `active (running)`.

### 3.5. Hotplug SATA

`ugreen-led-manager-hotplug.service` lance un script Python qui écoute :

```bash
udevadm monitor --udev --property --subsystem-match=block
```

Il filtre les événements `add` et `remove` sur les disques SATA détectés dans les chemins ATA, regroupe les événements rapprochés pendant **3 secondes**, puis exécute :

```bash
systemctl restart ugreen-diskiomon.service
```

**Test réel confirmé :** ajout `/dev/sde`, rafraîchissement trois secondes après ; retrait `/dev/sde`, nouveau rafraîchissement trois secondes après.

### 3.6. Verrou anti-double-instance

`ugreen-diskiomon` utilise `/run/ugreen-diskiomon.lock`. Avant son démarrage, `ugreen-led-manager-lockcheck` :

- laisse démarrer si aucun verrou n'existe ;
- refuse de supprimer le verrou si un autre processus `ugreen-diskiomon` est encore présent ;
- supprime le verrou s'il est **orphelin**.

Le message `UGREEN: removed stale diskiomon lock` est normal lorsqu'un ancien verrou a été nettoyé.

### 3.7. Persistance du mode ON/OFF

Le mode OFF est matérialisé par :

```text
/var/lib/ugreen-led-complete/disabled
```

Les services concernés exécutent `ExecCondition=/usr/libexec/ugreen-led-enabled`, qui teste l'absence de ce fichier. En mode OFF, `ugreen-led-control` arrête les services et force les LED à zéro. En mode ON, il efface le marqueur et redémarre les services.

**Attention :** le script `ugreen-led-control status` vérifie le marqueur et l'état systemd ; il ne mesure pas à lui seul la couleur ou l'état physique réel de chaque LED.

## 4. Installation neuve (aucun ancien paquet UGREEN LED)

### 4.1. Prérequis

Vérifier l'architecture, le noyau, les en-têtes, DKMS et la présence du paquet :

```bash
uname -m
uname -r
dpkg -l dkms linux-headers-$(uname -r) 2>/dev/null || true
ls -l /lib/modules/$(uname -r)/build
ls -lh ./ugreen-led-complete_1.0.2_amd64.deb
```

Si nécessaire, installer les prérequis depuis les dépôts Debian appropriés :

```bash
apt update
apt install dkms build-essential "linux-headers-$(uname -r)" \
  dmidecode smartmontools bash python3 systemd udev util-linux \
  iproute2 iputils-ping kmod
```

**Note :** `i2c-tools` est installé automatiquement par APT avec le `.deb` 1.0.2 ; il n’est pas nécessaire de l’installer séparément. Le service de détection charge `i2c-dev` avec `modprobe -v i2c-dev` lorsque le module n’est pas déjà chargé.

**Attention :** avec un noyau backports, le paquet `linux-headers-$(uname -r)` doit exister dans les dépôts configurés ; ne pas remplacer arbitrairement par des en-têtes d'un autre noyau.

### 4.2. Simulation et installation

```bash
apt -s install ./ugreen-led-complete_1.0.2_amd64.deb
apt install ./ugreen-led-complete_1.0.2_amd64.deb
```

Le `postinst` :

1. Crée `/etc/ugreen-leds.conf` depuis l'exemple **uniquement si le fichier n'existe pas**.
2. Vérifie si `led-ugreen/0.3` est installé via DKMS pour **le noyau en cours**.
3. Si nécessaire, enregistre le module DKMS puis le compile/installe.
4. Exécute `systemctl daemon-reload`.
5. **Ne migre pas automatiquement les anciens services personnalisés.**

### 4.3. Configuration avant activation

```bash
cp -a /etc/ugreen-leds.conf /root/ugreen-leds.conf.initial.bak
nano /etc/ugreen-leds.conf
```

Adapter le mapping et les couleurs avant d'activer. Sur ce NAS, l'interface réseau utilisée est `enp89s0` ; le nom est actuellement fixé dans les unités et dans le script de contrôle.

### 4.4. Activer les services

```bash
ugreen-led-complete-setup
ugreen-led-complete-check
/usr/sbin/ugreen-led-control status
```

Le setup active les cinq services attendus et appelle `/usr/sbin/ugreen-led-control on`. Sur installation neuve, il est également utilisable, mais sa logique de sauvegarde/migration est surtout prévue pour les anciens services locaux.

### 4.5. Validation

```bash
dkms status
lsmod | grep led_ugreen
ls /sys/class/leds/
systemctl is-active ugreen-probe-leds.service \
  ugreen-diskiomon.service \
  ugreen-netdevmon@enp89s0.service \
  ugreen-led-manager-hotplug.service \
  ugreen-led-manager-power.service
```

**Ne pas redémarrer immédiatement** si DKMS ou les services signalent une erreur ; examiner les journaux d'abord.

## 5. Migration depuis les anciens paquets / scripts personnalisés

### 5.1. Sauvegarder avant de migrer

```bash
mkdir -p /root/backup-ugreen-led
cp -a /etc/ugreen-leds.conf /root/backup-ugreen-led/ 2>/dev/null || true
cp -a /usr/local/sbin/ugreen-led-control /root/backup-ugreen-led/ 2>/dev/null || true
cp -a /usr/local/sbin/ugreen-led-hotplug-monitor /root/backup-ugreen-led/ 2>/dev/null || true
systemctl list-unit-files '*ugreen*'
dpkg -l | grep -E 'ugreen|led-ugreen'
dkms status
```

Faire également une sauvegarde externe du NAS/configuration OMV avant toute modification sur une machine en production.

### 5.2. Simuler le remplacement

```bash
apt -s install ./ugreen-led-complete_1.0.2_amd64.deb
```

**Simulation historique réellement observée sur ce NAS pour le passage aux anciens paquets vers la 1.0.1 (ne représente pas une simulation 1.0.2) :**

```text
Remv led-ugreen-dkms [0.3]
Remv led-ugreen-utils [0.3]
Inst ugreen-led-complete (1.0.1 local-deb [amd64])
Conf ugreen-led-complete (1.0.1 local-deb [amd64])
```

Le paquet déclare `Conflicts`, `Replaces` et `Provides` pour `led-ugreen-dkms`, `led-ugreen-utils` et `ugreen-led-manager`. Cela explique le remplacement par APT.

### 5.3. Installer

```bash
apt install ./ugreen-led-complete_1.0.2_amd64.deb
```

Pendant la migration constatée : l'ancien `led-ugreen-dkms` a supprimé son module, puis le `postinst` du nouveau paquet a recompilé et réinstallé `led-ugreen/0.3` pour le noyau actif.

Vérifier **avant de lancer le setup** :

```bash
dpkg-query -W ugreen-led-complete
dkms status
lsmod | grep led_ugreen
ugreen-led-complete-check
```

### 5.4. Exécuter le setup de migration

```bash
ugreen-led-complete-setup
```

Ce script :

- crée une sauvegarde horodatée sous `/var/backups/ugreen-led-complete/YYYYMMDD-HHMMSS/` ;
- sauvegarde la configuration et plusieurs scripts/unités locaux s'ils existent ;
- désactive et arrête `ugreen-led-hotplug.service` et `ugreen-power-led.service` ;
- déplace l'ancien `override.conf` de `ugreen-diskiomon` s'il est encore présent ;
- déplace une éventuelle règle `/etc/udev/rules.d/90-ugreen-led-hotplug.rules` vers la sauvegarde ;
- recharge systemd et active les cinq services du nouveau paquet ;
- allume les LED.

**Précision :** le script **désactive** les anciens services, mais ne les masque pas (`mask`) malgré un commentaire trompeur dans son code. Les fichiers d'unités personnalisées restent sur disque. La sauvegarde n'est pas un système de rollback automatique.

**Sauvegarde observée sur ce NAS :**

```text
/var/backups/ugreen-led-complete/20261118-215901
```

### 5.5. Corriger la priorité des anciens scripts

Sur le NAS, `type -a` a montré :

```text
/usr/local/sbin/ugreen-led-control    <- ancien script prioritaire
/usr/sbin/ugreen-led-control          <- nouveau script du paquet
/sbin/ugreen-led-control              <- généralement même fichier via usrmerge
```

L'ancien script a été renommé :

```bash
mv /usr/local/sbin/ugreen-led-control \
  /usr/local/sbin/ugreen-led-control.bak
hash -r
type -a ugreen-led-control
ugreen-led-control status
```

Après correction, `ugreen-led-control status` doit afficher `Mode: ON` et les cinq services du nouveau paquet. **Conserver le `.bak`** et vérifier les automatisations (SSH/Home Assistant/cron) qui utilisaient l'ancien chemin absolu.

### 5.6. Vérification après redémarrage

```bash
dpkg-query -W ugreen-led-complete
dkms status
ugreen-led-control status
ugreen-led-complete-check
cat /sys/class/leds/power/color
cat /sys/class/leds/power/brightness
```

**Résultats réellement observés après migration vers la 1.0.2 :** version `1.0.2`, DKMS installé pour `7.2.12+deb13-amd64`, cinq services actifs, Power `255 0 255` et `50`, Hotplug SATA opérationnel.

## 6. Commandes principales de gestion LED

> Exécuter en `root` (ou avec `sudo`), sauf simples commandes de lecture autorisées.

| Action | Commande |
|---|---|
| Allumer toutes les LED gérées | `ugreen-led-control on` |
| Éteindre toutes les LED gérées | `ugreen-led-control off` |
| Statut général | `ugreen-led-control status` |
| Diagnostic paquet | `ugreen-led-complete-check` |
| Migration / activation initiale | `ugreen-led-complete-setup` |
| Test OFF → ON (5 secondes) | `ugreen-led-control off; sleep 5; ugreen-led-control on` |
| Utiliser explicitement le bon script | `/usr/sbin/ugreen-led-control status` |
| Vérifier la résolution de la commande | `type -a ugreen-led-control` |

**Attention :** `off` coupe la surveillance LED et éteint les LED, **mais n'arrête pas les disques, le RAID, le réseau ou Docker**. Le service de détection matérielle `ugreen-probe-leds` n'est pas arrêté par la commande OFF.

## 7. Référence exhaustive des services systemd

| Service | Rôle | État attendu après démarrage |
|---|---|---|
| `ugreen-probe-leds.service` | Chargement module et détection I²C | `active (exited)` |
| `ugreen-diskiomon.service` | Activité/état disques et LED | `active (running)` |
| `ugreen-netdevmon@enp89s0.service` | LED trafic et lien réseau | `active (running)` |
| `ugreen-led-manager-hotplug.service` | Événements SATA add/remove | `active (running)` |
| `ugreen-led-manager-power.service` | Power violet 50 % | `active (exited)` |

### 7.1. Commandes applicables à chaque service

Remplacer `<SERVICE>` par le nom complet d'un service du tableau :

```bash
systemctl status <SERVICE> --no-pager --full
systemctl is-active <SERVICE>
systemctl is-enabled <SERVICE>
systemctl start <SERVICE>
systemctl stop <SERVICE>
systemctl restart <SERVICE>
systemctl enable <SERVICE>
systemctl disable <SERVICE>
systemctl enable --now <SERVICE>
systemctl disable --now <SERVICE>
systemctl cat <SERVICE>
systemctl show <SERVICE> -p ActiveState -p SubState -p Result
journalctl -u <SERVICE> -n 100 --no-pager
journalctl -u <SERVICE> -b --no-pager
journalctl -fu <SERVICE>
```

**Ne pas utiliser `stop`, `disable` ou `mask` au hasard** : arrêter le service disques désactive son rafraîchissement ; arrêter Hotplug désactive la prise en compte automatique des ajouts/retraits ; désactiver `probe` peut empêcher l'initialisation au prochain démarrage.

### 7.2. Exemples copiables, service par service

**Initialisation du matériel :**

```bash
systemctl status ugreen-probe-leds.service --no-pager
systemctl restart ugreen-probe-leds.service
journalctl -u ugreen-probe-leds.service -b --no-pager
```

**Disques :**

```bash
systemctl status ugreen-diskiomon.service --no-pager
systemctl restart ugreen-diskiomon.service
journalctl -fu ugreen-diskiomon.service
systemctl cat ugreen-diskiomon.service
```

**Réseau :**

```bash
systemctl status ugreen-netdevmon@enp89s0.service --no-pager
systemctl restart ugreen-netdevmon@enp89s0.service
journalctl -fu ugreen-netdevmon@enp89s0.service
```

**Hotplug SATA :**

```bash
systemctl status ugreen-led-manager-hotplug.service --no-pager
systemctl restart ugreen-led-manager-hotplug.service
journalctl -fu ugreen-led-manager-hotplug.service
```

**Power :**

```bash
systemctl status ugreen-led-manager-power.service --no-pager
systemctl restart ugreen-led-manager-power.service
systemctl show ugreen-led-manager-power.service \
  -p Type -p RemainAfterExit -p ActiveState -p SubState -p Result
```

**Vue synthétique :**

```bash
systemctl is-active \
  ugreen-probe-leds.service \
  ugreen-diskiomon.service \
  ugreen-netdevmon@enp89s0.service \
  ugreen-led-manager-hotplug.service \
  ugreen-led-manager-power.service

systemctl list-unit-files '*ugreen*'
systemctl --failed
```

### 7.3. Anciens services à laisser désactivés

```text
ugreen-power-led.service     ancien service Power personnalisé
ugreen-led-hotplug.service   ancien service Hotplug personnalisé
```

Vérification :

```bash
systemctl is-enabled ugreen-power-led.service ugreen-led-hotplug.service || true
systemctl is-active ugreen-power-led.service ugreen-led-hotplug.service || true
```

Ne pas les réactiver simultanément avec les nouveaux services : risque de commandes concurrentes sur les LED et de redémarrages multiples du moniteur disques.

## 8. Configuration `/etc/ugreen-leds.conf`

Le fichier est lu par `ugreen-diskiomon` et `ugreen-netdevmon` (scripts Bash qui font `source` de ce fichier). **Ne mettre que des affectations de variables de confiance** : un contenu malveillant pourrait exécuter du shell avec les droits du service.

### 8.1. Paramètres des disques

| Variable | Utilité | Exemple / défaut du modèle |
|---|---|---|
| `MAPPING_METHOD` | Méthode de correspondance | `ata` (`hctl` et `serial` possibles) |
| `DISK_SERIAL` | Séries des disques si `serial` | `"SN1 SN2 SN3 SN4"` |
| `LED_REFRESH_INTERVAL` | Intervalle activité | `0.1` s |
| `BRIGHTNESS_DISK_LEDS` | Luminosité (1–255) | `255` |
| `COLOR_DISK_HEALTH` | Disque sain | `"255 255 255"` |
| `COLOR_DISK_UNAVAIL` | Disque indisponible | `"255 0 0"` |
| `COLOR_DISK_STANDBY` | Veille disque | `"0 0 255"` |
| `COLOR_SMART_FAIL` | SMART défavorable | `"255 0 0"` |
| `CHECK_SMART` | Vérification SMART | `true` |
| `CHECK_SMART_INTERVAL` | Fréquence SMART | `360` s |
| `CHECK_DISK_ONLINE_INTERVAL` | Vérification présence | `5` s |
| `CHECK_ZPOOL` | Contrôle ZFS (si applicable) | `false` |
| `CHECK_ZPOOL_INTERVAL` | Fréquence contrôle ZFS | `5` s |
| `COLOR_ZPOOL_FAIL` | Couleur ZFS dégradé | `"255 0 0"` |
| `STANDBY_CHECK_INTERVAL` | Contrôle veille | `1` s |

**Remarque :** `STANDBY_MON_PATH` apparaît dans le modèle, mais le fichier `ugreen-check-standby` **n'est pas présent** dans l'archive 1.0.1 inspectée. Vérifier son existence et les conditions d'activation de cette fonctionnalité avant de compter sur une surveillance de veille.

### 8.2. Paramètres réseau

| Variable | Utilité | Exemple / défaut du modèle |
|---|---|---|
| `NETDEV_BLINK_TX` | Clignotement émission | `1` |
| `NETDEV_BLINK_RX` | Clignotement réception | `1` |
| `NETDEV_BLINK_INTERVAL` | Intervalle clignotement | `200` ms |
| `BRIGHTNESS_NETDEV_LED` | Luminosité (1–255) | `255` |
| `COLOR_NETDEV_NORMAL` | Couleur standard | `"255 165 0"` |
| `CHECK_LINK_SPEED` | Adapter couleur à la vitesse | `false` |
| `CHECK_NETDEV_INTERVAL` | Contrôle lien/passerelle | `60` s |
| `CHECK_GATEWAY_CONNECTIVITY` | Ping passerelle | `false` |
| `COLOR_NETDEV_GATEWAY_UNREACHABLE` | Passerelle inaccessible | `"255 0 0"` |
| `COLOR_NETDEV_LINK_100` | Lien 100 Mb/s | `"0 255 0"` |
| `COLOR_NETDEV_LINK_1000` | Lien 1 Gb/s | `"0 0 255"` |
| `COLOR_NETDEV_LINK_2500` | Lien 2,5 Gb/s | `"255 255 0"` |
| `COLOR_NETDEV_LINK_10000` | Lien 10 Gb/s | `"255 255 255"` |

**Configuration personnalisée précédemment utilisée sur ce NAS** (à vérifier contre le fichier actuellement présent) :

```bash
MAPPING_METHOD=ata
BRIGHTNESS_DISK_LEDS="50"
COLOR_DISK_HEALTH="0 255 0"
COLOR_DISK_UNAVAIL="255 0 0"
COLOR_DISK_STANDBY="0 0 255"
CHECK_SMART=true
CHECK_SMART_INTERVAL=360
CHECK_LINK_SPEED=true
BRIGHTNESS_NETDEV_LED="50"
COLOR_NETDEV_LINK_100="0 255 0"
COLOR_NETDEV_LINK_1000="0 0 255"
COLOR_NETDEV_LINK_2500="255 255 0"
COLOR_NETDEV_LINK_10000="255 255 255"
```

**Ce bloc est un extrait explicatif, pas un fichier complet à écraser tel quel.** Conserver les autres paramètres existants.

### 8.3. Modifier et appliquer la configuration

```bash
cp -a /etc/ugreen-leds.conf \
  "/etc/ugreen-leds.conf.bak.$(date +%Y%m%d-%H%M%S)"
nano /etc/ugreen-leds.conf
bash -n /etc/ugreen-leds.conf
systemctl restart ugreen-diskiomon.service
systemctl restart ugreen-netdevmon@enp89s0.service
```

**La LED Power n'est pas paramétrée par ce fichier.** Sa couleur et sa luminosité sont écrites directement dans `ugreen-led-manager-power.service`.

## 9. Contrôle direct des LED par sysfs (avancé)

### 9.1. Lire les valeurs sans modifier

```bash
ls /sys/class/leds/
for led in power netdev disk{1..8}; do
  p="/sys/class/leds/$led"
  [ -d "$p" ] || continue
  echo "=== $led ==="
  for a in brightness max_brightness color blink_type trigger; do
    [ -r "$p/$a" ] && { printf '%s: ' "$a"; cat "$p/$a"; }
  done
done
```

### 9.2. Modifier temporairement une LED

```bash
# Exemple : LED Power violette à 50
printf 'none\n' > /sys/class/leds/power/blink_type
printf '255 0 255\n' > /sys/class/leds/power/color
printf '50\n' > /sys/class/leds/power/brightness

# Exemple : LED disk1 verte à 50 (test temporaire)
printf '0 255 0\n' > /sys/class/leds/disk1/color
printf '50\n' > /sys/class/leds/disk1/brightness
```

**Précautions :** ces modifications peuvent être écrasées par les services de surveillance ; elles ne sont pas persistantes. Éviter de changer les couleurs de santé des disques en production sans comprendre les conséquences : une LED verte forcée pourrait masquer un avertissement SMART. Pour tester le mapping physique, arrêter temporairement le moniteur disques, noter l'état initial et le redémarrer ensuite.

### 9.3. Afficher les attributs disponibles

```bash
ls -la /sys/class/leds/power/
ls -la /sys/class/leds/netdev/
ls -la /sys/class/leds/disk1/
```

Ne pas supposer que tous les attributs existent pour chaque LED ou chaque version de pilote.

## 10. DKMS, noyau et mises à jour

```bash
# Module installé et compilé
dkms status -m led-ugreen -v 0.3

# Module effectivement chargé
lsmod | grep led_ugreen

# Noyau courant
uname -r

# Sources DKMS
ls -la /usr/src/led-ugreen-0.3/

# Modules sur disque
find "/lib/modules/$(uname -r)" -iname '*led*ugreen*'

# Journal du dernier build (si présent)
find /var/lib/dkms/led-ugreen/0.3 -name make.log -print
```

Le fichier `dkms.conf` contient notamment `AUTOINSTALL="yes"` : DKMS est conçu pour reconstruire le module lors des installations de noyau. **Ce n'est pas une garantie de compatibilité** avec un nouveau noyau ; vérifier les en-têtes, la compilation et le chargement après chaque mise à jour majeure.

Si le module manque après une mise à jour de noyau :

```bash
uname -r
dkms status
ls -l "/lib/modules/$(uname -r)/build"
```

**Ne pas lancer `dkms remove --all` en diagnostic :** cela supprimerait les installations DKMS sur tous les noyaux enregistrés. Pour une réparation ciblée, identifier d'abord le noyau et le message d'erreur exact.

## 11. Journaux, erreurs courantes et dépannage

### 11.1. Diagnostic rapide

```bash
ugreen-led-complete-check
journalctl -b -u ugreen-probe-leds.service \
  -u ugreen-diskiomon.service \
  -u ugreen-netdevmon@enp89s0.service \
  -u ugreen-led-manager-hotplug.service \
  -u ugreen-led-manager-power.service --no-pager
```

### 11.2. `lsmod: ERROR ... /sys/module/sunrpc/holders`

Message observé pendant `ugreen-probe-leds`. Dans les tests réalisés, il **n'a pas empêché** le module `led_ugreen` de se charger ni la découverte de `/dev/i2c-0`. Vérifier les autres lignes du journal avant de le considérer comme bloquant.

### 11.3. `UGREEN: removed stale diskiomon lock`

Le script de pré-démarrage a trouvé un verrou sans processus correspondant et l'a supprimé. **Normal après certains redémarrages du service.** Si le service refuse de démarrer, examiner les processus et le verrou :

```bash
ps -ef | grep '[u]green-diskiomon'
ls -l /run/ugreen-diskiomon.lock 2>/dev/null || true
journalctl -u ugreen-diskiomon.service -n 80 --no-pager
```

Ne pas supprimer le verrou à l'aveugle pendant qu'un moniteur fonctionne.

### 11.4. Service Power `inactive (dead)`

Avec `Type=oneshot` et `RemainAfterExit=yes`, l'état attendu **après démarrage réussi** est `active (exited)`. Si `inactive`, vérifier :

```bash
systemctl show ugreen-led-manager-power.service \
  -p Type -p RemainAfterExit -p Result -p ActiveState -p SubState
journalctl -u ugreen-led-manager-power.service -n 30 --no-pager
systemctl start ugreen-led-manager-power.service
```

Un arrêt explicite via `ugreen-led-control off` produit normalement `inactive` ; le test instrumenté `off → on` a confirmé le retour à `active`.

### 11.5. Mapping disques incorrect

```bash
lsblk -o NAME,SIZE,MODEL,SERIAL,TRAN
lsblk -S -o NAME,HCTL,SERIAL,TRAN
ls -l /sys/block/sd*/device 2>/dev/null
journalctl -u ugreen-diskiomon.service -n 100 --no-pager
```

Après un Hotplug, les noms `/dev/sda`, `/dev/sdb`, etc. peuvent changer. **Toujours recouper avec les numéros de série et les emplacements physiques.** Un mapping incorrect peut rendre trompeuse une LED d'alerte.

### 11.6. Les LED restent éteintes

```bash
/usr/sbin/ugreen-led-control status
ls -l /var/lib/ugreen-led-complete/disabled 2>/dev/null || true
lsmod | grep led_ugreen
ls /sys/class/leds/
systemctl status ugreen-probe-leds.service --no-pager
```

Si le marqueur `disabled` est présent, c'est le mode OFF ; utiliser `/usr/sbin/ugreen-led-control on` pour réactiver proprement.

### 11.7. Vérifier l'ancien script prioritaire

```bash
type -a ugreen-led-control
ls -l /usr/local/sbin/ugreen-led-control* /usr/sbin/ugreen-led-control 2>/dev/null
```

Sur ce NAS, l'ancien `/usr/local/sbin/ugreen-led-control` masquait le nouveau script. Il a été renommé en `.bak`.

## 12. Sauvegardes et désinstallation

### 12.1. Où sont les sauvegardes ?

```text
/var/backups/ugreen-led-complete/
  +-- preinstall-YYYYMMDD-HHMMSS/  copie préinstallation
  +-- YYYYMMDD-HHMMSS/             sauvegarde du setup

/usr/local/sbin/ugreen-led-control.bak  ancien script (sauvegarde manuelle)
```

**Limite constatée dans le paquet 1.0.1 :** `preinst` crée un dossier `preinstall-<date>`, alors que `postinst` cherche, si la configuration est absente, un chemin fixe `preinstall/ugreen-leds.conf`. Ce chemin ne correspond pas au dossier horodaté. En pratique, une configuration déjà présente est conservée ; **ne pas compter sur une restauration automatique depuis la sauvegarde horodatée** si le fichier manque.

### 12.2. Examiner le contenu des sauvegardes

```bash
find /var/backups/ugreen-led-complete -maxdepth 5 -type f -print
```

### 12.3. Désinstaller (à préparer, pas à faire sans raison)

```bash
apt -s remove ugreen-led-complete
```

Le script `prerm` du paquet arrête/désactive les deux services manager et supprime l'enregistrement DKMS `led-ugreen/0.3` pour tous les noyaux (`dkms remove --all`). **Ne pas désinstaller en pensant conserver automatiquement le pilote.** Une restauration des anciens paquets/services devra être planifiée séparément ; les sauvegardes ne restaurent rien toutes seules.

## 13. Exemple d'intégration Home Assistant par SSH

Le conteneur Home Assistant peut exécuter à distance la commande **du nouveau paquet** :

```bash
/usr/sbin/ugreen-led-control off
/usr/sbin/ugreen-led-control on
/usr/sbin/ugreen-led-control status
```

**Important :** les commandes exigent les droits `root`. Pour l'intégration, préférer un compte SSH dédié avec une règle `sudoers` limitée aux commandes nécessaires, plutôt qu'une connexion root générale. Vérifier le chemin absolu dans les automatisations : l'ancien `/usr/local/sbin/ugreen-led-control` a été renommé.

**Test manuel de la commande sur le NAS :**

```bash
/usr/sbin/ugreen-led-control off; sleep 5; /usr/sbin/ugreen-led-control on
```

Le paramétrage exact du conteneur Home Assistant, des clés SSH et du `sudoers` dépend de son déploiement ; il n'est pas inclus dans le `.deb`.

## 14. Fiche mémo — commandes essentielles

```bash
# Version du paquet
dpkg-query -W ugreen-led-complete

# Etat du pilote
dkms status
lsmod | grep led_ugreen

# Allumer / éteindre / statut
/usr/sbin/ugreen-led-control on
/usr/sbin/ugreen-led-control off
/usr/sbin/ugreen-led-control status

# Diagnostic général
ugreen-led-complete-check

# Redémarrer les moniteurs sans redémarrer le NAS
systemctl restart ugreen-diskiomon.service
systemctl restart ugreen-netdevmon@enp89s0.service
systemctl restart ugreen-led-manager-hotplug.service

# Réappliquer Power violet à 50 %
systemctl restart ugreen-led-manager-power.service

# Journaux temps réel
journalctl -fu ugreen-diskiomon.service
journalctl -fu ugreen-led-manager-hotplug.service

# Valeurs matérielles Power
cat /sys/class/leds/power/color
cat /sys/class/leds/power/brightness

# Interface et vitesse réseau
ip -br link show enp89s0
cat /sys/class/net/enp89s0/speed

# Voir la configuration effective des services
systemctl cat ugreen-diskiomon.service
systemctl cat ugreen-led-manager-power.service

# Sauvegardes
find /var/backups/ugreen-led-complete -type f
```

---

## 15. Historique de validation — DXP6800 Pro

| Test | Résultat observé |
|---|---|
| Simulation APT de migration | Retrait des deux anciens paquets, installation du nouveau |
| Installation `1.0.1` | Réussie (historique) |
| Mise à niveau `1.0.1` → `1.0.2` | Réussie le 18/11/2026 ; aucun paquet supprimé |
| `i2c-tools` dans les dépendances 1.0.2 | Confirmé par `dpkg-query` |
| `i2c-tools` installé | Version `4.4-2` |
| `i2cdetect` disponible | `/usr/sbin/i2cdetect` |
| `i2c_dev` chargé | Confirmé par `lsmod` |
| Reconstruction DKMS `0.3` | Réussie sur `7.2.12+deb13-amd64` |
| `ugreen-led-complete-setup` | Réussi ; sauvegarde créée |
| `ugreen-led-control off/on` | Test réussi ; Power confirmé actif après test instrumenté |
| Redémarrage NAS | Services actifs au retour |
| LED Power | `255 0 255`, luminosité `50` |
| Hotplug SATA `/dev/sde` | Ajout et retrait détectés ; relance diskiomon après 3 s |
| Priorité script ancien/nouveau | Ancien `/usr/local/sbin` renommé en `.bak` |
| Correspondance physique de chaque baie | **À contrôler manuellement** |

**État de référence :** paquet opérationnel sur cette configuration. Conserver le `.deb` et les sauvegardes avant toute évolution du noyau, du pilote ou des services.

---

## 16. Mise à jour 1.0.2 — installation autonome et vérifications I²C

### 16.1. Changement par rapport à la 1.0.1

**La version 1.0.2 ajoute `i2c-tools` à `Depends`**, afin qu’une réinstallation de Debian 13 / OMV 8 n’exige plus la commande manuelle `apt install -y i2c-tools`. `i2c-tools` fournit notamment `i2cdetect`, appelé par le script de détection du matériel.

Le module **`i2c-dev` n’est pas un paquet APT**. Le script `/usr/bin/ugreen-probe-leds` vérifie son chargement et appelle `modprobe -v i2c-dev` si nécessaire ; il effectue une vérification analogue pour `led-ugreen`. Un `modprobe` manuel n’est donc pas nécessaire dans le déroulé normal.

Dépendances réellement déclarées dans le paquet 1.0.2 :

```text
dkms, dmidecode, smartmontools, bash, python3, systemd, udev, util-linux, i2c-tools
```

### 16.2. Procédure recommandée après réinstallation complète d’OMV 8

Exécuter en root, depuis le répertoire où se trouve le fichier `.deb` :

```bash
apt update
uname -r
ls -ld "/lib/modules/$(uname -r)/build"
# Si le lien build manque, installer les headers EXACTS du noyau actif
apt install build-essential "linux-headers-$(uname -r)"
apt install ./ugreen-led-complete_1.0.2_amd64.deb
ugreen-led-complete-setup
ugreen-led-complete-check
```

**Si `linux-headers-$(uname -r)` est introuvable**, ne pas installer au hasard les headers d’un autre noyau. Vérifier la provenance du noyau, les dépôts APT et la disponibilité de ses en-têtes avant de poursuivre. Le succès de DKMS sur `7.2.12+deb13-amd64` ne garantit pas une compilation sur un autre noyau.

### 16.3. Vérification après installation ou mise à niveau

```bash
dpkg-query -W -f='${Package} ${Version}\n${Depends}\n' ugreen-led-complete
dpkg-query -W i2c-tools
command -v i2cdetect
lsmod | grep i2c_dev
dkms status
ugreen-led-control status
ugreen-led-complete-check
```

Résultats **réellement obtenus** sur le NAS le 18/11/2026 :

```text
ugreen-led-complete 1.0.3
dkms, dmidecode, smartmontools, bash, python3, systemd, udev, util-linux, i2c-tools
i2c-tools       4.4-2
/usr/sbin/i2cdetect
i2c_dev                28672  0
led-ugreen/0.3, 7.2.12+deb13-amd64, x86_64: installed
```

Les cinq services étaient actifs au contrôle après mise à niveau, et le mode était `ON`. Le setup a créé la sauvegarde :

```text
/var/backups/ugreen-led-complete/20261118-222217
```

### 16.4. Messages APT non bloquants rencontrés

- **`apt-listchanges` ne trouve pas le changelog de la version locale 1.0.2** : cela n’a pas empêché l’installation, confirmée par `Paramétrage de ugreen-led-complete (1.0.2)`.
- **Téléchargement hors bac à sable `_apt`** : le `.deb` était placé sous `/root`, inaccessible à `_apt` ; APT a continué en root. Pour éviter cet avertissement, placer le fichier dans un répertoire accessible à `_apt`.
- **`lsmod` signale `/sys/module/sunrpc/holders`** : malgré cet avertissement observé, `ugreen-probe-leds.service` a terminé avec `status=0/SUCCESS` et `/dev/i2c-0` a été trouvé. Surveiller seulement si la détection ou les LED cessent de fonctionner.

### 16.5. Portée de la validation

- **Confirmé** : migration de 1.0.1 vers 1.0.2 sur le NAS actuel, dépendance `i2c-tools`, module `i2c_dev`, DKMS, services et Hotplug SATA.
- **Non encore confirmé** : installation de 1.0.2 sur une machine Debian 13 / OMV 8 totalement vierge, sans les anciens paquets ni la configuration préexistante.
- **À vérifier** : mapping physique des quatre baies HDD, et disponibilité des headers du noyau après une future réinstallation.


---

## 17. Nouveautés v1.0.3 — Détection de veille des HDD (validée sur le NAS)

**Configuration réelle testée :** UGREEN DXP6800 Pro, Debian 13 / OMV 8, noyau
`7.2.12+deb13-amd64`, disque de test SATA `/dev/sde` identifié par
`ugreen-diskiomon` comme **`disk6`**. Ce mappage n'est pas universel :
les noms `/dev/sdX` peuvent changer.

### Principe

La version 1.0.3 ajoute le programme Python `/usr/bin/ugreen-check-standby`,
lancé automatiquement comme processus enfant de `ugreen-diskiomon.service`.
Il interroge les disques avec :

```bash
smartctl -n standby -i /dev/sde
```

Le mode `-n standby` évite une interrogation SMART normale lorsqu'un disque ATA
est déjà endormi. Cela ne garantit pas qu'aucun autre composant du NAS ne réveille
le disque (RAID, services Docker, contrôle SMART indépendant, etc.).

**La veille n'est pas déclenchée par ce programme.** Il observe seulement
l'état et ajuste la couleur si elle correspond à une couleur normale/veille.
Les couleurs de défaut SMART ou d'indisponibilité sont préservées.

### Cycle complet observé

| État | Résultat SMART / utilisateur | Couleur `disk6` |
|---|---|---|
| Disque sain et actif | Couleur normale configurée | **Vert : `0 255 0`** |
| Mise en veille via `hdparm -y /dev/sde` | `Device is in STANDBY mode, exit(2)` | **Bleu : `0 0 255`** |
| Disque réveillé | Retour confirmé par l'utilisateur | **Vert : `0 255 0`** |
| Alerte SMART / indisponibilité | Couleur d'alerte conservée par le helper | **Rouge : `255 0 0`**, selon les paramètres |

**Important :** l'exemple livré par le paquet peut définir une autre couleur
pour `COLOR_DISK_HEALTH` (blanc). Sur le NAS testé, la configuration existante
`/etc/ugreen-leds.conf` définit explicitement `COLOR_DISK_HEALTH="0 255 0"`.
C'est pourquoi le retour au vert est **normal**, pas une anomalie.

### Paramètres vérifiés sur le NAS

```bash
STANDBY_MON_PATH=/usr/bin/ugreen-check-standby
STANDBY_CHECK_INTERVAL=30
COLOR_DISK_HEALTH="0 255 0"
COLOR_DISK_UNAVAIL="255 0 0"
COLOR_DISK_STANDBY="0 0 255"
COLOR_SMART_FAIL="255 0 0"
CHECK_SMART=true
CHECK_SMART_INTERVAL=360
```

La configuration installée avait initialement `STANDBY_CHECK_INTERVAL=1`,
mais le helper **impose au minimum 30 secondes**. Le journal le confirme :

```text
ugreen-check-standby: polling interval 1s raised to 30s for disk safety
```

Pour harmoniser le fichier de configuration :

```bash
sed -i 's/^STANDBY_CHECK_INTERVAL=.*/STANDBY_CHECK_INTERVAL=30/' /etc/ugreen-leds.conf
systemctl restart ugreen-diskiomon.service
```

### Commandes utiles

```bash
# Vérifier le helper
command -v ugreen-check-standby
pgrep -af ugreen-check-standby

# Vérifier l'état sans réveil volontaire via SMART
smartctl -n standby -i /dev/sde

# Observer la LED
cat /sys/class/leds/disk6/color
watch -n 2 'cat /sys/class/leds/disk6/color'

# Journaux
journalctl -u ugreen-diskiomon.service -n 60 --no-pager
```

**Test de mise en veille manuelle (seulement sur un disque indépendant,
non monté et ne participant pas à un RAID actif)** :

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS /dev/sde
cat /proc/mdstat
hdparm -y /dev/sde
```

---

## 18. Commandes de rappel — Référence rapide (v1.0.3)

À exécuter en tant que `root` (ou avec `sudo`) sur le NAS. Les commandes de consultation ne modifient pas les LED, sauf `ugreen-led-control on|off`.

```bash
# Activer, désactiver et afficher le mode des LED
ugreen-led-control on
ugreen-led-control off
ugreen-led-control status

# Diagnostic complet et pilote DKMS
ugreen-led-complete-check
dkms status

# Afficher toutes les couleurs réellement appliquées (LED présentes uniquement)
for led in /sys/class/leds/{disk*,netdev,power}; do
    [ -f "$led/color" ] && echo "$(basename "$led"): $(cat "$led/color")"
done

# Lire une seule LED : /dev/sde était associé à disk6 lors du test
cat /sys/class/leds/disk6/color
watch -n 2 'cat /sys/class/leds/disk6/color'

# Surveiller le helper de veille et interroger SMART sans réveil volontaire
pgrep -af ugreen-check-standby
smartctl -n standby -i /dev/sde

# État des cinq services sur ce NAS (interface réseau : enp89s0)
systemctl status ugreen-probe-leds.service
systemctl status ugreen-diskiomon.service
systemctl status ugreen-netdevmon@enp89s0.service
systemctl status ugreen-led-manager-hotplug.service
systemctl status ugreen-led-manager-power.service

# Journaux de surveillance des HDD et des événements SATA
journalctl -u ugreen-diskiomon.service -n 50 --no-pager
journalctl -u ugreen-diskiomon.service -f
journalctl -u ugreen-led-manager-hotplug.service -f
```

**Couleurs réellement testées sur `/dev/sde → disk6` :** vert `0 255 0` = disque sain/actif ; bleu `0 0 255` = veille ; retour au vert après réveil. Le rouge `255 0 0` est défini pour certaines alertes SMART ou disques indisponibles. L'apparence exacte dépend du fichier `/etc/ugreen-leds.conf` ; un défaut SMART doit être confirmé dans les journaux.

**Précautions :** ne jamais forcer un disque membre d'un RAID actif en veille pour tester une LED. Les noms `/dev/sdX`, les emplacements `diskN` et l'interface réseau peuvent varier après redémarrage ou selon le modèle UGREEN.
