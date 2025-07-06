# Redis

Playing with Redis (Remote Dictionary Server).

## TOC

...

[redis]: https://github.com/redis/redis-py

### Pre-work

My OS: Ubuntu

I didn't mind about "redis-cli"(ent) installed: `sudo apt update && sudo apt install redis-tools`.

Docker image (no need to install Redis system-wide): `docker pull redis:8.0.2-alpine`. A particular version of Redis is good for reproducibility, Alpine is minimal enough.

I decided to retag the pulled image: `docker tag redis:8.0.2-alpine redis` (the tag will be defaulted to "latest" - I don't care).

Launching: `docker run --name="redserv" --rm -d -p 6379:6379 redis`. The default port for Redis is, obviously, 6379.

Checking: `redis-cli`. It will default to the host `-h 127.00.1` ("localhost") and the port `-p 6379`.

As s Python developer (now it is), I would like to play with the [redis][redis] library (no need for me to use [aioredis](https://github.com/aio-libs-abandoned/aioredis-py) because [redis][redis] embraced supports asynchrounisity). The Python 3.13 version is presumed for these notes.

In the [python](./python/) directory:

1. `uv venv --python 3.13`
2. `source .venv/bin/activate`
3. `uv pip install "redis[hiredis]"` - with [hiredis](https://github.com/redis/hiredis) support
4. `uv pip list` - if you like to check it installed.
