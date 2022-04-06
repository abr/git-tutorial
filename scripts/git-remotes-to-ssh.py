#!/usr/bin/env python

from subprocess import check_output


def call(command):
    output = check_output(command)
    return output.decode("utf-8").strip()


remotes = call(["git", "remote"])
remotes = [s.strip() for s in remotes.split("\n")]

for remote in remotes:
    url = call(["git", "remote", "get-url", remote]).split("/")

    if url[0].lower() == "https:":
        assert url[1] == "", "`https:` should be followed by `//`"
        git_server = url[2]
        git_path = "/".join(url[3:])

        if git_server == "github.com":
            ssh_server = "git@%s" % git_server
        elif git_server == "gl.appliedbrainresearch.com":
            ssh_server = "git@%s:36563" % git_server
        else:
            raise RuntimeError("Unsupported git server: [%s]" % git_server)

        ssh_url = "ssh://" + ssh_server + "/" + git_path
        call(["git", "remote", "set-url", remote, ssh_url])
        print(">> Set URL for %r to %r" % (remote, ssh_url))
