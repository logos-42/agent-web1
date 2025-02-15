from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Set
import uvicorn
import logging
import json
import sys
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AIXP Demo")

# 存储已注册的代理
registered_agents: Dict[str, List[str]] = {}

# 存储活动的 WebSocket 连接
active_connections: Set[WebSocket] = set()

# 存储消息历史
message_history: List[Dict[str, Any]] = []

class Message(BaseModel):
    sender_id: str
    receiver_id: str
    task: str
    data: Dict[str, Any]
    
    class Config:
        arbitrary_types_allowed = True

class AgentInfo(BaseModel):
    agent_id: str
    capabilities: List[str]
    
    class Config:
        arbitrary_types_allowed = True

# WebSocket 连接管理
async def broadcast_update():
    """向所有连接的客户端广播更新"""
    if active_connections:
        message = {
            "event": "update",
            "data": {
                "status": "running",
                "registered_agents": len(registered_agents),
                "agents": [
                    {"id": agent_id, "capabilities": capabilities}
                    for agent_id, capabilities in registered_agents.items()
                ],
                "messages": message_history
            }
        }
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {str(e)}")
                try:
                    active_connections.remove(connection)
                except:
                    pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """处理 WebSocket 连接"""
    await websocket.accept()
    active_connections.add(websocket)
    try:
        # 发送初始状态
        await broadcast_update()
        # 保持连接并处理消息
        while True:
            data = await websocket.receive_text()
            # 这里可以添加消息处理逻辑
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        active_connections.remove(websocket)

@app.get("/")
async def get_html():
    """返回前端页面"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AIXP 智能体演示</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f0f0f0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .status {
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 3px;
            }
            .running {
                background-color: #d4edda;
                color: #155724;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
            }
            .agent-list {
                margin-top: 20px;
            }
            .agent-item {
                padding: 10px;
                margin-bottom: 5px;
                background-color: #e9ecef;
                border-radius: 3px;
            }
            .message-list {
                margin-top: 20px;
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                padding: 10px;
            }
            .message-item {
                padding: 10px;
                margin-bottom: 5px;
                border-bottom: 1px solid #dee2e6;
            }
            .message-header {
                font-weight: bold;
                color: #495057;
                margin-bottom: 5px;
            }
            .message-content {
                color: #212529;
                margin-left: 10px;
            }
            .message-time {
                color: #6c757d;
                font-size: 0.85em;
                margin-top: 5px;
            }
        </style>
        <script>
            let ws;
            let reconnectAttempts = 0;
            const maxReconnectAttempts = 5;

            function connect() {
                ws = new WebSocket('ws://' + window.location.host + '/ws');
                
                ws.onopen = function() {
                    console.log('已连接到服务器');
                    reconnectAttempts = 0;
                    updateStatus('已连接', true);
                };

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    updateUI(data);
                };

                ws.onclose = function() {
                    console.log('与服务器断开连接');
                    updateStatus('已断开连接', false);
                    if (reconnectAttempts < maxReconnectAttempts) {
                        reconnectAttempts++;
                        setTimeout(connect, 2000);
                    }
                };

                ws.onerror = function(error) {
                    console.error('WebSocket错误:', error);
                    updateStatus('错误: ' + error, false);
                };
            }

            function updateStatus(message, isRunning) {
                const statusDiv = document.getElementById('status');
                statusDiv.textContent = message;
                statusDiv.className = 'status ' + (isRunning ? 'running' : 'error');
            }

            function formatTime(timestamp) {
                const date = new Date(timestamp * 1000);
                return date.toLocaleTimeString();
            }

            function updateUI(data) {
                if (data.event === 'update') {
                    // 更新代理列表
                    const agentList = document.getElementById('agent-list');
                    agentList.innerHTML = '';
                    data.data.agents.forEach(agent => {
                        const agentDiv = document.createElement('div');
                        agentDiv.className = 'agent-item';
                        agentDiv.textContent = `智能体: ${agent.id} - 能力: ${agent.capabilities.join(', ')}`;
                        agentList.appendChild(agentDiv);
                    });

                    // 更新消息列表
                    const messageList = document.getElementById('message-list');
                    messageList.innerHTML = '';
                    if (data.data.messages) {
                        data.data.messages.forEach(msg => {
                            const msgDiv = document.createElement('div');
                            msgDiv.className = 'message-item';
                            
                            const headerDiv = document.createElement('div');
                            headerDiv.className = 'message-header';
                            headerDiv.textContent = `${msg.sender_id} -> ${msg.receiver_id} (${msg.task})`;
                            
                            const contentDiv = document.createElement('div');
                            contentDiv.className = 'message-content';
                            contentDiv.textContent = JSON.stringify(msg.data, null, 2);
                            
                            const timeDiv = document.createElement('div');
                            timeDiv.className = 'message-time';
                            timeDiv.textContent = msg.timestamp;
                            
                            msgDiv.appendChild(headerDiv);
                            msgDiv.appendChild(contentDiv);
                            msgDiv.appendChild(timeDiv);
                            messageList.appendChild(msgDiv);
                        });
                        
                        // 自动滚动到最新消息
                        messageList.scrollTop = messageList.scrollHeight;
                    }
                }
            }

            window.onload = connect;
        </script>
    </head>
    <body>
        <div class="container">
            <h1>AIXP 智能体演示</h1>
            <div id="status" class="status">正在连接...</div>
            <div class="agent-list">
                <h2>已注册的智能体</h2>
                <div id="agent-list"></div>
            </div>
            <div class="message-list">
                <h2>消息历史</h2>
                <div id="message-list"></div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/register")
async def register_agent(agent_info: AgentInfo):
    """注册一个新的AI代理"""
    try:
        registered_agents[agent_info.agent_id] = agent_info.capabilities
        logger.info(f"Agent {agent_info.agent_id} registered successfully")
        
        # 添加注册消息到历史记录
        message_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": "system",
            "receiver_id": "all",
            "task": "agent_registered",
            "data": {
                "agent_id": agent_info.agent_id,
                "capabilities": agent_info.capabilities
            }
        })
        
        # 广播更新
        await broadcast_update()
        return {
            "status": "success",
            "message": f"Agent {agent_info.agent_id} registered successfully",
            "agent_id": agent_info.agent_id,
            "capabilities": agent_info.capabilities
        }
    except Exception as e:
        logger.error(f"Error registering agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_message")
async def send_message(message: Message):
    """处理代理之间的消息传递"""
    try:
        if message.receiver_id not in registered_agents:
            raise HTTPException(status_code=404, detail=f"Receiver {message.receiver_id} not found")
        
        # 添加消息到历史记录
        message_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "task": message.task,
            "data": message.data
        })
        
        # 保持消息历史在合理范围内
        if len(message_history) > 100:
            message_history.pop(0)
        
        # 广播更新
        await broadcast_update()
        
        return {
            "status": "success",
            "message": "Message delivered",
            "receiver": message.receiver_id,
            "task": message.task
        }
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """列出所有注册的代理"""
    try:
        return registered_agents
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting AIXP Demo server")
    uvicorn.run(app, host="127.0.0.1", port=9000) 