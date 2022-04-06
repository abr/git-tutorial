This is a list of useful Git commands.
Many of them will be explored in more depth in subsequent tutorials.
You can get more information about any command through `git <command> --help`.

For the rest of these tutorials,
we will assume that you have added the aliases in `configs/general`.
These aliases will be noted along with each command.

Notes on terminology:
- index: The index is the list of files that are managed by Git.
- remote: A remote repository is a copy of the repository that is stored remotely
  (e.g. on Github).
- working tree: The working tree is the set of files that is currently being worked on
  (a.k.a. "checked out").
- HEAD: The `HEAD` is an object that points to the commit that the working tree is on
  (i.e. the checked out commit). Can also find commits relative to it, for example
  `HEAD~3` will always be three commits earlier in the commit history. See also `git reflog`.

Notes on variables:
- `<commit-ish>`: A commit hash, branch name, tag, etc.
- `<file>` and `<dir>`: A path to a file or directory.

# Viewing commits/history

## checkout (alias: co)

`git checkout <commit-ish>` checks out a branch/commit/tag/etc., replacing all the
code in the working files with the version in that object.
- `git checkout -b <new-branch-name>`: Create a new branch with the given name at
  the current commit, and check it out.
- `git checkout -- <file>`: Checks out the most recent committed version of a file
  (i.e. discards working changes).

## status (alias: s)

`git status` shows the current status of files, split into those with staged changes,
those with unstaged changes, and those not tracked (but not ignored by `.gitignore`).

## log (concise version: lg)

`git log` lists the commits (from last to first) in a branch.
If you don't provide a branch name, defaults to the current branch.
- `git log -- <file>`: Shows the log of commits that have touched a file.
- `git log --grep=<regex>`: Grep for a particular regex pattern in commit messages.
- `git log -G<regex>`: Find commits where the regex pattern appears in any of the
  modified lines.
- `git log -S<string>`: Find commits that change the number of occurences of `<string>`.
  The string can be a regex with the additional `--pickaxe-regex` argument.

See the `git lg` alias for a more consise log,
which can also take any of the options listed above.

## diff (staged version: ds)

`git diff` shows the current unstaged changes (default),
or compares with a target commit, or compares between two commits.
- `git diff -b`: Ignore whitespace when diffing.
- `git diff --staged`: Diff staged changes. Our alias for this is `git ds`.

## show

`git show` shows a particular commit.
- `git show <commit-ish>:<file>`: Show a version of a file in command line. Can do
  normal things after like `| less` or `> my-file-copy`.
- `git show --stat`: List files and the number of lines changed only.

## reflog

`git reflog` shows the history of the working head (`HEAD`). You can reference commits
in the reflog either with their hash or with e.g. `HEAD@{3}` to go three commits back.
Can be especially useful if you think you've lost a commit or branch and want to get it back.

## ls-tree

`git ls-tree` lists files in the index.
- `git ls-tree -r --name-only <commit-ish> -- <dir>`: List files in a particular
directory in a particular commit.

## worktree

`git worktree` allows you to check out a separate version of a repo into a
subdirectory. You can then `cd` into that subdirectory and use `git` commands
to manage that working tree.
- `git worktree add <dir> <commit-ish>`: Checkout `<commit-ish>` to `<dir>`

# Making changes

## branch

`git branch` is used to list and manage branches
- `git branch`: List branches.
- `git branch --merged <commit-ish>`: List branches that are "merged" into the given
  commit/branch.
- `git branch -a --contains <commit-ish>`: List branches that contain the given commit.
- `git branch -d <branch>`: Delete a branch.
- `git branch -u <branch> <remote>/<branch>`: Set the upstream (remote) branch for a
  given branch (typically done by default when you check out a branch).

## add

`git add` adds changes to the staging area (from where they can be committed).
- `git add <file>`: Adds all the changes to the given file. Also used for adding new files.
- `git add -p`: Interactively takes you through changes to indexed files, letting you
  add or skip them. The best way to add changes to existing files, because it also makes
  you think about each change.

## rm

`git rm <file>` is used to remove a file from the index. It puts the proposed change in
the staging area, like `git add`.

## commit

`git commit` creates a new commit using the changes in the staging area. You will be
prompted to enter a commit message. We keep the title (first line) of commit messages to
50 characters, succinctly summarizing the changes. If you would like to provide more
details, you can add a commit message body with more details (put one blank line between
the title and the body).
- `git commit --amend`: Amend the most recent commit with the staged changes.
- `git commit --fixup/--squash <commit-ish>`: Adds a fixup or squash commit for the
  given target commit. Fixup commits have no message, whereas squash commits have a
  message that will be appended to the target commit message (though you'll also have a
  chance for further editing). See also `git rebase --autosquash`.
