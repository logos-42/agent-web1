from agent import AIXPAgent
import time
import logging
import sys
import traceback

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("aixp_demo/test_agents.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("开始测试代理注册")
    try:
        # 创建第一个代理
        logger.info("创建第一个测试代理")
        agent1 = AIXPAgent(
            agent_id="test_agent_1",
            capabilities=["text_processing", "chat"]
        )
        logger.info("第一个代理创建成功")
        
        # 等待一下确保注册完成
        time.sleep(2)
        
        # 创建第二个代理
        logger.info("创建第二个测试代理")
        agent2 = AIXPAgent(
            agent_id="test_agent_2",
            capabilities=["image_processing", "vision"]
        )
        logger.info("第二个代理创建成功")
        
        # 保持程序运行一段时间以观察效果
        logger.info("代理已注册，请查看Web界面观察效果")
        logger.info("程序将在30秒后自动退出")
        time.sleep(30)
        
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        logger.error("详细错误信息:")
        logger.error(traceback.format_exc())
    finally:
        logger.info("测试程序结束")

if __name__ == "__main__":
    main() 