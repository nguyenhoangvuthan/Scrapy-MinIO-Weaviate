import uvicorn
from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("run-spider")
async def run_spider(spider_name):
    process = CrawlerProcess(get_project_settings())
    await process.crawl(spider_name)
    process.start()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)