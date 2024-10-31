# Porkbun DNS Updater
This simple Python program checks & updates your Porkbun URL IP addresses every hour.

> **WARNING: THIS PROGRAM DELETES THE LABEL ATTRIBUTED TO THE DNS ENTRIES. I HAVE TOLD PORKBUN ABOUT THIS.**

I created this because Vodafone decided to update my IP address nearly every day _(sometimes multiple times)_ and I was frustrated with having to change all my domains.

## Running
To run this program *(e.g, on a server)*, you can clone the repo, add the [environmental variables](#environmental-variables) to a `.env` file, and create a `domains.json` file in the root of the project:
```json
{
    "<domain>": [
        {
            "type": "<type_of_record>",
            "subdomain": "<subdomain>"
        },
        {
            "type": "<type_of_record>",
            "subdomain": "<subdomain>"
        }
    ]
}
```

Finally, you can run the following commands:
```bash
pip install -r requirements.txt
python app.py
```

A docker build is [coming soon](https://github.com/jamie6king/porkbun_dns_updater/issues/1).

### Environmental Variables
- `PORKBUN_API_KEY` - a Porkbun API key. ***(REQUIRED)***
- `PORKBUN_SECRET_KEY` - a Porkbun secret key. ***(REQUIRED)***

- `IP_ADDRESS` - the IP address to update the domain entries to. *(optional)*
    - Defaults to the current IP address, determined by the result of `curl https://ip.me`.
- `DEBUG_OUTPUT` - whether to show `[DEBUG]` output or not. *(optional)*
    - Defaults to `0` *(no debug output)*, set to `1` if debug output is needed.