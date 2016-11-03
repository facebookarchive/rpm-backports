# Contributing to Facebook's RPM backports

## Our Development Process
This repository is synced from an internal repository. We gladly accept pull requests and will deal with the merging appropriately.

## Contributor License Agreement ("CLA")
In order to accept your pull request, we need you to submit a CLA. You only need
to do this once to work on any of Facebook's open source projects.

Complete your CLA here: <https://code.facebook.com/cla>

## Issues
We use GitHub issues to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

Facebook has a [bounty program](https://www.facebook.com/whitehat/) for the safe
disclosure of security bugs. In those cases, please go through the process
outlined on that page and do not file a public issue.

## Sending a pull request

Have a fix or feature? Awesome! When you send the pull request we suggest you
include a build output.

We will hold all contributions to the same quality and style standards as the
existing code.

### New Packages

We'd like to keep this repo focused on "core" RPM packages that are related to the base OS. These packages either require changes to the specfile or source code patches to run on CentOS 7, or are not currently packaged at all. We specifically exclude straight backports (packages that build as-is without requiring any changes) as they can be easily rebuilt from the original src.rpm as shipped by upstream.

If you would like to contribute a package, we recommend you start by filing an Issue first to avoid duplicating effort (we may have one that we can try to open-source, or other people may be writing one) before working on it.

## License
By contributing to this repository, you agree that your contributions will be
licensed in accordance to the LICENSE document in the root of this repository.
This means that specfiles will be licensed under the MIT license, and source
code changes and patches will be under the upstream license of the original
packgage.
