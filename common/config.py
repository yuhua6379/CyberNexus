import os

if os.environ.get("running_environment", "local").lower() == "local":
    pass

elif os.environ.get("running_environment", "gcp").lower() == "local":
    pass
