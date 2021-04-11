# justcolor.io

> Just the color, and nothing else

[Just Color][justcolor] is a useless website to quickly display
a certain color. Who needs those fancy color tools like
[ColorHexa][colorhexa]? Sometimes, you just need the color, and nothing
else.

## Dependencies

- [Python 3.9][python]
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
[localhost:5000][localhost-5000].

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

## Deployment

### Preparing

For now, it is assumed that the deployment is done on an [EC2][ec2]
instance running [Amazon Linux 2][amazon-linux-2]. Install all system
dependecies listed above.

Assume the SSH alias `justcolor.io` was configured correctly in
`~/.ssh/config`.

```
Host justcolor.io
  HostName <elastic ip address>
  IdentityFile <pem file>
  User ec2-user
```

Remotely, set up two directories for Git: bare and working.

```
ssh justcolor.io
mkdir -p repo/justcolor.io.git repo/justcolor.io
cd repo/justcolor.io.git
git init --bare
```

For the bare repository `justcolor.io.git`, the `hooks/post-update`
executable file should look something like this:

```
#!/bin/bash -l

git --work-tree ~/repo/justcolor.io --git-dir ~/repo/justcolor.io.git checkout --force
cd ~/repo/justcolor.io
just bootstrap
just restart
```

Locally, the Git remote `live` should point to the EC2 instance via SSH.

```
git remote add live ssh://justcolor.io/home/ec2-user/repo/justcolor.io.git
```

Basically, when we push to `live` remote, the `post-update` hook will
update the working directory `justcolor.io` with the latest code from
`master` branch. After that, the project is bootstrapped before the
production server is restarted.

### Deploying

For the first deployment, manually start the production server.

```
ssh justcolor.io
cd repo/justcolor.io
just up
```

For subsequent deployments, assuming the EC2 instance never went down,
run `just deploy` to deploy new changes to the live server.

[amazon-linux-2]: https://aws.amazon.com/amazon-linux-2/
[colorhexa]: https://www.colorhexa.com/
[ec2]: https://aws.amazon.com/ec2/
[flask]: https://flask.palletsprojects.com/
[gunicorn]: https://gunicorn.org/
[just]: https://github.com/casey/just
[justcolor]: https://justcolor.io
[localhost-5000]: http://localhost:5000
[localhost]: http://localhost
[nginx]: https://gunicorn.org/
[pipenv]: https://pipenv.pypa.io/en/latest/
[python]: https://www.python.org/
[supervisor]: http://supervisord.org/
