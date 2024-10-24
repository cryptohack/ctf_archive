#!/bin/sh

echo "[+] Waiting for connections"
socaz --timeout 69 --flag-from-env FLAG --bind 1337 --cmd "sage rsatogether.sage"
echo "[+] Exiting"
