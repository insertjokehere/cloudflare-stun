import stun
import requests
import argparse
import os
import logging
import json
import time

logger = logging.getLogger(__name__)


class App():

    CF_API_ENDPOINT = "https://api.cloudflare.com/client/v4"
    CF_API_ZONE_LIST = CF_API_ENDPOINT + "/zones"
    CF_API_RECORD_LIST = CF_API_ENDPOINT + "/zones/{}/dns_records"
    CF_API_RECORD_UPDATE = CF_API_RECORD_LIST + "/{}"

    def __init__(self, zone, record, cf_auth_key, cf_auth_email, stun_server, stun_port, ttl, force_update):
        self.zone = zone
        self.record = record
        self.cf_auth_key = cf_auth_key
        self.cf_auth_email = cf_auth_email
        self.stun_server = stun_server
        self.stun_port = stun_port
        self.ttl = ttl
        self.force_update = force_update
        self.record_type = "A"

    def _api_headers(self):
        headers = {
            'X-Auth-Email': self.cf_auth_email,
            'X-Auth-Key': self.cf_auth_key,
            'Content-Type': 'application/json'
        }
        return headers

    def get_external_ip(self):
        nat_type, external_ip, external_port = stun.get_ip_info(stun_host=self.stun_server, stun_port=self.stun_port)
        return external_ip

    def get_zone_id(self, zone_name):
        resp = requests.get(
            App.CF_API_ZONE_LIST,
            headers=self._api_headers(),
            params={
                'name': zone_name
            })

        logger.debug(resp.text)
        resp.raise_for_status()

        r_data = resp.json()
        assert r_data['success']

        for zone in r_data['result']:
            if zone['name'] == zone_name:
                return zone['id']

        raise ValueError("No such zone {} from API".format(zone_name))

    def get_record_id(self, zone_name, record_name):
        zone_id = self.get_zone_id(zone_name)

        if record_name != "":
            target_zn = "{}.{}".format(record_name, zone_name)
        else:
            target_zn = zone_name

        resp = requests.get(
            App.CF_API_RECORD_LIST.format(zone_id),
            headers=self._api_headers(),
            params={
                'type': self.record_type,
                'name': target_zn
            })

        logger.debug(resp.text)
        resp.raise_for_status()

        r_data = resp.json()
        assert r_data['success']

        for record in r_data['result']:
            if record['name'] == target_zn:
                return zone_id, record['id'], record['content']

        raise ValueError("No such record {} in zone {} from API".format(zone_name, record_name))

    def update_record(self, zone_id, record_id, content):
        resp = requests.patch(
            App.CF_API_RECORD_UPDATE.format(zone_id, record_id),
            headers=self._api_headers(),
            data=json.dumps({'content': content})
        )

        logger.debug(resp.text)
        resp.raise_for_status()

    def create_record(self, zone_id, record_name, record_type, content, ttl):
        resp = requests.post(
            App.CF_API_RECORD_LIST.format(zone_id),
            headers=self._api_headers(),
            data=json.dumps({
                'type': record_type,
                'name': record_name,
                'content': content,
                'ttl': ttl
            })
        )
        logger.debug(resp.text)
        resp.raise_for_status()

    def do_update(self):
        extrn_ip = self.get_external_ip()
        if extrn_ip is None:
            logger.error("Cannot determine external IP!")
            exit(1)
        else:
            logger.info("External IP: {}".format(extrn_ip))
        try:
            zone_id, record_id, record_content = self.get_record_id(self.zone, self.record)
        except ValueError:
            zone_id = self.get_zone_id(self.zone)
            self.create_record(zone_id, self.record, self.record_type, extrn_ip, self.ttl)
        else:
            if record_content != extrn_ip or self.force_update:
                self.update_record(zone_id, record_id, extrn_ip)
            else:
                logger.debug("Record is already up to date, pass --force-update to update anyway")

    @staticmethod
    def _get_from_environment(args, param):
        cmd_val = getattr(args, param.replace('-', '_'))
        if cmd_val is None:
            try:
                value = os.environ[param.replace('-', '_').upper()]
            except KeyError:
                logger.error("Must set {} environment variable if --{} is not passed on the command line".format(
                    param.replace('-', '_').upper(),
                    param
                ))
                exit(1)
        else:
            value = cmd_val

        return value

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('--zone', required=True, help="The name of the zone to update")
        parser.add_argument('--record-name', required=False, default="", help="The name of the record to update, eg if --zone is example.com and --record-name is extrn, extrn.example.com will be updated. If omitted, the root of the zone will be updated")
        parser.add_argument('--cf-auth-key', required=False, help="Cloudflare auth key. This is required if the CF_AUTH_KEY environment variable isn't set")
        parser.add_argument('--cf-auth-email', required=False, help="Cloudflare auth email. This is required if the CF_AUTH_EMAIL environment variable isn't set")
        parser.add_argument('--stun-server', default=None, help="STUN server to query")
        parser.add_argument('--stun-port', default=3478, type=int, help="Port of the STUN server")
        parser.add_argument('--ttl', default=120, help="TTL of the new DNS record. This is only used if the record doesn't already exist")
        parser.add_argument('--force-update', action='store_true', help="By default, the tool won't attempt to update the record if it is already correct. Use this to override this behavior")

        log_group = parser.add_mutually_exclusive_group()
        log_group.add_argument('--debug', action='store_true', help="Output lots of information to help with debugging")
        log_group.add_argument('--quiet', action='store_true', help="Don't output anything")

        daemonize_group = parser.add_mutually_exclusive_group()
        daemonize_group.add_argument('--once', action='store_true', default=True, help="Check for changes once, then exit")
        daemonize_group.add_argument('--every', type=int, required=False, help="Run every <n> seconds")

        args = parser.parse_args()

        cf_auth_key = App._get_from_environment(args, 'cf-auth-key')
        cf_auth_email = App._get_from_environment(args, 'cf-auth-email')

        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif not args.quiet:
            logging.basicConfig(level=logging.INFO)

        app = App(args.zone, args.record_name, cf_auth_key, cf_auth_email, args.stun_server, args.stun_port, args.ttl, args.force_update)

        while not args.once:
            app.do_update()
            if not args.once and args.every is not None:
                logger.debug("Sleeping for {} seconds".format(args.every))
                time.sleep(args.every)
