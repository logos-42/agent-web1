from agent import TextProcessingAgent, ImageProcessingAgent
import time
import requests
from requests.exceptions import RequestException
import logging
import sys
import os

# 禁用代理设置
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def wait_for_server(url: str, max_retries: int = 10, retry_delay: int = 3):
    """等待服务器启动"""
    logger.debug("开始等待服务器启动...")  # 添加调试信息
    session = requests.Session()
    session.proxies = {'http': None, 'https': None}
    for i in range(max_retries):
        try:
            logger.debug(f"尝试连接服务器 {i+1}/{max_retries}")  # 添加调试信息
            response = session.get(url)
            if response.status_code == 200:
                logger.info("服务器已启动并运行")
                return True
        except RequestException as e:
            logger.warning(f"服务器未就绪，尝试 {i+1}/{max_retries}: {str(e)}")
        time.sleep(retry_delay)
    return False

def main():
    logger.debug("开始运行主程序...")  # 添加调试信息
    # 等待服务器启动
    server_url = "http://127.0.0.1:8000"
    if not wait_for_server(server_url):
        logger.error("服务器启动失败")
        return

    try:
        logger.debug("创建代理实例...")  # 添加调试信息
        # 创建两个不同类型的代理
        text_agent = TextProcessingAgent("text_agent_1")
        image_agent = ImageProcessingAgent("image_agent_1")

        # 等待代理注册完成
        logger.debug("等待代理注册完成...")  # 添加调试信息
        time.sleep(2)

        # 获取已注册的代理列表
        logger.info("\n已注册的代理：")
        agents = text_agent.get_registered_agents()
        logger.info(agents)

        # 示例：文本代理处理文本
        text = "这是一个示例文本，用于测试AI代理之间的通信。"
        logger.debug(f"处理文本: {text}")  # 添加调试信息
        text_result = text_agent.process_text(text)
        logger.info("\n文本处理结果：")
        logger.info(text_result)

        # 示例：文本代理向图像代理发送消息
        logger.debug("发送消息给图像代理...")  # 添加调试信息
        message_result = text_agent.send_message(
            receiver_id="image_agent_1",
            task="process_text_result",
            data=text_result
        )
        logger.info("\n消息发送结果：")
        logger.info(message_result)

        # 示例：图像代理处理图像
        image_url = "http://example.com/sample.jpg"
        logger.debug(f"处理图像: {image_url}")  # 添加调试信息
        image_result = image_agent.process_image(image_url)
        logger.info("\n图像处理结果：")
        logger.info(image_result)

    except Exception as e:
        logger.error(f"运行示例时发生错误: {str(e)}")
        logger.exception("详细错误信息：")  # 添加详细错误信息

if __name__ == "__main__":
    main() 