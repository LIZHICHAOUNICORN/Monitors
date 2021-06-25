from monitors.celery import app

@app.task
def test_celery(x, y):
    time.sleep(3)
    return x * y
 
