from celery import Celery

app = Celery(
    "tasks",
    broker="amqp://127.0.0.1:5672//",
    backend="db+sqlite:///results.sqlite",
)


@app.task(ignore_result=False)
def add(x: int, y: int) -> int:
    result = x + y
    print(f"add function {result =}")
    return result
