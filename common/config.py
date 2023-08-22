import os

if os.environ.get("running_environment", "local").lower() == "local":
    from .config_local import *

elif os.environ.get("running_environment", "gcp").lower() == "local":
    from .config_gcp import *
