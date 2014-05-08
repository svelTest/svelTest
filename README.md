svelTest
========

# Navigation
| Project & Contributors | Git Workflow  |
| :------------: | :------------: | :-----:|
![](http://www.flaticon.com/png/256/1391.png)|![](http://www.flaticon.com/png/256/25997.png) |
| [Project & Contributors](#project--contributors) | [Git Workflow](#git-workflow) |
| Introducing SvelTest - why we built it and what it does | Our Git / GitHub workflow

## Project & Contributors

### Deliverables
1. Whitepaper ([GDOC] (https://docs.google.com/document/d/1Z7Xzvcv0Aax7_WevoXOm4fF4oYqJ9_yP1PLgtqTIJ4w/edit?usp=sharing))
2. Language Tutorial ([HTML] (https://svelTest.github.io/tutorial) | [GDOC](https://docs.google.com/document/d/1Zh-MP_gr9qH-466IiityswVk1Wd6GZtAT1-l0jpcYhU/edit?usp=sharing))
3. Language Reference Manual ([GDOC] (https://docs.google.com/document/d/1sn5K1YFt0yfNsU4QQjW1xewVx-IlDh8yKmCrAinI2wY/edit?usp=sharing))

### Contributors
Project Manager: Kaitlin Huben ([@kaitlinhuben](https://github.com/kaitlinhuben))

Language Guru: Emily Hsia ([@emilyhsia](https://github.com/emilyhsia))

System Architect: Joshua Lieberman ([@JALsnipe](https://github.com/JALsnipe))

System Integrator: Christopher So ([@chrso](https://github.com/chrso))

Verification and Validation Person: Amanda Swinton ([@mcswint](https://github.com/mcswint))


## Git Workflow

#### If you're creating the svelTest project for the first time or you want a fresh copy: 
- Fork svelTest/svelTest on GitHub
- Clone <yourname>/svelTest onto your local machine
```
$ git clone https://github.com/<yourname>/svelTest
```
- Set up a remote: 
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
#### Every time:

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
