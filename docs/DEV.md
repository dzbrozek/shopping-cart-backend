Local development
============

We run `pre-commit` to preserve the quality of the code. To set up `pre-commit` run:

```
pip install virtualenvwrapper
mkvirtualenv shoppingcart -p python3.8
echo "cd $(pwd)" >> ~/.virtualenvs/shoppingcart/bin/postactivate
pip install -r requirements/dev.txt
pre-commit install
pre-commit install --hook-type commit-msg
```
