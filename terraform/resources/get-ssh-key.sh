#! /bin/bash
echo "-----BEGIN RSA PRIVATE KEY-----" > resources/key.pem
cat key_pem | tr " " "\n" | awk '{print $1}' | tail -n +5 | head -n -4 >> resources/key.pem
echo "-----END RSA PRIVATE KEY-----" >> resources/key.pem
chmod 700 resources/key.pem
rm key_pem