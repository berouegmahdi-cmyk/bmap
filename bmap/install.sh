#!/bin/bash
echo "[*] Installing BMAP v2..."
mkdir -p /opt/bmap
cp bmap.py /opt/bmap/bmap.py
chmod +x /opt/bmap/bmap.py

if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    PREFIX_BIN="/data/data/com.termux/files/usr/bin/bmap"
    pip install requests 2>/dev/null
else
    PREFIX_BIN="/usr/local/bin/bmap"
    pip install requests --break-system-packages 2>/dev/null || pip install requests 2>/dev/null
fi

ln -sf /opt/bmap/bmap.py "$PREFIX_BIN"
chmod +x "$PREFIX_BIN"

echo "[+] Installation finished successfully!"
echo "[+] Type 'bmap' from anywhere to run your tool!"
