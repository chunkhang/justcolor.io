# justcolor.io

> Just the color, and nothing else

[Just Color][justcolor] is a useless website to quickly display
a certain color. Who needs those fancy color tools like
[ColorHexa][colorhexa]? Sometimes, you just need the color, and nothing
else.

## Dependencies

- [Python 3.9][python]
- [Pipenv][pipenv]
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

Run `just up` to start the production server. [Gunicorn][gunicorn] will
be run by [Supervisor][supervisor], which itself runs as a daemon. The
application can be accessed via [localhost:5000][localhost-5000].

### Checking

Run `just status` to check the status of the production server.

### Restarting

Run `just restart` to restart the production server if there are new
changes to the application code.

### Stopping

Run `just down` to stop the production server.

## Deployment

### Instance

For now, it is assumed that the deployment is done on an [EC2][ec2]
instance running [Amazon Linux 2][amazon-linux-2]. Install all system
dependencies listed above.

### SSH

Configure the SSH alias `justcolor.io` in `~/.ssh/config`:

```
Host justcolor.io
  HostName <elastic ip address>
  IdentityFile <pem file>
  User ec2-user
```

Now, we can SSH into the remote instance with:

```
ssh justcolor.io
```

### Git

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
#!/bin/bash

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

### NGINX

Install and set up [NGINX][nginx] to proxy public requests to the
production server. Assuming [Let's Encrypt][lets-encrypt] was set up
using [Certbot][certbot], the `/etc/nginx/nginx.conf` file should look
something like this:

```
worker_processes 1;

events {
  worker_connections 1024;
}

http {
  include       mime.types;
  default_type  application/octet-stream;

  sendfile  on;
  gzip      on;

  keepalive_timeout  5;

  server {
    listen 80;

    server_name justcolor.io;

    location / {
      return 301 https://$server_name$request_uri;
    }
  }

  server {
    listen 443 ssl;

    server_name justcolor.io;

    ssl_certificate      /etc/letsencrypt/live/justcolor.io/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/justcolor.io/privkey.pem;

    location / {
      proxy_pass         http://127.0.0.1:8000/;
      proxy_redirect     off;

      proxy_set_header   Host                 $host;
      proxy_set_header   X-Real-IP            $remote_addr;
      proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto    $scheme;
    }
  }
}
```

### Deploying

For the first deployment, manually start the production server and NGINX:

```
ssh justcolor.io
cd repo/justcolor.io
just up
sudo nginx
```

For subsequent deployments, run `just deploy` to deploy new changes to
the live server.

[amazon-linux-2]: https://aws.amazon.com/amazon-linux-2/
[certbot]: https://certbot.eff.org/
[colorhexa]: https://www.colorhexa.com/
[ec2]: https://aws.amazon.com/ec2/
[flask]: https://flask.palletsprojects.com/
[gunicorn]: https://gunicorn.org/
[just]: https://github.com/casey/just
[justcolor]: https://justcolor.io
[lets-encrypt]: https://letsencrypt.org/
[localhost-5000]: http://localhost:5000
[nginx]: https://gunicorn.org/
[pipenv]: https://pipenv.pypa.io/en/latest/
[python]: https://www.python.org/
[supervisor]: http://supervisord.org/
