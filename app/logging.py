#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
