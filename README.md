# AdAway for Desktop

[![Maintenance](https://img.shields.io/maintenance/yes/2016.svg)]()

This program blocks ad servers globally by blacklisting them in `/etc/hosts`.

Beware that if you have a HTTP server running on ports 80 or 443 (if you don't
know what a HTTP server is, you probably don't) then you may get additional log
entries related to apps or websites trying to display ads. If so, the possible
solutions are to change the listening port of the web server or provide the
`-t` option to redirect them to another server.

## Usage

(Download the script first).

### Windows

1. Download and install [Python](https://www.python.org/) 2.7.
2. Open a Command Prompt with administrator privileges and run
   `C:\path\to\python adaway.py`

### Linux

1. Run `python adaway.py` (`python` must be in version `2.x`, if it isn't, try
   `python2.7` or `python2`).

## Credits

- [AdAway](http://adaway.org) (the original Android app)
