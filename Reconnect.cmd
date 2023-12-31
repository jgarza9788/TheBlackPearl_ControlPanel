cd "C:\Program Files\NordVPN\"
::nordvpn --disconnect
::timeout 3
nordvpn --connect

timeout 3
cd "C:\Program Files\qBittorrent"
qbittorrent.exe


if errorlevel 1 (

    echo [%date% %time%] "Failed to execute Reconnect.cmd." >> rc.txt

) else (
    echo [%date% %time%] "reconnected NordVPN, and restarted qBittorrent " >> rc.txt
)

