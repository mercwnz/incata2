# gps/__init__.py

import logging

# Configure package-wide logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("GPS package initialized")

from .nmea import NMEA
from .devices import DEVICES
