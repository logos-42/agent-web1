from agent import AIXPAgent
import time
import logging
import sys
import traceback
import requests
from requests.exceptions import RequestException

# 强制刷新输出
sys.stdout.reconfigure(line_buffering=True)

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True  # 强制重新配置日志
)

# 设置requests的日志级别
logging.getLogger('requests').setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def wait_for_server(url: str = "http://127.0.0.1:9000", max_retries: int = 5):
    """等待服务器启动"""
    print("开始检查服务器状态...")  # 直接使用print进行调试
    for i in range(max_retries):
        try:
            print(f"尝试连接服务器 ({i+1}/{max_retries})")  # 直接使用print进行调试
            response = requests.get(url)
            print(f"服务器响应状态码: {response.status_code}")  # 直接使用print进行调试
            if response.status_code == 200:
                print("服务器连接成功！")  # 直接使用print进行调试
                return True
            else:
                print(f"服务器返回非200状态码: {response.status_code}")  # 直接使用print进行调试
        except RequestException as e:
            print(f"连接失败: {str(e)}")  # 直接使用print进行调试
        time.sleep(2)
    return False

def main():
    print("\n=== 开始测试消息发送 ===\n")  # 直接使用print进行调试
    
    # 首先等待服务器启动
    if not wait_for_server():
        print("无法连接到服务器，测试终止")  # 直接使用print进行调试
        return
    
    try:
        print("\n1. 创建并注册代理...")  # 直接使用print进行调试
        # 创建第一个代理
        agent1 = AIXPAgent(
            agent_id="message_agent_1",
            capabilities=["text_processing", "chat"]
        )
        print("代理1创建成功")  # 直接使用print进行调试
        
        time.sleep(2)
        
        # 创建第二个代理
        agent2 = AIXPAgent(
            agent_id="message_agent_2",
            capabilities=["image_processing", "vision"]
        )
        print("代理2创建成功")  # 直接使用print进行调试
        
        time.sleep(2)
        
        print("\n2. 验证代理注册状态...")  # 直接使用print进行调试
        agents = agent1.get_registered_agents()
        print(f"当前注册的代理: {agents}")  # 直接使用print进行调试
        
        if "message_agent_1" not in agents or "message_agent_2" not in agents:
            print("代理注册失败，请检查服务器日志")  # 直接使用print进行调试
            return
        
        print("\n3. 开始消息测试...")  # 直接使用print进行调试
        for i in range(3):
            print(f"\n--- 测试消息 {i+1}/3 ---")  # 直接使用print进行调试
            
            message = {
                "content": f"测试消息 {i+1}",
                "timestamp": time.time()
            }
            
            print(f"代理1 -> 代理2: {message}")  # 直接使用print进行调试
            try:
                response = agent1.send_message(
                    receiver_id="message_agent_2",
                    task="process_message",
                    data=message
                )
                print(f"发送结果: {response}")  # 直接使用print进行调试
            except Exception as e:
                print(f"发送消息失败: {str(e)}")  # 直接使用print进行调试
                continue
            
            time.sleep(2)
            
            reply = {
                "reply_to": message["content"],
                "status": "received",
                "timestamp": time.time()
            }
            
            print(f"代理2 -> 代理1: {reply}")  # 直接使用print进行调试
            try:
                response = agent2.send_message(
                    receiver_id="message_agent_1",
                    task="message_reply",
                    data=reply
                )
                print(f"回复结果: {response}")  # 直接使用print进行调试
            except Exception as e:
                print(f"回复消息失败: {str(e)}")  # 直接使用print进行调试
            
            time.sleep(2)
            
        print("\n=== 消息测试完成 ===")  # 直接使用print进行调试
        
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")  # 直接使用print进行调试
        print("详细错误信息:")  # 直接使用print进行调试
        traceback.print_exc()
    finally:
        print("\n测试程序结束")  # 直接使用print进行调试

if __name__ == "__main__":
    main() 