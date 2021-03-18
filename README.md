# Cloudflare Digital Ocean Sync (cfdosync)

A Python script that synchronizes a Digital Ocean firewall to match Cloudflare IP addresses

## Background

For added security, I only permit TCP443 connections to my Digital Ocean droplet from [Cloudflare IP addresses](https://www.cloudflare.com/ips/). Because all of my web traffic goes through CloudFlare,
no HTTPS connections go directly to the droplet.

This python script ensures that if Cloudflare adds or removes any IP addresses from their published ranges, they will automatically be able to connect to my droplet to pass traffic.

# Usage

You must first have a firewall created on Digital Ocean. This script does not create a new firewall, but rather modified an existing firewall. The firewall you create must be exclusively for Cloudflare,
as any other inbound rules will be wiped out.

Once you've created your firewall, you can get the ID associated with it from the URL when editing the firewall on Digital Ocean's website.

Lastly, you'll also need a Digital Ocean API key, which you can create by [following these steps](https://www.digitalocean.com/docs/apis-clis/api/create-personal-access-token/).

## Podman/Docker Container

A container image if provided if you don't want to mess with any Python install or requirements

```bash
podman run -e FIREWALL_ID=... -e API_KEY=... --rm ghcr.io/ecnepsnai/cfdosync:latest
```

*Note:* Replace `podman` with `docker` if that's what you're using.

## Python Script

**Requirements:**

- Python 3
- Requests (any recent version should do)

```bash
FIREWALL_ID=... API_KEY=... python3 sync.py
```