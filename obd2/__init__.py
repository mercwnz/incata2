# obd/__init__.py

import logging

# Configure package-wide logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("OBD package initialized")

from .devices import DEVICES
