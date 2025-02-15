# AIXP Demo - AI代理通信演示项目

这是一个演示AI代理之间通信的示例项目，基于AIXP（AI-Exchange Protocol）协议实现。

## 项目结构

```
aixp_demo/
├── README.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── server.py          # 服务器实现
├── agent.py           # 代理实现
├── example.py         # 使用示例
└── tests/             # 测试目录
```

## 功能特性

- AI代理注册和发现
- 代理间消息传递
- 文本处理代理示例
- 图像处理代理示例
- 完整的错误处理和日志记录

## 安装说明

1. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动服务器：
```bash
python server.py
```

2. 运行示例：
```bash
python example.py
```

## API说明

### 服务器API

1. 注册代理
- 端点：POST /register
- 功能：注册新的AI代理
- 参数：
  ```json
  {
    "agent_id": "代理ID",
    "capabilities": ["能力1", "能力2"]
  }
  ```

2. 发送消息
- 端点：POST /send_message
- 功能：发送消息给其他代理
- 参数：
  ```json
  {
    "sender_id": "发送者ID",
    "receiver_id": "接收者ID",
    "task": "任务名称",
    "data": {}
  }
  ```

3. 获取代理列表
- 端点：GET /agents
- 功能：获取所有注册的代理列表

### 代理API

1. TextProcessingAgent
- 功能：文本处理代理
- 能力：文本分析、情感分析

2. ImageProcessingAgent
- 功能：图像处理代理
- 能力：图像分析、对象检测

## 注意事项

1. 服务器默认在本地（localhost:8000）运行
2. 确保在运行示例前启动服务器
3. 所有操作都有日志记录，方便调试

## 开发计划

- [ ] 添加更多类型的代理
- [ ] 实现认证和授权机制
- [ ] 添加更多的测试用例
- [ ] 支持更多的通信协议

## 贡献指南

欢迎提交问题和改进建议！

## 许可证

MIT License 