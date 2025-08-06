#import uvicorn
#from fastapi.staticfiles import StaticFiles
#from fastapi.responses import FileResponse
#from pathlib import Path

#from app.web.api import app
#from app.logger import logger

# 设置静态文件目录
#static_path = Path(__file__).parent / "static"
#static_path.mkdir(exist_ok=True)

# 挂载静态文件目录
#app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# 设置根路由返回index.html
#@app.get("/")
#async def read_index():
 #   index_path = static_path / "index.html"
 #   return FileResponse(str(index_path))

# 健康检查接口
#@app.get("/health")
#async def health_check():
 #   return {"status": "ok"}

#if __name__ == "__main__":
 #   logger.info("启动OpenManus Web服务...")
  #  logger.info(f"静态文件目录: {static_path}")
  #  logger.info("访问地址: http://localhost:8000")
  #  uvicorn.run(app, host="0.0.0.0", port=8000) 
    
import uvicorn
import socket
from contextlib import closing
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.web.api import app
from app.logger import logger

def find_free_port(start_port=8000, max_attempts=100):
    """自动寻找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex(('0.0.0.0', port)) != 0:
                return port
    raise RuntimeError(f"No available port found in range {start_port}-{start_port+max_attempts-1}")

# 设置静态文件目录
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)

# 挂载静态文件路由
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def read_index():
    index_path = static_path / "index.html"
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found at {index_path}")
    return FileResponse(str(index_path))

@app.get("/health")
async def health_check():
    return {"status": "ok", "port": app.state.port}

if __name__ == "__main__":
    try:
        port = find_free_port()
        app.state.port = port  # 存储当前端口
        
        logger.info("启动OpenManus Web服务...")
        logger.info(f"静态文件目录: {static_path}")
        logger.info(f"访问地址: http://localhost:{port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False,
            access_log=True,
            timeout_keep_alive=60
        )
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        raise
        
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
 
