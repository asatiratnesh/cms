# CMS Django

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:asatiratnesh/cms.git
$ cd cms
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
