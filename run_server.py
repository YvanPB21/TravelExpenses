import sys
print("Testing Flask app...", file=sys.stderr, flush=True)

try:
    from app import app
    print("App imported successfully!", file=sys.stderr, flush=True)
    print("Starting Flask server...", file=sys.stderr, flush=True)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()

