# PryingEyes

A small tool that will list processes as they are created in realtime.
It will also report if a program changes its commandline arguments. This can be interesting because it is a typical way to hide sensitive information.

Works on linux with /proc/ filesystem.
Might work on other unixes with some modifications.


```
python pe.py 
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
```

