"""
微信个人号机器人
基于 wxpy 库的简单微信机器人实现
"""

from wxpy import *
from config import REPLY_RULES, ENABLE_LOGGING, LOG_FILE
import logging
from datetime import datetime

# 配置日志
if ENABLE_LOGGING:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
else:
    logger = None

def log_message(message):
    """记录日志"""
    if logger:
        logger.info(message)

def main():
    """主函数"""
    print("=" * 50)
    print("微信机器人启动中...")
    print("=" * 50)
    
    # 初始化机器人
    # 参数说明：
    # cache_path='wxpy.pkl' - 缓存登录信息
    try:
        bot = Bot(cache_path='wxpy.pkl')
        print("✅ 登录成功！")
        print(f"✅ 当前账号: {bot.self.name}")
        log_message(f"机器人启动成功，账号: {bot.self.name}")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        log_message(f"登录失败: {e}")
        return
    
    print("\n" + "=" * 50)
    print("机器人已启动，等待消息...")
    print("=" * 50 + "\n")
    
    # 处理消息的函数
    @bot.register()
    def handle_message(msg):
        """
        处理所有消息的函数
        msg: 消息对象
        """
        try:
            # 获取消息内容
            message_text = msg.text.strip()
            sender_name = msg.sender.name
            
            # 打印收到的消息
            print(f"\n📨 收到消息来自 {sender_name}")
            print(f"   内容: {message_text}")
            
            log_message(f"收到来自 {sender_name} 的消息: {message_text}")
            
            # 检查是否匹配回复规则
            if message_text in REPLY_RULES:
                reply_content = REPLY_RULES[message_text]
                
                # 发送回复
                msg.reply(reply_content)
                
                print(f"✅ 已回复: {reply_content}")
                log_message(f"已回复 {sender_name}: {reply_content}")
        
        except Exception as e:
            print(f"❌ 处理消息时出错: {e}")
            log_message(f"处理消息时出错: {e}")
    
    # 保持机器人运行
    print("💡 提示: 按 Ctrl+C 可以停止机器人\n")
    
    try:
        embed()  # 进入交互模式，保持机器人运行
    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("机器人已关闭")
        print("=" * 50)
        log_message("机器人已关闭")

if __name__ == '__main__':
    main()