#!/bin/bash
echo "[*] Installing BMAP v3 for Termux/Linux..."
pkg update -y && pkg install -y python python-pip nmap git 2>/dev/null
pip install requests 2>/dev/null
mkdir -p ~/.bmap
cp bmap.py ~/.bmap/bmap.py
chmod +x ~/.bmap/bmap.py
rm -f $PREFIX/bin/bmap
cat << 'WRAPPED' > $PREFIX/bin/bmap
#!/bin/bash
python3 ~/.bmap/bmap.py "$@"
WRAPPED
chmod +x $PREFIX/bin/bmap
echo "[+] BMAP v3 Installed Successfully! Type 'bmap' to run."
