#!/bin/bash
# Start the matchbox window manager
# Print Application starting
echo "########"
echo "########"
echo "Starting Application"
echo "########"
echo "########"

#export DISPLAY=:0 

current_project

# cd /home/IntExp/Documents/vlcWork

# Xvfb :99 -screen 0 1024x768x16 &

# # # Wait for Xvfb to start
# sleep 2

# # Export the DISPLAY environment variable
# export DISPLAY=:99

# matchbox-window-manager &

# Run the Python script
#sudo -E /home/IntExp/Documents/vlcWork/.venv/bin/python /home/IntExp/Documents/vlcWork/MainLoop.py

python MainLoop.py

exit 0