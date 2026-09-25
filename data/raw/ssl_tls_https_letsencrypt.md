# SSL/TLS, HTTPS, and Let's Encrypt

## SSL vs TLS
SSL (Secure Sockets Layer) is the older protocol, deprecated due to security flaws.
TLS (Transport Layer Security) is its modern successor. In casual use, "SSL
certificate" almost always actually means a TLS certificate — the terms are used
interchangeably in practice.

## How HTTPS works (simplified)
1. Client connects to the server and requests a secure connection.
2. Server presents its TLS certificate (containing its public key, signed by a
   Certificate Authority).
3. Client verifies the certificate is valid and trusted (checks the CA chain,
   expiration, hostname match).
4. Client and server perform a handshake to agree on a shared symmetric session key.
5. All further communication is encrypted with that symmetric key (faster than
   asymmetric encryption for bulk data).

## Certificate components
- **Public/private key pair**: the private key stays on the server; the public key is
  embedded in the certificate.
- **Certificate Authority (CA)**: a trusted third party that signs certificates,
  vouching for their authenticity (e.g. Let's Encrypt, DigiCert).
- **Chain of trust**: root CA → intermediate CA → your certificate — browsers trust a
  small set of root CAs and verify the whole chain.

## Let's Encrypt
A free, automated Certificate Authority. Uses the ACME protocol to prove domain
ownership (usually via an HTTP challenge or DNS challenge) and issues short-lived
(90-day) certificates, meant to be renewed automatically.

### Using Certbot (the standard Let's Encrypt client)
```bash
sudo apt install certbot python3-certbot-nginx

sudo certbot --nginx -d example.com -d www.example.com
# Certbot automatically edits the Nginx config to add the certificate and redirect
# HTTP -> HTTPS.

sudo certbot renew --dry-run     # test that auto-renewal works
```
Certbot installs a systemd timer/cron job to renew automatically before the 90-day
certificate expires.

## Common errors & fixes
- **"NET::ERR_CERT_AUTHORITY_INVALID"**: the certificate isn't from a trusted CA
  (common with self-signed certs) — fine for local dev, not for production.
- **"NET::ERR_CERT_COMMON_NAME_INVALID"**: the certificate's domain doesn't match the
  URL you're visiting — check the cert covers all needed domains/subdomains (or use a
  wildcard cert).
- **Certbot challenge fails ("Connection refused")**: port 80 must be reachable from
  the internet for the HTTP-01 challenge — check firewall/security group rules and
  that Nginx is actually running.
- **Certificate expired**: the auto-renewal cron/timer silently failed — check
  `sudo certbot renew --dry-run` output and `systemctl status certbot.timer`.
- **Mixed content warnings**: an HTTPS page loading some resources over plain HTTP —
  update those resource URLs to HTTPS too.
