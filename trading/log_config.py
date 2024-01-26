import logging

logging.basicConfig(level=logging.DEBUG)

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()

# Create formatters and add it to handlers
# c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# c_handler.setFormatter(c_format)

c_handler.setLevel(logging.DEBUG)

logger.addHandler(c_handler)