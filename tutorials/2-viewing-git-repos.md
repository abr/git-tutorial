This tutorial dives into a number of useful tools for viewing Git repos.

## The `git lg` alias

The `git lg` alias (see `configs/general`) is incredibly useful.
It is a version of `git log` that shows each commit as a single line.

Let's compare a linear history with a non-linear history:

    git lg linear-history
    git lg nonlinear-history

## `git diff`

The `git diff` command has many different options.

### `git ds` alias

The `git ds` alias allows us to easily diff what's in the staged area.


### Diff/show options

1. The `-b` option
