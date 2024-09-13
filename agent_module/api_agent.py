from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import AgentBot

# Создаем экземпляр FastAPI
app = FastAPI()

# Экземпляр AgentBot
agent = AgentBot()

# Модель данных для запросов
class QueryRequest(BaseModel):
    answer: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    """
    API endpoint для обработки пользовательского ввода.
    Ожидает JSON с ключом 'answer'.
    Возвращает результат метода 'scenario' из AgentBot.
    """
    answer = request.answer

    try:
        # Вызов метода scenario в AgentBot
        result = agent.scenario(answer)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
