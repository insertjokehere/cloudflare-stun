#!/bin/bash -x
if [ -f /run/secrets/cf-auth-key ]; then
    export CF_AUTH_KEY=$(cat /run/secrets/cf-auth-key)
fi

cloudflare_stun "$@"
