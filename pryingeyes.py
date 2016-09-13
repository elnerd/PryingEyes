#!/usr/bin/env python


"""
Prying Eyes is a small program that will list processes as they are created.
It will also warn you if a program tries to hide its original commandline arguments.

Example output:

$ python pryingeyes.py
pid	usr	grp	cmdline
cmdline changed from ['/usr/sbin/munin-node [::ffff:127.0.0.1]'] to ['']
14399	nobody	99	/usr/bin/sh ['/etc/munin/plugins/forks', 'config', ''] 483
cmdline changed from ['/usr/sbin/munin-node [::ffff:127.0.0.1]'] to ['']
14409	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 489
14416	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 496
14425	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 505
14428	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 508
14434	nobody	99	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 514
14437	nobody	99	/usr/bin/sh ['/etc/munin/plugins/vmstat', 'config', ''] 515
cmdline changed from ['/usr/bin/sh', '/etc/munin/plugins/vmstat', 'config', ''] to ['']
14447	nobody	99	/usr/bin/sh ['/etc/munin/plugins/vmstat', ''] 520
14446	nobody	99	vmstat ['1', '2', ''] 521
14492	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 566
cmdline changed from ['/usr/sbin/munin-node [::ffff:127.0.0.1]'] to ['']
14498	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 572
14502	nobody	99	/usr/bin/sh ['/etc/munin/plugins/entropy', 'config', ''] 574
14506	root	0	/usr/sbin/munin-node [::ffff:127.0.0.1] [] 577
cmdline changed from ['/usr/sbin/munin-node [::ffff:127.0.0.1]'] to ['']
14511	nobody	99	/bin/bash ['/etc/munin/plugins/if_enp4s0f1', 'config', ''] 581
"""
import os, string, sys, time


def GetPids():
    files = os.listdir("/proc/")
    pids = []
    # Filter process numbers only
    for file in files:
        try:
            pids.append(int(file))
        except ValueError:
            pass
    pids.sort()
    return pids


# Create dictionaries to map uid/gid to usernames
userdict = {}
groupdict = {}
for line in open("/etc/passwd").readlines():
    line = line.strip()
    if line.startswith("#"): continue
    username, _, uid, gid, _, _, _ = line.split(":")
    userdict[uid] = username
    groupdict[gid] = username


# Use fork() to identify the highest pid in use
def GetCurrentPid():
    mypid = os.fork()
    if mypid == 0:
        os.setsid()
        os._exit(0)
    else:
        os.umask(0)
        os.wait()
        return mypid


# Parse the /proc/<pid>/status file, and return the found uid and gid
def GetUidGid(pid):
    lines = open("/proc/%d/status" % pid).readlines()
    gid = None
    uid = None
    for line in lines:
        variable, value = string.split(line, ":", 1)
        if variable == "Gid":
            gid = string.split(value)[0]
        elif variable == "Uid":
            uid = string.split(value)[0]
    return uid, gid


# Main function:
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "getpid":
            sys.exit(os.getpid())
    # build a quick list of known pids, we don't want to report these.
    knownpids = GetPids()
    print "pid\tusr\tgrp\tcmdline"
    epid = 0
    while 1:
        mypid = GetCurrentPid()
        knownpids.append(mypid)
        for x in range(10):  # Repeat this look-forward function Y times.
            stime = time.time()
            for i in range(10):  # Look X pids ahead of known highest pid.
                # If this fails, then /proc/<pid>/cmdline does not exists
                try:
                    thispid = mypid + i % 65535
                    if thispid not in knownpids:
                        cmdline = None
                        for z in range(2):
                            lastline = cmdline
                            time.sleep(0.0001)
                            data = open("/proc/%d/cmdline" % (thispid)).read()
                            cmdline = string.split(data, "\x00")
                            if lastline and not cmdline == lastline:
                                print "cmdline changed from %s to %s" % (lastline, cmdline)
                        knownpids.append(thispid)
                        if not cmdline == ['']:
                            uid, gid = GetUidGid(thispid)
                            print "%d\t%s\t%s\t%s" % (
                            thispid, userdict[uid], gid, "%s %s" % (cmdline[0], cmdline[1:])), len(knownpids)
                    else:
                        pass
                except IOError:
                    if thispid in knownpids:
                        # pid used to exist, but no longer... can remove it, and maybe do something else...
                        knownpids.remove(thispid)
            etime = time.time()
            dtime = etime - stime


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print
        print "Thank you for keeping a watchful neighborhood!"
        sys.exit(0)
