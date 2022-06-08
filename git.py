#!/usr/bin/python
import git
from git import Repo
# git clone new_repo
#create a folder Assignment7
git.Repo.clone_from('https://github.com/kapana031/Assignment7', 'Assignment7')
#commit new file
repo=git.Repo('Assignment7')
