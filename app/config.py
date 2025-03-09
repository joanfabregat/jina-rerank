#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

import os

VERSION = os.getenv("VERSION", "0.1.0")
BUILD_ID = os.getenv("BUILD_ID", "unknown")
COMMIT_SHA = os.getenv("COMMIT_SHA", "unknown")
PORT = os.getenv("PORT", 8000)
