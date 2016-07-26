===============
cloudflare-stun
===============

CloudFlare Dynamic DNS using STUN

There are a few command line dynamic DNS clients that support CloudFlares' API, but most of these use services like `jsonip <http://jsonip.com>`_ to look up the external IP of a system. These services are great, but it would be better to use a standard protocol to do this. Fortunately, the STUN protocol exists for exactly this purpose.

Quick Start
-----------

::

   CF_AUTH_EMAIL="foo@bar.com" CF_AUTH_KEY="abcde1234" cloudflare_stun --zone example.com --record-name extrn

Will create or update an A record for ``extrn.example.com`` with the public IP address of the machine running the tool.

Usage
-----

::

   cloudflare_stun [-h] --zone ZONE --record-name RECORD_NAME
                       [--cf-auth-key CF_AUTH_KEY]
                       [--cf-auth-email CF_AUTH_EMAIL]
                       [--stun-server STUN_SERVER] [--stun-port STUN_PORT]
                       [--ttl TTL] [--force-update] [--debug | --quiet]

   Arguments:
     -h, --help                      show this help message and exit
   
     --zone ZONE                     The name of the zone to update
  
     --record-name RECORD_NAME       The name of the record to update, eg if --zone is
                                     example.com and --record-name is extrn,
                                     extrn.example.com will be updated
     
     --cf-auth-key CF_AUTH_KEY       Cloudflare auth key. This is required if the
                                     CF_AUTH_KEY environment variable isn't set

     --cf-auth-email CF_AUTH_EMAIL   Cloudflare auth email. This is required if the
                                     CF_AUTH_EMAIL environment variable isn't set

     --stun-server STUN_SERVER       STUN server to query

     --stun-port STUN_PORT           Port of the STUN server

     --ttl TTL                       TTL of the new DNS record. This is only used if the
                                     record doesn't already exist

     --force-update                  By default, the tool won't attempt to update the
                                     record if it is already correct. Use this to override
                                     this behavior

     --debug                         Output lots of information to help with debugging

     --quiet                         Don't output anything


Known Issues
------------

* This tool only support Python 2.7, because the underlying STUN library doesn't support Python 3.x - See `the upstream repo <https://github.com/jtriley/pystun>`_ for details.
