#--- Monitoring commands for OpsMgr role: osa_lxc_keystone

command[osa_lxc_ad] = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p keystone-ad -w 20 -c 30 -W 1 -C 1'
command[osa_lxc_se] = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p keystone-se -w 20 -c 30 -W 1 -C 1'
command[osa_lxc_apache2] = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p apache2 -w 15 -c 30 -W 1 -C 1'

command[osa_lxc_cpu]         = sudo /etc/nagios/plugins/check-lxc.sh keystone check-cpu.rb '-w 80 -c 90'
command[osa_lxc_mem]         = sudo /etc/nagios/plugins/check-lxc.sh keystone check-mem.sh '-w 250 -c 100'
command[osa_lxc_disk]        = sudo /etc/nagios/plugins/check-lxc.sh keystone check-disk.rb ''
command[osa_lxc_large_files] = sudo /etc/nagios/plugins/check-lxc.sh keystone check-for-large-files.sh '-d /var/log -s 1048576'
command[osa_lxc_slsocket]    = sudo /etc/nagios/plugins/check-lxc.sh keystone check-syslog-socket.rb ''
command[osa_lxc_eth0]        = sudo /etc/nagios/plugins/check-lxc.sh keystone check-netif.rb '-c 500 -w 350 --interfaces eth0'
command[osa_lxc_eth1]        = sudo /etc/nagios/plugins/check-lxc.sh keystone check-netif.rb '-c 500 -w 350 --interfaces eth1'
command[osa_lxc_rsyslogd]    = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p rsyslogd -w 15 -c 30 -W 1 -C 1'
command[osa_lxc_sshd]        = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p sshd -w 15 -c 30 -W 1 -C 1'
command[osa_lxc_cron]        = sudo /etc/nagios/plugins/check-lxc.sh keystone check-procs.rb '-p cron -w 15 -c 30 -W 1 -C 1'
