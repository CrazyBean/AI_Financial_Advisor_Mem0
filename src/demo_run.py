import os
import sys

# -----------------------------------------------------
# API Key 设置区
# -----------------------------------------------------
MY_ZHIPU_KEY = "YOUR_API_KEY_HERE"

def main():
    global MY_ZHIPU_KEY
    
    print("=====================================================")
    print(" 🤖 欢迎使用基于 Mem0 的私人财富顾问系统 (国内大模型驱动)")
    print("=====================================================\n")

    # 1. 智能 API Key 注入
    if MY_ZHIPU_KEY == "YOUR_API_KEY_HERE" or not MY_ZHIPU_KEY.strip():
        print("🔑 【身份认证】系统检测到您尚未在代码中配置 API Key。")
        user_input = input(" 👉 请在此处粘贴您的智谱清言(ZhipuAI) API Key 并按回车: ").strip()
        print("")
        
        if not user_input:
            print("❌ 未检测到输入，程序退出。")
            return
        MY_ZHIPU_KEY = user_input

    os.environ["ZHIPU_API_KEY"] = MY_ZHIPU_KEY

    # 必须在环境变量设置好之后再导入 Advisor
    try:
        from advisor import FinancialAdvisor
    except Exception as e:
        print(f"❌ 依赖加载失败，请检查 requirements 是否安装完整: {e}")
        sys.exit(1)

    # 2. 实例化我们的私人财富顾问
    print("⏳ 正在初始化 Mem0 记忆引擎与智谱大模型，请稍候...\n")
    try:
        advisor = FinancialAdvisor()
    except Exception as e:
        print(f"❌ 初始化失败！可能原因：API Key 错误。\n报错详情: {e}")
        sys.exit(1)
        
    user_id = "client_huang_001"

    # 3. 模拟阶段一：日常沟通，系统隐式记录用户画像
    print(">>> 【阶段一：资产状况与偏好沟通】")
    user_message_1 = "我还有两年就要退休了，现在手里有100万闲钱。我心脏不好，受不了股票市场的剧烈波动，尤其是之前买过比特币亏惨了，以后绝对不碰加密货币和高科技股。"
    print(f"User: {user_message_1}\n")
    try:
        advisor.chat_and_remember(user_id=user_id, message=user_message_1)
    except Exception as e:
        print(f"\n❌ 连接 API 失败！报错详情: {e}")
        sys.exit(1)

    print("\n----------------------------------------------------\n")

    # 4. 模拟阶段二：在未来的某一天，用户发起投资咨询
    print(">>> 【阶段二：未来某日的投资咨询测试】")
    user_query = "最近市场有什么好机会吗？这100万帮我推荐几个投资标的。"
    print(f"User: {user_query}")
    
    # 系统根据记忆生成个性化方案
    try:
        advice = advisor.get_personalized_advice(user_id=user_id, query=user_query)
        print("\n🤖 AI 顾问建议:")
        print(advice)
    except Exception as e:
        print(f"\n❌ 生成建议失败！报错详情: {e}")

    print("\n=====================================")
    print(" 🎉 演示结束。")
    print("=====================================")

if __name__ == "__main__":
    main()