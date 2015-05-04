<h2>Text Processing Collection Library</h2>

This is a collection of methods writte in Python that performs basic text processing methods. 

<h4>Module into another Git Repo</h4>

If you want to import this repo as a submodule into another Git Repo, check the following steps (retrived from [here](http://stackoverflow.com/questions/2140985/how-to-set-up-a-git-project-to-use-an-external-repo-submodule))

* You have a project -- call it MyWebApp that already has a github repo
* You want to use the TextProcessingLib repository in your project
* You want to pull the TextProcessingLib repo into your project as a submodule.

Submodules are really, really easy to reference and use. Assuming you already have MyWebApp set up as a repo, from terminal issue these commands:

```
cd MyWebApp
git submodule add https://github.com/xarabas/TextProcessingLib.git externals/TextProcessingLib
```

This will create a directory named externals/TextProcessingLib* and link it to the github jquery repository. Now we just need to init the submodule and clone the code to it:

```
git submodule update --init --recursive
```

You should now have all the latest code cloned into the submodule. If the jquery repo changes and you want to pull the latest code down, just issue the submodule update command again. Please note: 
I typically have a number of external repositories in my projects, so I always group the repos under an externals directory.

The online Pro Git Book has some good information on submodules (and git in general) presented in an easy-to-read fashion. Alternately, git help submodule will also give good information. Or take a look at the Git Submodule Tutorial on the git wiki.

I noticed this blog entry which talks about submodules and compares them to Subversion's svn:externals mechanism: http://speirs.org/blog/2009/5/11/understanding-git-submodules.html
