# cloudflare-stun

CloudFlare Dynamic DNS using STUN

There are a few command line dynamic DNS clients that support CloudFlares' API, but most of these use services like [jsonip](jsonip.com) to look up the external IP of a system. These services are great, but it would be better to use a standard protocol to do this. Fortunately, the STUN protocol exists for exactly this purpose.

## Usage

```
CF_AUTH_EMAIL="foo@bar.com" CF_AUTH_KEY="abcde1234" cloudflare_stun --zone example.com --record-name extrn
```