- `git commit -C HEAD@{1}`: Commit using the commit message/info from the commit at
  `HEAD@{1}` (see `reflog`). Can be very useful when used in tandem with `git reset`
  to roll back a commit, and `git add -p` to add just some of the changes, then reform
  the commit.
- `git commit --no-verify`: Skip running pre-commit hooks.

## reset

`git reset` resets the current branch to another commit. This can be an earlier commit
- `git reset HEAD^`: Roll back the most recent commit. The changes in that commit will
  become unstaged changes.
- `git reset <commit-ish> --hard`: Set the branch to `<commit-ish>`,
  and the `--hard` option **discards** any difference with the target commit.
  However, if you do this accidentally, you can still get back to the previous state
  with e.g. `git reset HEAD@{1} --hard` (see `reflog`).

## rebase

`git rebase` is used to take the commits from another b

- `git rebase -i`: Interactive rebase, allows you to reorder/squash/rename/edit/drop/etc. commits.
- `git rebase -i --autosquash`: Interactive rebase, squashing fixup and squash commits
  into their target commits.

## cherry-pick

`git cherry-pick` allows you to add specific commits to the current branch.
For example, you may want to bring a commit that you added to another branch
into your current branch as well.
You can target either a specific commit, or a range of commits.

## merge

`git merge` is not used very much when trying to maintain a linear history, as we do.
The main use is when merging a pull request,
where you will use it with the `--ff-only` option (see the "rebase-example" tutorial).
- `git merge --ff-only`: When merging, only allow the merge if it is a fast-forward
  (i.e. the branch being merged is already rebased onto the current branch).

## stash

`git stash` stores any active changes to the working tree to a "stash",
where they can be retrieved later.
- `git stash list`: List all the stash entries, and the branches they were made on.
- `git stash show -p <stash-id>`: Show all the changes in the most recent stash.
   `<stash-id>` is an optional stash identifier, to view a stash other than
   the most recent one (see `stash list`).
- `git stash pop <stash-id>`: Pop the most recent stash entry (or an earlier one if
  `<stash-id>` is provided) and apply it to the working tree.
- `git stash drop <stash-id>`: Discard the most recent stash entry
   (or an earlier one if `<stash-id>` is provided).

# Remote repositories

## remote

`git remote` allows you to view and edit associated remote repositories.
Try `git remote -v` to view current remotes.
- `git remote prune origin`: Remove `origin/` branches that are no longer on remote

## fetch

`git fetch` fetches the latest branches/commits from a remote repository.
If you have more than one remote, use `git fetch <remote>` (default is `origin`).
The fetched branches will all be named `<remote>/branch-name`.

## pull

`git pull` fetches and integrates the changes from the remote version of a branch
into the current branch.
By default, will integrate with a merge,
but you probably want to set your config file to do a rebase by default.

## push

`git push` pushes changes in a branch to the remote version of that branch.
- `git push -u origin <branch>`: Push `<branch>` to the `origin` remote,
   creating a new branch on `origin` if necessary.
- `git push --force-with-lease` (alias `git fpush`): Force pushes your changes,
   e.g. if you have rebased so your changes no longer follow directly on what exists
   in the target branch. Safer than the `--force` option, in that it checks if your
   copy of the target branch is up-to-date first.

# Advanced tools

## blame

`git blame` lets you know line-by-line in a file when that line was changed and by whom.
Some text editors may have integrations for this (e.g. Emacs is `C-x v g`).

## bisect

`git bisect` allows you to find when a change occurred in a repo, based on an external test.
For example, you can find when a unit test broke by specifying known start and stop points
(when the test was working, and when it wasn't); `git bisect` will then take you to
commits in between, you run the test, and let it know if it passed on that commit or not.

## rev-list

`git rev-list` lists commit hashes for some range of commits. Useful in scripts.

# Other information

## gitrevisions

`man gitrevisions` will tell you about different ways to specify revisions.
- `<commit-ish>^`: The commit before `<commit-ish>` in the branch.
- `<commit-ish>^^^` or `<commit-ish>~3`: Three commits before `<commit-ish>` in the branch.
- `<branch>@{1.week.ago}`: The commit pointed to by `<branch>` one week ago.
