# Arrrsync

Arrsync is a program designed to allow secure file transfer and exploration through ssh, whilst ensuring restricted execution possibilities and strict permission handling.

## How it works

To enable access to your server through `arrrsync`, you need to add this a piece of code to your `authorized_keys` file.

        command="/usr/bin/arrrsync-server -ro /srv/files/"`

It should look like this afterwards:

        command="/usr/bin/arrrsync-server -ro /srv/files/" ssh-rsa AAAAB3NzaC1y ... vjEZqWX3w == nuke@Contamination

`command` is an ssh functionality which allows us to pipe the ssh command directly to another program, without opening a shell.  

Let's take a closer look at the command: `/usr/bin/arrrsync-server -r -w /srv/files/`

`arrrsync-server` This is the program that interprets all incoming commands and only executes those, that are allowed.  
`/srv/files/` specifies the directory the user is allowed to see. He will be able to explore everything beneath it, but he can't escape it.  
`-rw` A normal read/write flag. By default there is only directory exploration allowed.  

## The client

The `arrrsync` client emulates an shell, but it's actually nothing else than an convenient way of exploring the remote directory with autocompletion and history.  
The client supports `ls`, `cd`, `get` and `push`. `get` and `push` are aliases for rsync with some specific flags for file transfer.

The client uses paramiko for establishing a ssh session and tries to use as much configuration from your `~/.ssh/config` as possible.
The files downloaded with `get` will be stored in the directory you called `arrrsync`.
