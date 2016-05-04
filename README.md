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
`/srv/files/` specifies the directory the user is allowed to see. He will only be able to explore anything beneath it, but he can't escape it.  
`-rw` A normal read/write flag. By default there is only directory exploration allowed.  

## The client

The `arrrsync` client emulates an shell, but it's actually nothing else than a convenient way of exploring the remote directory with autocompletion and history.  
Currently supported commands are `ls`, `cd`, `get` and `push`. `get` and `push` are aliases for rsync with some specific flags for file transfer.

The client uses paramiko for establishing a ssh session and tries to use as much configuration from your `~/.ssh/config` as possible.
The destination for downloaded or uploaded files can be specified with `-t`. If the flag isn't given your current working directory and the remote file root will be used.

## Progress:

The commands `get` and `push` already work. But it only does with a ssh-agent and a key for the target server. I'm still looking for a convenient way to use the open paramiko ssh channel in combination with rsync.

##Completion:
Completion as a really annoying topic! I implemented basic path completion, but there are so many ways for users to write faulty paths, I stopped trying to handle all of them.  


Help or advice is really appreciated!!  
Feel free to contribute!!


Copyright &copy; 2016 Arne Beer ([@Nukesor](https://github.com/Nukesor))
