cat > ~/autostart.sh << 'EOF'
#!/bin/bash
source ~/venv/bin/activate
python3 /home/pi/led.py
EOF
