## How to run:

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ copy settings.py to local_settings.json and fill in admin_token and discord_token
$ python3 main.py
```

To install new library:
Make sure these commands need to be done while in venv:
```bash
$ pip3 install libraryName
$ pip3 freeze > requirements.txt
```

To deactivate the virtual env:
```bash
$ deactivate
```