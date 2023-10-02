# README

## Useful commands
### Start HomeAssitant in Docker
Running from the command line in the root of the project:
```bash
docker run --name home-assistant-test --rm -it -p 8123:8123/tcp -v ${PWD}/tests/resources/HA:/config ghcr.io/home-assistant/home-assistant:stable
```

To login to home assistant go to http://localhost:8123 and use the following credentials:
```bash
username: appdaemon
password: appdaemon
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhYjdiOGY4ZDEzOTc0MjlkYWEyYWU2YWY3OTQ3NDY1NCIsImlhdCI6MTY5NjQyNjEzOSwiZXhwIjoyMDExNzg2MTM5fQ.a48RAuLg676Mmxwgx4j7-U4vHORR3EmKL5M5TkNf7Vk
```

or

```
username: main
password: main
```
