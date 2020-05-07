#!/bin/bash

# This script turns sysuser.d files into scriptlets mandated by Fedora
# packaging guidelines. The general idea is to define users using the
# declarative syntax but to turn this into traditional scriptlets.

user() {
    user="$1"
    uid="$2"
    desc="$3"
    group="$4"
    home="$5"
    shell="$6"

[ "$desc" = '-' ] && desc=
[ "$home" = '-' -o "$home" = '' ] && home=/
[ "$shell" = '-' -o "$shell" = '' ] && shell=/sbin/nologin

if [ "$uid" = '-' -o "$uid" = '' ]; then
    cat <<EOF
getent passwd '$user' >/dev/null || \\
    useradd -r -g '$group' -d '$home' -s '$shell' -c '$desc' '$user'
EOF
else
    cat <<EOF
if ! getent passwd '$user' >/dev/null ; then
    if ! getent passwd '$uid' >/dev/null ; then
        useradd -r -u '$uid' -g '$group' -d '$home' -s /sbin/nologin -c '$desc' '$user'
    else
        useradd -r -g '$group' -d '$home' -s /sbin/nologin -c '$desc' '$user'
    fi
fi

EOF
fi
}

group() {
    group="$1"
    gid="$2"
if [ "$gid" = '-' ]; then
    cat <<EOF
getent group '$group' >/dev/null || groupadd -r '$group'
EOF
else
    cat <<EOF
getent group '$group' >/dev/null || groupadd -f -g '$gid' -r '$group'
EOF
fi
}

parse() {
    while read line; do
        [ "${line:0:1}" = '#' -o "${line:0:1}" = ';' ] && continue
        line="${line## *}"
        [ -z "$line" ] && continue
        eval arr=( $line )
        case "${arr[0]}" in
            ('u')
                group "${arr[1]}" "${arr[2]}"
                user "${arr[1]}" "${arr[2]}" "${arr[3]}" "${arr[1]}" "${arr[4]}" "${arr[5]}"
                # TODO: user:group support
                ;;
            ('g')
                group "${arr[1]}" "${arr[2]}"
                ;;
            ('m')
                group "${arr[2]}" "-"
                user "${arr[1]}" "-" "" "${arr[2]}"
                ;;
        esac
    done
}

for fn in "$@"; do
    [ -e "$fn" ] || continue
    echo "# generated from $(basename $fn)"
    parse < "$fn"
done
