import requests
from typing import Dict, Any, List
import logging
import os
import sys
import json

# 禁用代理设置
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AIXPAgent:
    def __init__(self, agent_id: str, capabilities: List[str], server_url: str = "http://127.0.0.1:9000"):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.server_url = server_url
        # 设置请求不使用代理
        self.session = requests.Session()
        self.session.proxies = {'http': None, 'https': None}
        logger.info(f"初始化代理 {agent_id}，能力：{capabilities}")
        self.register()

    def register(self):
        """向服务器注册代理"""
        try:
            logger.info(f"正在注册代理 {self.agent_id}...")
            response = self.session.post(
                f"{self.server_url}/register",
                json={"agent_id": self.agent_id, "capabilities": self.capabilities}
            )
            response_text = response.text
            logger.info(f"注册响应：{response.status_code} - {response_text}")
            
            if response.status_code == 200:
                logger.info(f"代理 {self.agent_id} 注册成功")
                return response.json()
            else:
                error_msg = f"代理 {self.agent_id} 注册失败: {response_text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"注册代理时发生错误: {str(e)}")
            raise

    def send_message(self, receiver_id: str, task: str, data: Dict[str, Any]):
        """发送消息给其他代理"""
        try:
            message = {
                "sender_id": self.agent_id,
                "receiver_id": receiver_id,
                "task": task,
                "data": data
            }
            logger.info(f"发送消息: {json.dumps(message, ensure_ascii=False)}")
            
            response = self.session.post(
                f"{self.server_url}/send_message",
                json=message
            )
            response_text = response.text
            logger.info(f"发送响应：{response.status_code} - {response_text}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"发送消息失败: {response_text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"发送消息时发生错误: {str(e)}")
            raise

    def get_registered_agents(self):
        """获取所有注册的代理列表"""
        try:
            logger.info("获取已注册的代理列表...")
            response = self.session.get(f"{self.server_url}/agents")
            response_text = response.text
            logger.info(f"获取响应：{response.status_code} - {response_text}")
            
            if response.status_code == 200:
                agents = response.json()
                logger.info(f"成功获取到 {len(agents)} 个代理")
                return agents
            else:
                error_msg = f"获取代理列表失败: {response_text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"获取代理列表时发生错误: {str(e)}")
            raise

# 示例：文本处理代理
class TextProcessingAgent(AIXPAgent):
    def __init__(self, agent_id: str):
        logger.info(f"创建文本处理代理 {agent_id}")
        super().__init__(agent_id, capabilities=["text_analysis", "sentiment_analysis"])

    def process_text(self, text: str) -> Dict[str, Any]:
        """处理文本的示例方法"""
        try:
            logger.info(f"处理文本: {text}")
            # 这里可以添加实际的文本处理逻辑
            word_count = len(text.split())
            result = {
                "word_count": word_count,
                "text_length": len(text),
                "sample_analysis": "这是一个示例分析"
            }
            logger.info(f"文本处理结果: {result}")
            return result
        except Exception as e:
            logger.error(f"处理文本时发生错误: {str(e)}")
            raise

# 示例：图像处理代理
class ImageProcessingAgent(AIXPAgent):
    def __init__(self, agent_id: str):
        logger.info(f"创建图像处理代理 {agent_id}")
        super().__init__(agent_id, capabilities=["image_analysis", "object_detection"])

    def process_image(self, image_url: str) -> Dict[str, Any]:
        """处理图像的示例方法"""
        try:
            logger.info(f"处理图像: {image_url}")
            # 这里可以添加实际的图像处理逻辑
            result = {
                "detected_objects": ["示例对象1", "示例对象2"],
                "image_format": "jpg",
                "sample_analysis": "这是一个示例图像分析"
            }
            logger.info(f"图像处理结果: {result}")
            return result
        except Exception as e:
            logger.error(f"处理图像时发生错误: {str(e)}")
            raise 