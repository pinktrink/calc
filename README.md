You'll want to set up a virtualenv so

```
brew install python3
virtualenv -p python3 venv
venv/bin/activate
pip install -r requirements.txt
python calc.py '1 + 3 + 9 / 4 * 7 - 1'
```

If you don't have virtualenv, just run

```
sudo easy_install pip
sudo pip install virtualenv
```
