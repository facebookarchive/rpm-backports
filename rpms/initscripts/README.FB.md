As of 9.49.39, CentOS7 is rebased onto Fedora master, and we are trying to
keep close to that (because many CentOS-specific changes) need to happen.

Therefore, to add patches, in the upstream initscripts repo do:

```
git format-patch <hash> --stdout -n1 > /tmp/yourpatch
```

Then in opsfiles/rpms/initscripts/sources/git do :

```
git am < /tmp/yourpatch
```

And `yummy git2spec initscripts` to generate the spec/patch changes.

When new versions come out in CentOS, reset to that, and pull in only patches
not yet in the C7 version.

