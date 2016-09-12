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
  --name tc-agent-mgr \
  -e TC_URL=https://your-ci.your-domain.com \
  -e TC_USER=jsmith \
  -e TC_PASS=SecretPassword \
  vpetersson/tc-agent-mgr
```

### Optional Settings

* `TC_MAX_AGENT`:  This will default to 3 (which is the limit for the free license).
* `AGENT_WHITELIST_STRING`: Set this if you want to only approve agents with this string in the name.

## Security Notes

Please note that there is not a whole lot of security considerations in here. Any agent trying to register to your TeamCity server will automatically get approved (unless `AGENT_WHITELIST_STRING` is set). Don't use this unless you understand that risk.

You may also want to create a new TeamCity group and only grant permission to the role 'Agent manager'. You can then make your new a member of this group and this group only.
