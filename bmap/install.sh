#!/bin/bash
echo "[*] Installing BMAP v2 cross-platform..."
SCRIPT_PATH="$(pwd)/bmap.py"

if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    PREFIX_BIN="/data/data/com.termux/files/usr/bin/bmap"
    pip install requests 2>/dev/null
else
    PREFIX_BIN="/usr/local/bin/bmap"
    pip install requests --break-system-packages 2>/dev/null || pip install requests 2>/dev/null
fi

printf '#!/bin/bash\npython3 %s "$@"\n' "$SCRIPT_PATH" > "$PREFIX_BIN"
chmod +x "$PREFIX_BIN"

echo "[+] Installation finished successfully!"
echo "[+] You can now type 'bmap' from anywhere on your device to run the tool!"
