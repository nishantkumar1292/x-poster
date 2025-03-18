#!/bin/bash

# Get current directory as absolute path
CURRENT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Remove existing app if it exists
rm -rf "/Applications/X Poster.app"

# Create a temporary directory for our applescript
mkdir -p "tmp_applescript"

# Create the AppleScript file
cat > "tmp_applescript/x_poster.applescript" << EOL
-- X Poster AppleScript
-- This launches the Python app for posting to X.com

on run
    set appPath to "$CURRENT_DIR/mac_app.py"
    set appFolder to "$CURRENT_DIR"

    try
        do shell script "cd " & quoted form of appFolder & " && source " & quoted form of appFolder & "/venv/bin/activate && python " & quoted form of appPath
    on error errorMsg
        display dialog "Error launching X Poster: " & errorMsg buttons {"OK"} default button "OK" with icon stop
    end try
end run
EOL

# Compile the AppleScript into an app
osacompile -o "/Applications/X Poster.app" "tmp_applescript/x_poster.applescript"

# Use a system icon for the app
cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AirDrop.icns "/Applications/X Poster.app/Contents/Resources/applet.icns"

# Clean up
rm -rf "tmp_applescript"

# Make the app more visible to Spotlight
touch "/Applications/X Poster.app"
mdimport "/Applications/X Poster.app"

# Create a Desktop shortcut
ln -sf "/Applications/X Poster.app" ~/Desktop/

echo "X Poster app has been created and installed in the Applications folder."
echo "A shortcut has been created on your Desktop."
echo "You can now launch it from Spotlight by typing 'X Poster' or from your Desktop."
