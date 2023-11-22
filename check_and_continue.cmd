tasklist | find "qbittorrent.exe" > nul
if errorlevel 1 (

    cd "C:\Program Files\NordVPN\"
    nordvpn --connect

    cd "C:\Program Files\qBittorrent"
    qbittorrent.exe

    echo [%date% %time%] "reconnected NordVPN, and restarted qBittorrent " >> cac_log.txt

) else (
    echo "still running"
)
