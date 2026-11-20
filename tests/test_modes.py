#!/usr/bin/env python3
"""Offline dry-run of LED control using temporary sysfs and systemctl fixtures."""
import os, pathlib, subprocess, tempfile

PKG=pathlib.Path(__file__).resolve().parents[1]/'package'
CONTROL=(PKG/'usr/sbin/ugreen-led-control').read_text()
HELPER=(PKG/'usr/libexec/ugreen-led-enabled').read_text()
PWR_COND=(PKG/'usr/libexec/ugreen-led-power-enabled').read_text()
PWR=(PKG/'usr/libexec/ugreen-led-set-power').read_text()

with tempfile.TemporaryDirectory() as d:
    root=pathlib.Path(d)
    state=root/'state'; state.mkdir()
    sysfs=root/'sysfs'; sysfs.mkdir()
    for name in ['power','netdev','disk1','disk2','disk3','disk4']:
        led=sysfs/name; led.mkdir()
        for f in ['trigger','blink_type','brightness','color']:
            (led/f).write_text('0\n')
    bindir=root/'bin'; bindir.mkdir()
    shim=bindir/'systemctl'
    shim.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "'+str(root/'calls')+'"\nif [ "$1" = is-active ]; then echo active; fi\n')
    shim.chmod(0o755)
    rewrite=lambda s:s.replace('/var/lib/ugreen-led-complete',str(state)).replace('/sys/class/leds',str(sysfs))
    ctl=root/'control'; ctl.write_text(rewrite(CONTROL));ctl.chmod(0o755)
    cond=root/'cond';cond.write_text(rewrite(HELPER));cond.chmod(0o755)
    pcond=root/'pcond';pcond.write_text(rewrite(PWR_COND));pcond.chmod(0o755)
    power=root/'power';power.write_text(rewrite(PWR));power.chmod(0o755)
    env=os.environ.copy();env['PATH']=str(bindir)+':'+env['PATH']
    def run(path,*args):
        return subprocess.run([str(path),*args],text=True,capture_output=True,env=env)
    def mode(action,expected,brightness,monitors):
        x=run(ctl,action)
        assert x.returncode==0,(action,x.stdout,x.stderr)
        assert expected in x.stdout,(action,x.stdout)
        assert run(cond).returncode==(0 if monitors else 1)
        assert run(pcond).returncode==(1 if expected=='OFF' else 0)
        if expected!='OFF':
            y=run(power);assert y.returncode==0,y.stderr
        assert (sysfs/'power/brightness').read_text().strip()==str(brightness)
        if not monitors:
            assert (sysfs/'disk1/brightness').read_text().strip()=='0'
    mode('day','DAY',50,True)
    mode('night','NIGHT',10,False)
    assert (state/'night').exists()
    mode('restart','NIGHT',10,False)
    mode('off','OFF',0,False)
    mode('restart','OFF',0,False)
    mode('on','DAY',50,True)
    mode('night','NIGHT',10,False)
    mode('day','DAY',50,True)
    status=run(ctl,'status')
    assert 'Mode: DAY' in status.stdout
    actions=(root/'calls').read_text()
    assert 'restart ugreen-led-manager-power.service' in actions
    assert 'stop ugreen-led-manager-hotplug.service' in actions
    assert 'restart ugreen-led-manager-hotplug.service' in actions
    print('PASS: modes DAY/NIGHT/OFF, restart persistence, mode gates, power LED brightness, systemctl actions')
