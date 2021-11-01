## How to run:

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
If there is any error in pip3 install, try updating pip3 first.
Then copy settings.py to local_settings.json and fill in admin_token and discord_token.

```bash
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

=======
Coming feature
1. Loot count down
2. Integrate Bid function
3. Alt management