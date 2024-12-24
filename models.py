from pydantic import BaseModel
from typing import List, Optional, Dict

class Question(BaseModel):
    context: str