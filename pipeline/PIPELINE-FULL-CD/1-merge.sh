#/bin/sh
git checkout master
git tag -a `date +%d%b%Y%H%M%S` -m "CD"
git merge origin/develop
git commit -am "Merged develop branch to master"
git remote add origin ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/todo-list-serverless-aws
git push --set-upstream origin master