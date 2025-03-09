#  Copyright (c) 2025 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
