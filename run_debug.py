import sys
import traceback

try:
    from app import app
    print("App imported successfully", file=sys.stderr)
    sys.stderr.flush()
    app.run(debug=True, host='0.0.0.0', port=5000)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    input("Press Enter to continue...")

