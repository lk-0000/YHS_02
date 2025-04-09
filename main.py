import os
import logging
from app import app

# Configure logging based on environment
log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Set debug mode based on environment
debug_mode = os.environ.get('FLASK_ENV', 'development') != 'production'

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Start the app with enhanced error handling
    try:
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
