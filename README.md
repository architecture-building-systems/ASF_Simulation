# ASF_Simulation
Numerical Simulation of the ASF to determine its energy saving potential and optimal configurations


##Git the simple guide - no deep shit
http://rogerdudler.github.io/git-guide/

##Git Setup

In Your working directory type
`git init`

Then Checkout the repository
`git clone https://github.com/architecture-building-systems/LCA_Paper.git `

To download the files type

`git pull`

##Git Use

Always do a `git pull` before starting work, just so you have the latest update


I like to first type `git status`so you know exactly what files are different

To add your changes:
`git add <filename>`
or
`git add *` to add all files in your working directory

I like to also do a `git status` here again to make sure that everything you want has been added

Then commit the changes
`git commit -m "commit message"`

At this point it is good to run a `git pull` in case someone was working on the same file at the same time

If there are no conflicts then do a 
`git push origin master`

##If you get a confilct
Github will tell you which files were conflicting. Open these files in your text editor and there will be the following markers
```
<<<<<<< HEAD:file.txt
What your version is
=======
What the confliciting version is
>>>>>>> 77976da35a11db4580b80ae27e8d65caf5208086:file.txt
```
Pick which ever version you like. Delete everything else `<<<<<<< HEAD:file.txt`, `=======`, `>>>>>>> 77976da35a11db4580b80ae27e8d65caf5208086:file.txt`
If everything fails, then save your work somewhere, delete your work, and download a fresh copy...

The do another `git commit -m "commit message"` and `git push origin master`
Follow this up with a `git pull` just to make sure its all ok. And then finish it up with a `git status` to make sure that everything is clean
