#!/bin/bash

# Get current directory as absolute path
CURRENT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Clean up any existing app bundle
rm -rf "X Poster.app"
rm -rf "/Applications/X Poster.app"

# Create the app bundle structure
mkdir -p "X Poster.app/Contents/MacOS"
mkdir -p "X Poster.app/Contents/Resources"

# Create Info.plist
cat > "X Poster.app/Contents/Info.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.xposter.app</string>
    <key>CFBundleName</key>
    <string>X Poster</string>
    <key>CFBundleDisplayName</key>
    <string>X Poster</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOL

# Create the launcher script with better error handling
cat > "X Poster.app/Contents/MacOS/launcher" << EOL
#!/bin/bash

# Log file for debugging
LOG_FILE="${CURRENT_DIR}/xposter_log.txt"

# Output to log file
exec > "\${LOG_FILE}" 2>&1

echo "Starting X Poster app at \$(date)"
echo "Current directory: ${CURRENT_DIR}"

# Change to the app directory
cd "${CURRENT_DIR}" || { echo "Failed to change directory to ${CURRENT_DIR}"; exit 1; }

# Check if venv exists
if [ ! -f "${CURRENT_DIR}/venv/bin/activate" ]; then
    echo "Virtual environment not found at ${CURRENT_DIR}/venv"
    echo "Creating new virtual environment..."
    python3 -m venv "${CURRENT_DIR}/venv"
    source "${CURRENT_DIR}/venv/bin/activate"
    pip install tweepy python-dotenv PyQt6==6.5.0
else
    echo "Activating virtual environment..."
    source "${CURRENT_DIR}/venv/bin/activate"
fi

# Run the app with the full path to the Python interpreter
echo "Running the application..."
"${CURRENT_DIR}/venv/bin/python" "${CURRENT_DIR}/mac_app.py"
EOL

# Make the launcher script executable
chmod +x "X Poster.app/Contents/MacOS/launcher"

# Use a system icon for the app
cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AirDrop.icns "X Poster.app/Contents/Resources/AppIcon.icns"

# Move the app to the Applications folder
cp -R "X Poster.app" "/Applications/"

# Fix permissions
chmod -R 755 "/Applications/X Poster.app"

# Force Spotlight to index the app
touch "/Applications/X Poster.app"
mdimport "/Applications/X Poster.app"

# Create a Desktop shortcut
ln -sf "/Applications/X Poster.app" ~/Desktop/

echo "X Poster app has been created and installed in the Applications folder."
echo "A shortcut has been created on your Desktop."
echo "You can now launch it from Spotlight by typing 'X Poster' or from your Desktop."
echo "If you have issues, check the log file at: ${CURRENT_DIR}/xposter_log.txt"
