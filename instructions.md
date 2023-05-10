# Welcome to the DevOps challenge

### Instructions

We've found a data leak in our company, but before we're deleting our resources, we need you to extract the information and deliver it.
You're assigned with the creation of a device that will be used as a POC to transfer highly sensitive data.
With the language of your choice follow the instructions below to stop the leak.
**Your `codeName = thedoctor`** - note that this is code **not** guaranteed to work, and you may need to show some debugging skills to fix it.

1. Your task is to write a **containerized** application that will extract the secret string from a DynamoDB table and present it in a web server
1. The `secretCode` lies in a DynamoDB table `devops-challenge` where `codeName = <YOUR_CODENAME>`
1. Instead of using keys to reach out to production, we've cloned our DB to a [local dynamodb](https://hub.docker.com/r/amazon/dynamodb-local). You can get it by pulling [`zestyco/dynamodb-challenge:amd`](https://hub.docker.com/repository/docker/zestyco/dynamodb-challenge) container. Note: `latest` tag pulls an arm based container, use `amd` tag if needed instead.
1. Create a web router that runs in a docker container, which will respond with a json structure as seen below to `/health` and `/secret`
1. Push your container to a docker registry of your choice and use the address both in your compose file and in the `health` endpoint (see example)
1. Create a docker-compose file that sets the environment of the app and the db
1. Lastly, add a README.md with instructions and any other documentation you see fit.
1. Once completed, reply to the challenge email:
```
Subject: DevOps Challenge complete
Content: Name:      <YOUR_NAME>
Attached: a compressed tarball of your project
```

---

The response from `/health` should look like:
```json
{
  "status": "Healthy!",
  "container": "https://docker.registry.com/somepath"
}
```

The response from `/secret` should look like:
```json
{
  "codeName": "<YOUR_CODENAME>",
  "secretCode": "<SECRET_CODE>"
}
```

---

### Guidance:

1. Use `git init` before starting to work and commit your changes as you would normally
2. Think *security*: Avoid exposing secrets or sensitive information in any way
3. Examples of different routers in [Ruby](https://github.com/sinatra/sinatra), [Python](http://flask.pocoo.org/), [Go](https://golang.org/pkg/net/http/) and [Node](https://www.npmjs.com/package/http-server) (you're more than welcome to use any language / project of choice)
4. Structure the project in a maintainable logic way, you may use `/example`
---

```
devops@zesty.co
```
