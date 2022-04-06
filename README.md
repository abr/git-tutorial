# git-tutorial

Tutorials, tools, and scripts for using Git

## Tutorials

The tutorials provided here are intended to both
get you familiar with the range of commands and options available in Git,
and to show you some of the workflows we use.
It assumes basic familiarity already with Git,
so anyone completely new to Git should do an online tutorial first.

The tutorials assume that you have the aliases in `configs/general`
added to your Git config file (see below), so make sure to do that first.

The 0th tutorial is simply a list of useful Git commands,
to give you an idea of what is out there.
It's recommended that you go through this list first,
but don't feel like you need to understand everything perfectly
before proceeding with the rest of the tutorials.

These tutorials are all using command-line Git.
While you're welcome to use a GUI on top of Git,
having a decent understanding of how things are working on the command-line
is useful even if you're using a GUI,
since Git is doing the same underlying operations in either case
and the command-line might expose you to some details that are often hidden by the GUI.

## Configs

The `configs` folder contains Git configurations that can be added to a valid
Git config location:
- `~/.gitconfig`: To add across all Git projects for user
- `project/.git/config`: To add to a specific project

## Scripts

The `scripts` folder contains scripts that can be useful
for various specialized Git purposes.
- `git-big-files`: List large files in a Git project tree. Useful for slimming down repos.
- `git-remotes-to-ssh.py`: Change remotes using `https` to `ssh`
- `git-resolve-conflit`: Resolve conflicts across whole files, taking one set
  of changes or the other, or a union of the two.
