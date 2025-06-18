#!/bin/bash
# Script to fix and test the TUI application

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=== AIgency Extract TUI Fix ==="
echo "This script will fix the TUI application and verify the fix."
echo "Working directory: $(pwd)"
echo

# Run the fix script
echo "Running fix script..."
python "$SCRIPT_DIR/fix_tui.py"
if [ $? -ne 0 ]; then
    echo "Fix script failed! Check fix_tui.log for details."
    exit 1
fi
echo "Fix script completed successfully."
echo

# Run the test script
echo "Running verification script..."
python "$SCRIPT_DIR/test_fix.py"
if [ $? -ne 0 ]; then
    echo "Verification script failed! Check test_fix.log for details."
    exit 1
fi
echo "Verification script completed successfully."
echo

echo "=== Fix and verification completed successfully! ==="
echo "The TUI application should now work correctly."
echo "See TUI_FIX_README.md for details about the fix."
