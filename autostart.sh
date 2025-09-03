mkdir -p ~/.config/autostart && cat <<EOF > ~/.config/autostart/chromium-chatgpt.desktop
[Desktop Entry]
Type=Application
Name=Chromium
Exec=/usr/bin/chromium-browser --new-window --disable-infobars --autoplay-policy=no-user-gesture-required https://chatgpt.com
X-GNOME-Autostart-enabled=true
EOF
