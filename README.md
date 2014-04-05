svelTest
========

# Navigation
| Project & Contributors | Environment Config  | Git Workflow  |
| :------------: | :------------: |:---------------:| :-----:|
![](http://www.flaticon.com/png/256/1391.png)|![](http://www.flaticon.com/png/256/1140.png)| ![](http://www.flaticon.com/png/256/25997.png) |
| [Project & Contributors](#project--contributors) | [Environment Config](#environment-config)| [Git Workflow](#git-workflow) |
| Introducing SvelTest - why we built it and what it does | Setting up Vagrant and our own environment configurations | Our Git / GitHub workflow

## Project & Contributors

### Deliverables
1. Whitepaper ([GDOC] (https://docs.google.com/document/d/153WFuabcumkn7Wo-ne4FiyEzbwGChfMImohJrg47NK4/edit))
2. Language Tutorial ([HTML] (https://svelTest.github.io/tutorial) | [GDOC](https://docs.google.com/document/d/1Jlvgt7bFuxl1FKmwID8w9gefvy7QOWRC7YnWgSUJQVY/edit?usp=sharing))
3. Language Reference Manual ([GDOC] (https://docs.google.com/document/d/11q1Y8ffmkp-IT7JVnWYSrp-OCFPGAVzYU3rPH-81z40/edit))

### Contributors
Project Manager: Kaitlin Huben (kjh2141)

Language Guru: Emily Hsia (ejh2170)

System Architect: Joshua Lieberman (jal2238)

System Integrator: Christopher So (css2162)

Verification and Validation Person: Amanda Swinton (acs2211)

## Environment Config

### Vagrant
A getting started guide from devfest: http://squidarth.github.io/Devfest-Environment-Setup/ 

#### Vagrant with Virtualbox (basic):
1. Download Vagrant: http://www.vagrantup.com/downloads
2. Download VirtualBox: https://www.virtualbox.org/wiki/Downloads
3. Configure and run VM (http://docs.vagrantup.com/v2/getting-started/index.html)
```
$  vagrant init hashicorp/precise32
$  vagrant up
$  vagrant ssh
```
*`vagrant up` for the first time make take a while because it is downloading files from the internet

#### Goals:
- Work on the same OS (maybe something similar to the clic machines)
- Red Hat Linux 9 - couldn’t find this image
- Easily install and modify all dependencies with correct versions
- Java ✓
- Python ✓
- Lex ✓
- Yacc ✓
- PLY ✓

Provisioning file (.sh):
```
sudo apt-get update
sudo apt-get install openjdk-6-jre-headless
sudo apt-get install python
sudo apt-get install flex
sudo apt-get install bison
sudo apt-get install python-ply

sudo apt-get install vim
sudo apt-get install git
sudo apt-get install make
```

Free VirtualBox images:
- http://virtualboxes.org/images/
- https://vagrantcloud.com/

#### Brief Tutorial:
Make sure `Vagrantfile` and `bootstrap.sh` are in the current directory.

To start up the virtualbox (may take a while if it’s the first time):
```
$ vagrant up
```

To SSH into virtualbox:
```
$ vagrant ssh
```
To access local files in the directory that you `vagrant up`ed in
```
$ cd /vagrant
```
So we want to keep `Vagrantfile` in the same dir as `.git` repo so that when we `cd /vagrant` we can `git add` and commit stuff as if we were modding everything on our local.

To leave guest machine:
```
$ exit
```

To teardown, can suspend, halt, or destroy - more on teardown below:
```
$ vagrant suspend
```

Virtualboxes from Vagrant are stored in host machine in this directory (not sure about windows):
`~/.vagrant.d/boxes`

Versions for current Precise32 box:
- Python:	2.7.3
- Java:		1.6.0_30
- Yacc:		Bison 2.5
- Lex:		Flex 2.5.35
- PLY:		3.4-2build1

Teardown:
- Suspend : saves current running state of VM and stop it. Fast, but requires more disk space.
- Halt : shuts down guest OS and machine. Takes more time to boot up, requires disk space.
- Destroy : completely removes all traces of guest machine; deletes everything

```
cso@dyn-160-39-246-228 /Users/cso/Documents/coms4115/svelTest $ vagrant ssh
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)

Documentation:  https://help.ubuntu.com/
Welcome to your Vagrant-built virtual machine.
Last login: Fri Sep 14 06:22:31 2012 from 10.0.2.2
vagrant@precise32:~$ java -version
java version "1.6.0_30"
OpenJDK Runtime Environment (IcedTea6 1.13.1) (6b30-1.13.1-1ubuntu2~0.12.04.1)
OpenJDK Client VM (build 23.25-b01, mixed mode, sharing)
vagrant@precise32:~$ python -V
Python 2.7.3
vagrant@precise32:~$ lex -V
lex 2.5.35
vagrant@precise32:~$ yacc -V
bison (GNU Bison) 2.5
Written by Robert Corbett and Richard Stallman.

Copyright (C) 2011 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
vagrant@precise32:~$  
```

## Git Workflow

#### If you're creating the svelTest project for the first time or you want a fresh copy: 
1. Fork svelTest/svelTest on GitHub
2. Clone <yourname>/svelTest onto your local machine
```
$ git clone https://github.com/<yourname>/svelTest
```

#### Set up a remote: 
```
$ git remote add upstream https://github.com/svelTest/svelTest.git
```
Now check to make sure your remote is there:
```
$ git remote -v
```
Should see:
```
origin		https://github.com/<yourname>/svelTest.git (fetch)
origin		https://github.com/<yourname>/svelTest.git (push)
upstream	https://github.com/svelTest/svelTest.git (fetch)
upstream	https://github.com/svelTest/svelTest.git (push)
```
Every time:

- Work on your changes

- When you have a set of changes ready to push, FETCH/PULL FIRST from upstream to make sure you are updated with the base svelTest/svelTest repo
```
$ git fetch upstream
or
$ git pull upstream master
```

- Switch to your main branch (don't worry about this if you're not working on a separate branch)
```
$ git checkout master
```

- Merge with the upstream master branch (only if you fetched instead of pulled)
```
$ git merge upstream/master
```

- If merge conflicts, fix and continue (only if you fetched instead of pulled)

- Push your changes to your own repository (origin)
```
$ git push origin master // if working on master branch
```

- Go to Github and create a pull request against svelTest/master
Base fork: svelTest/svelTest
base: master
Head fork: <yourname>/svelTest
compare: master (//or whatever branch you want to push)
