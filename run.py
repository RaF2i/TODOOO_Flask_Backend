# This is the main entry point to start the Flask application.

from app import create_app
import os

# Create the Flask app instance using the app factory pattern
app = create_app()

if __name__ == '__main__':
    # Run the app
    # The host '0.0.0.0' makes the server accessible from your local network,
    # which is useful for testing from other devices.
    # The port 5001 is chosen to avoid conflicts with the Next.js frontend (usually on 3000).
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
