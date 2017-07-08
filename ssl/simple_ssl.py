import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False
context.load_verify_locations("/Users/wingman/openSource/D/vibe.d/tests/tls/server.crt")