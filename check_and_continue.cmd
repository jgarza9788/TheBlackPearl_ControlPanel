tasklist | find "qbittorrent.exe" > nul
if errorlevel 1 (

    cd "C:\Program Files\NordVPN\"
    nordvpn --connect

    cd "C:\Program Files\qBittorrent"
    qbittorrent.exe

) else (
    echo "still running"
)
