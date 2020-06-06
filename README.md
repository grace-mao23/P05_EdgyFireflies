# Read and Chill by Edgy Fireflies

Read and Chill: Read Your Way to Real Romance

![](https://github.com/grace-mao23/P05_EdgyFireflies/workflows/CI/badge.svg)

## Roster

* Grace Mao: Frontend, Project Manager
* Tammy Chen: Frontend, User Interaction
* Joseph Lee: Backend, API Connection
* Jun Tao Lei: Backend, Database Management

## Description

The objective of this project is to create a Tinder-like web application for book lovers to communicate. The application will allow users to meet new people with similar genre/book interests and bring people together (at a reasonably safe distance). Users can swipe left/right on other users just like the Tinder app & message people in real-time, with the use of Web Sockets. Users can also browse through a variety of book selections with the help of the Google Books API. 

## API

* [Google Books API](https://github.com/grace-mao23/P05_EdgyFireflies/blob/master/411_google-books.pdf)

## Launch Instructions

If you are using *nix shells, use make to run this application.

Available Make Commands:

* run
* test
* setup
* venv
* clean

If you are not able to use make, use the following:

1. Clone the Git repository.

```bash
git clone https://github.com/grace-mao23/P05_EdgyFireflies.git
```

2. Setup the application environment.

```bash
python3 -m venv env
env/bin/pip install -r requirements.txt
```

3. Run the application.

```bash
env/bin/python application.py
```

## Unit Tesing

Either use the supported make command or the following:

0. Make sure your are in the root of the project directory (i.e. path/to/P05_EdgyFireflies).

1. Run the unit tests with pytest. Be sure to have already setup the application environment as described above.

```bash
env/bin/python -m pytest
```
