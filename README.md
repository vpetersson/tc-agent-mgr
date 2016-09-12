# TeamCity Agent Manager

We've been using TeamCity for some time. However, the lack of 'Cloud' integration with Google Cloud made it hard to dynamically scale the build agent count up and down through an instance group (since you would have to manually approve the build agents).

This little script will periodically check if there are any unapproved workers, and automatically approve them.

Here's what you need to get this working:

 * TeamCity 10 (Not sure if the API calls work on earlier versions)
 * A host to run this on (preferably in Docker)
 * Some kind of auto provisioning of build agents (we use [Startup Scripts](https://cloud.google.com/compute/docs/startupscript), but that's up to you)
 * An account on TeamCity that can approve new build agents

 ## Setup

 ```
$ docker run -d \
  -e TC_URL=https://your-ci.your-domain.com \
  -e TC_USER=jsmith \
  -e TC_PASS=SecretPassword \
  vpeterssson\tc-agent-mgr
```

If you have a paid license of TeamCity, you may also specify `TC_MAX_AGENT`, but this will default to 3 (which is the limit for the free license).
