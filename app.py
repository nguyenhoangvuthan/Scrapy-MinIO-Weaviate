import shutil
import subprocess
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class SpiderRequest(BaseModel):
    spider_name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/run-spider/")
async def run_spider(spider_request: SpiderRequest):
    spider_name: str = spider_request.spider_name
    if not shutil.which('scrapy'):
        raise HTTPException(status_code=500, detail="Scrapy not found in PATH")
    try:
        # Run Scrapy spider using subprocess
        process = subprocess.Popen(
            ['scrapy', 'crawl', spider_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode())

        return {"status": "Scraping completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)