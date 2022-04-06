
For working on open-source projects, the typical Github workflow is that you
create a "fork" of the repo in your own Github account.
You can then clone and work on that fork, and when you're ready,
make a pull request (PR) back to the original repo.

While this workflow is typically not necessary with ABR repos
(since we can give you permission to write directly to branches on the repo),
we'll use it here both so that you can get familiar with having multiple remote repos,
and so that we can keep people from making their own branches on `git-tutorial`
which may make the tutorials more confusing.

For these tutorials, the only step that's necessary here is the first
"creating a fork" step.
The additional information is provided in the case where
you want to be able pull code from the original repository after cloning.


## Creating a fork

To create a fork, first bring up the target repo in your web browser.
In our case, it's: https://github.com/abr/git-tutorial .
Click the "Fork" icon in the top right.
This will bring up the dialog for creating a new fork.
Make sure the target owner is you (which should be the default);
the repo name and description can keep their default values.
Click the "Create fork" button, and you should now have a fork of the repo
in your user account.

You can now clone this repo with:

    git clone git@github.com:<your-github-username>/git-tutorial


## Setting an upstream remote

Git is a distributed version control system,
where everybody has their own copy of the repo.
Changes are then synchronized among these copies through `git pull` and `git push`.
Git allows for multiple "remote" repos,
which are repos that you can push to and pull from.
By default, when you clone a repo from Github,
the Github version of that repo will be added as the "origin" remote.
This is the default remote used when you push and pull.

You can list the remotes with the following command:

    git remote -v

Doing that in your new repo, you should see something like:

    origin	git@github.com:hunse/git-tutorial (fetch)
    origin	git@github.com:hunse/git-tutorial (push)

In the case where you've forked a repo, like we have,
you will likely also want to get code (i.e. fetch/pull)
from the original copy of that repo.
To do this, we add it as an additional remote, which we will call "upstream".

    git remote add upstream git@github.com:abr/git-tutorial

Now if you do `git remote -v` again, you should see "upstream" there as well.

You can fetch all the upstream branches with:

    git fetch upstream

You can then make local copies of these branches with something like:

    git co -b <branch-name> upstream/<branch-name>

You can also do things like fast-forward your main branch to
the new state of the upstream main branch.
Of course, this assumes that you've made no changes to your main branch.

    git co main
    git merge --ff-only upstream/main
