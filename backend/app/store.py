from typing import Dict
from threading import Lock

job_store: Dict[str, dict] = {}
# prevents race condition when updating the job_store
lock = Lock() 
