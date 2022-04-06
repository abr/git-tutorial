
This example demonstrates how to rebase a branch and clean up the history,
in the slightly more complicated case that some of the commits that the branch
was based off have changed in the base branch.

In our example, we are rebasing the `rebase-example-branch` branch onto the
`rebase-example-main` branch. It was originally based off this branch,
but some commits were modified and some were added to the base branch.
This simulates a scenario where you started a branch off of a base branch,
added some commits, and while you were working someone else modified and added
commits in the base branch.


## Rebasing in steps

There are two main parts to our rebase:
1. Get `rebase-example-branch` rebased onto `rebase-example-main`
2. Clean up the history of the rebased branch

While we could accomplish both these objectives with one `git rebase` command,
it often makes sense to "rebase in steps" and call `git rebase` a number of times.
This is because we will sometimes run into conflicts, and may realize that
the operations we're trying to do are not the best way of accomplishing our goal.
For example, we may be trying to change the order of commits and squash them together,
but if one of those squash commits interacts with changes that now happen after it
in the new order, things can get messy.
It can sometimes be easier in that case to abort the rebase,
and back and split up that squash commit into multiple parts, for example.
However, if we've already fixed a bunch of rebase conflicts,
then aborting the whole rebase is costly.
Thus, the fewer changes we make with one `git rebase` call, the better.

The other thing to keep in mind is that it can sometimes be easier
to do some of the history cleanup before we rebase onto the target branch.
This is because `git rebase` simply tries to apply each commit in order,
and doesn't consider the whole picture.
So if we've got a commit in our branch that modifies or even undoes earlier changes,
then when we rebase we might have to fix conflicts on those earlier changes,
only to have to then fix further related conflicts on the subsequent commit.
Having these commits already squashed means we only have to fix the conflicts once.


## Example

We start by checking out the branch we want to rebase:

    git co rebase-example-branch

Note that if you've added an additional remote (e.g. "upstream"),
Git does not know which remote to checkout from by default,
so you'll need to specify the remote branch to check out from:

    git co -b rebase-example-branch origin/rebase-example-branch

You should see a message saying that your local branch has been
set up to track the remote branch by rebasing.

We do `git pull` to make sure we have the latest
(though if this is our first time checking out the branch, we will have the latest):

    git pull

We are now ready to rebase.


### First try

At this point, you may try to just do the rebase.
Note that when we run the following command, it lists all the commits
with the first to be applied at the top.
This is the opposite order than we're used to seeing with `git lg`.

    git rebase -i origin/rebase-example-main

When you do this, you'll find that there's a conflict.
You can see what files have conflicts with `git status`,
and look at the files to see what the conflicts are.
Some text editors (e.g. emacs) are configured to color-code these diffs.

    git s
    less demo_repo/numbers.py

When we did the rebase, you may have noticed that the first commit
had the same name as one in `rebase-example-main`: "Add some demo_repo code".
We might expect these to be the same commit, however running `git lg` on each of
the two branches shows they have different hashes:

    git lg rebase-example-branch
    git lg origin/rebase-example-main

You can compare the two commits directly by doing
a `git diff` of their respective hashes.
When you do this, you'll see that the commit in `origin/rebase-example-main`
adds a `__repr__` function implementation to the `Number` class.

There's a better way to do this, so lets abort this rebase and try again.

    git rebase --abort

Our branch is now back in the state it was before we started the rebase.
(You can do `git lg` and see that
it's in the same place as `origin/rebase-example-branch`).


## Second try

For our second try, we'll start off the same.
However, we now know that `origin/rebase-example-main` has
an updated version of the "Add some demo_repo code" commit,
which happened because somebody force-pushed changes to that branch.

While that is uncommon for a main branch (we try to never force-push to `main`),
it is more common when feature branches are based off other feature branches.
For example, maybe somebody else developed a feature that you want to build off,
but their feature is not yet merged into `main`.
So you check out their feature branch,
create your own branch based off it, and get to work adding your feature.
In the mean time, their feature branch is merged into `main`,
and as part of that process the history is cleaned up and some commits are squashed.
Now, when you try to rebase your feature branch to the new `main`,
there will be commits in there that are "updated" versions
of the commits with the same names in your repo.

The solution to this is when we rebase,
we remove all the commits from the interactive rebase log
that already appear in the branch we're rebasing onto.

In our specific example, run the rebase command again,
but remove the first line (corresponding to the "Add some demo_repo code" commit)
from the interactive listing that appears.
This stops that commit from being added,
which is fine because an updated version of it
is already in the branch we're rebasing onto.

    git rebase -i origin/rebase-example-main

Now, the rebase should go ahead without any problems.


## Cleaning up the history

If you run `git lg` again, you'll notice that there are some "fixup" commits.
These commits are meant to be squashed into other commits.
We can do this automatically with the `--autosquash` argument.

    git rebase -i origin/rebase-example-main --autosquash

You'll see in the list of commits that the two fixup commits
have been put right after the commits they are fixing up,
and marked with "fixup" so that they are squashed into those commits.
Close this interactive prompt and the rebase will begin.

You should then get a message about a merge conflict in `demo_repo/numbers.py`.
If you do `git status`, it will show which files are conflicted in red,
and also tell us useful things like we're in the middle of a rebase,
and which commits have been applied.

Open up `demo_repo/numbers.py` to see the conflicted file.
You'll see a section like the following, which indicates the conflict:

    <<<<<<< HEAD
    =======
        def invert(self):
            self.value = 1 / self.value

        def _check_positive(self):
            assert self.value > 0

    >>>>>>> c3133a5... fixup! Add Float class

The top part of this section (between the `<<<<< HEAD` and `=====`)
indicates what was present in the HEAD
(the branch we're rebasing onto, plus any commits that have been successfully applied),
and the second part (between `=====` and `>>>>>`)
indicates what is present in the commit we're trying to apply.
Right after the `>>>>>`, it handily shows part of the commit hash,
as well as the name of the commit.

If you copy that hash (omit the `...`) and do `git show <hash>`,
you'll be able to see what was originally present in that commit.
In our case, it shows

         def fractional(self):
             return Float(self.value - int(self.value))

    +    def invert(self):
    +        self.value = 1 / self.value
    +
         def _check_positive(self):
             assert self.value > 0

This indicates that the `invert` function was added
in between the `fractional` and `_check_positive` functions.
However, in the conflicted version of `numbers.py`,
it's showing both the `invert` _and_ `_check_positive` functions
being added by this commit.
This is because the `_check_positive` function was added
_after_ the commit we're trying to put the fixup commit into,
but _before_ the fixup commit itself.
It thus appears as _context_ in the fixup commit,
and when we rebase, Git isn't sure what to do with it.
Typically, in a case like this, we want to modify the changes
to accomplish what the original commit was trying to accomplish.

Modify the contents of the conflicted `numbers.py` so that
it's just adding the `invert` function to the `Float` class.
Specifically, remove the `_check_positive` function,
as well as the lines starting with `<<<<<`, `=====`, and `>>>>>`.
Now that you've resolve the conflict,
do `git add demo_repo/numbers.py` to add the fix,
and `git rebase --continue` to continue the rebase.

You will encounter a second conflict,
because the commit that added the `_check_positive` command
didn't have the `invert` command present at the time,
so again the context has changed.
Modify this conflict so that
both the `invert` and `_check_positive` commands are there.

You should now be able be able to do `git rebase --continue`
and have the rebase complete successfully.
