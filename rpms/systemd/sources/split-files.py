import re, sys, os, collections

buildroot = sys.argv[1]
known_files = sys.stdin.read().splitlines()
known_files = {line.split()[-1]:line for line in known_files}

def files(root):
    os.chdir(root)
    todo = collections.deque(['.'])
    while todo:
        n = todo.pop()
        files = os.scandir(n)
        for file in files:
            yield file
            if file.is_dir() and not file.is_symlink():
                todo.append(file)

o_libs = open('.file-list-libs', 'w')
o_udev = open('.file-list-udev', 'w')
o_pam = open('.file-list-pam', 'w')
o_rpm_macros = open('.file-list-rpm-macros', 'w')
o_devel = open('.file-list-devel', 'w')
o_container = open('.file-list-container', 'w')
o_remote = open('.file-list-remote', 'w')
o_tests = open('.file-list-tests', 'w')
o_rest = open('.file-list-rest', 'w')
for file in files(buildroot):
    n = file.path[1:]
    if re.match(r'''/usr/(share|include)$|
                    /usr/share/man(/man.|)$|
                    /usr/share/zsh(/site-functions|)$|
                    /usr/share/dbus-1$|
                    /usr/share/dbus-1/system.d$|
                    /usr/share/dbus-1/(system-|)services$|
                    /usr/share/polkit-1(/actions|/rules.d|)$|
                    /usr/share/pkgconfig$|
                    /usr/share/bash-completion(/completions|)$|
                    /usr(/lib|/lib64|/bin|/sbin|)$|
                    /usr/lib.*/(security|pkgconfig)$|
                    /usr/lib/rpm(/macros.d|)$|
                    /usr/lib/firewalld(/services|)$|
                    /usr/share/(locale|licenses|doc)|             # no $
                    /etc(/pam\.d|/xdg|/X11|/X11/xinit|/X11.*\.d|)$|
                    /etc/(dnf|dnf/protected.d)$|
                    /usr/(src|lib/debug)|                         # no $
                    /run$|
                    /var(/cache|/log|/lib|/run|)$
    ''', n, re.X):
        continue
    if '/security/pam_' in n or '/man8/pam_' in n:
        o = o_pam
    elif '/rpm/' in n:
        o = o_rpm_macros
    elif re.search(r'/lib.*\.pc|/man3/|/usr/include|(?<!/libsystemd-shared-...).so$', n):
        o = o_devel
    elif '/usr/lib/systemd/tests' in n:
        o = o_tests
    elif re.search(r'''journal-(remote|gateway|upload)|
                       systemd-remote\.conf|
                       /usr/share/systemd/gatewayd|
                       /var/log/journal/remote
    ''', n, re.X):
        o = o_remote
    elif re.search(r'''mymachines|
                       machinectl|
                       systemd-nspawn|
                       import-pubring.gpg|
                       systemd-(machined|import|pull)|
                       /machine.slice|
                       /machines.target|
                       var-lib-machines.mount|
                       network/80-container-v[ez]|
                       org.freedesktop.(import|machine)1
    ''', n, re.X):
        o = o_container
    elif '.so.' in n:
        o = o_libs
    elif re.search(r'''udev(?!\.pc)|
                       hwdb|
                       bootctl|
                       sd-boot|systemd-boot\.|loader.conf|
                       bless-boot|
                       boot-system-token|
                       kernel-install|
                       vconsole|
                       backlight|
                       rfkill|
                       random-seed|
                       modules-load|
                       timesync|
                       cryptsetup|
                       kmod|
                       quota|
                       pstore|
                       sleep|suspend|hibernate|
                       systemd-tmpfiles-setup-dev|
                       network/99-default.link|
                       growfs|makefs|makeswap|mkswap|
                       fsck|
                       repart|
                       gpt-auto|
                       volatile-root|
                       verity-setup|
                       remount-fs|
                       /boot$|
                       /boot/efi|
                       /kernel/|
                       /kernel$|
                       /modprobe.d
    ''', n, re.X):
        o = o_udev
    else:
        o = o_rest

    if n in known_files:
        prefix = ' '.join(known_files[n].split()[:-1])
        if prefix:
            prefix += ' '
    elif file.is_dir() and not file.is_symlink():
        prefix = '%dir '
    elif n.startswith('/etc'):
        prefix = '%config(noreplace) '
    else:
        prefix = ''

    suffix = '*' if '/man/' in n else ''

    print(f'{prefix}{n}{suffix}', file=o)
