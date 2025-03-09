#  Copyright (c) 2025 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

import os

VERSION = os.getenv("VERSION", "0.1.0")
BUILD_ID = os.getenv("BUILD_ID", "unknown")
COMMIT_SHA = os.getenv("COMMIT_SHA", "unknown")
PORT = os.getenv("PORT", 8000)
