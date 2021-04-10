# justcolor.io

> Just the color, and nothing else

[Just Color][justcolor] is a useless website to quickly display
a certain color. Who needs those fancy color tools like
[ColorHexa][colorhexa]? Sometimes, you just need the color, and nothing
else.

## Dependencies

- [Python][python]
- [Pipenv][pipenv]
- [NGINX][nginx]
- [Supervisor][supervisor]
- [Just][just]

## Installation

Run `just bootstrap` to:

- Verify that all system dependencies are present
- Install project dependencies
- Create relevant project folders

## Development

### Running

Run `just start` to start the development server. Hot reload is
handled by [Flask][flask]. The application can be accessed via
[localhost:5000][localhost:5000].

### Stopping

Stop the development server any time with the usual `Ctrl-C`.

## Production

### Running

Run `just up` to start the production server. [Gunicorn][gunicorn] and
[NGINX][nginx] are both handled by [Supervisor][supervisor], which runs
as a daemon. The application can be accessed via [localhost][localhost].

### Checking

Run `just status` to check the status of the production server.

### Restarting

Run `just restart` to restart the production server if there are new
changes to the application code.

### Stopping

Run `just down` to stop the production server.

[localhost]: http://localhost
[localhost:5000]: http://localhost:5000
[colorhexa]: https://www.colorhexa.com/
[flask]: https://flask.palletsprojects.com/
[gunicorn]: https://gunicorn.org/
[just]: https://github.com/casey/just
[justcolor]: https://justcolor.io
[nginx]: https://gunicorn.org/
[pipenv]: https://pipenv.pypa.io/en/latest/
[python]: https://www.python.org/
[supervisor]: http://supervisord.org/
