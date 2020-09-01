# Do not allow "dnf -y remove" to expand the list of packages to remove to
# include packages which require one of the explicitly listed packages.
# Fail the request instead.

import dnf
import libdnf


class Flunk_Dependent_Remove(dnf.Plugin):

    name = "flunk_dependent_remove"

    def resolved(self):
        # hook dnf after it has resolved all the RPMs to be installed, removed,
        # upgraded, etc. but before it has made any changes.
        if not self.base.conf.assumeyes:
            # If interactive (no -y option) ask the user what he wants to do
            # as usual. Only flunk dependency removal for automated requests.
            return
        remove = libdnf.transaction.TransactionItemAction_REMOVE
        install = libdnf.transaction.TransactionItemAction_INSTALL
        dependent = libdnf.transaction.TransactionItemReason_DEPENDENCY
        installcount = 0
        removecount = 0
        depcount = 0
        # check each proposed install/remove and tally up why (explicit or
        # dependency)
        for tsi in self.base.transaction:
            if tsi.action == remove:
                removecount += 1
                if tsi.reason == dependent:
                    # Nope, we'd have to remove packages we weren't asked
                    # to remove in order to remove this one.
                    depcount += 1
            else:
                installcount += 1
        if (installcount != 0) or (removecount <= 0) or (depcount <= 0):
            # no problematic removals detected
            return

        # If no removals are due to installing something new
        # And we're removing packages
        # And at least one package we weren't explicitly asked to remove
        #   requires a package we were asked to remove
        print("===========================================================")
        print("=== FAIL: INSTALLED PACKAGES DEPEND ON REMOVED PACKAGES ===")
        print("===========================================================")

        # reverse the affect of -y, causing dnf to abort the transaction
        # after helpfully printing what it wanted to do. When dnf aborts,
        # it returns status 1 letting the caller know it failed.
        self.base.conf.assumeno = True
        self.base.conf.assumeyes = False
