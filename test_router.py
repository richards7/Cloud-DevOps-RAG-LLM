import traceback
from app.llm.router import LLMRouter

router = LLMRouter()
try:
    print(router.generate('What is a Docker image?'))
except Exception as e:
    traceback.print_exc()
