# python_utils
Python utils I like to have.
## Add to your repo
As submodule
* `git submodule add https://github.com/lakazatong/python_utils`

As source
* `git clone https://github.com/lakazatong/python_utils`
## Update your submodules
* `git submodule update --remote --merge`
## Remove the submodule
* `path=python_utils && git submodule deinit -f path && rm -rf .git/modules/path && git rm -f path`

Taken from [here](https://gist.github.com/myusuf3/7f645819ded92bda6677?permalink_comment_id=3915500#gistcomment-3915500).
