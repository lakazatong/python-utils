# python_utils
Python utils I like to have.
## Add to your repo
In your repo root folder
* `git submodule add https://github.com/lakazatong/python_utils libs/python_utils`
## Import
### From files inside the libs folder
* `from python_utils.utils.all import *`
### Outside
* `import sys; sys.path.append('libs'); from python_utils.utils.all import *`
## Update your submodules
* `git submodule update --remote --merge`