#!/bin/bash

# Sign the app with ad-hoc signature
codesign --force --deep --sign - "/Applications/X Poster.app"

# Verify the signature
codesign -vvv --deep --strict "/Applications/X Poster.app"

echo "App has been signed with ad-hoc signature."
echo "You may need to right-click the app and select 'Open' the first time to bypass Gatekeeper."
