import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv


# 这里的 base_url 需要根据你选择的平台更换
# DeepSeek: https://api.deepseek.com
# 阿里云: https://dashscope.aliyuncs.com/compatible-mode/v1
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

db = chromadb.Client()
collection = db.get_or_create_collection(name="cat_memory")

# 初始化数据库
def get_memory(query):
    # 检索最相关的 1 条记忆
    results = collection.query(query_texts=[query], n_results=1)
    if results['documents'] and results['distances'][0][0] < 0.5: # 阈值过滤
        return results['documents'][0][0]
    return None

# 聊天
def chat_with_memory():
    print("🐱 太空猫管家已上线！（输入 'quit' 退出）")
    
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'quit': break
        
        # 1. 提取记忆
        past_memory = get_memory(user_input)
        
        # 2. 构造提示词
        prompt = user_input
        if past_memory:
            prompt = f"【已知背景：{past_memory}】\n用户的当前问题：{user_input}"
        
        # 3. 请求 AI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是有记忆的太空猫，请参考背景亲切地回答。"},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        print(f"太空猫: {answer}")
        
        # 4. 关键词触发存储（比如提到“小黑”或“喜欢”）
        if any(key in user_input for key in ["小黑", "喜欢", "名字", "吃"]):
            mem_id = f"mem_{len(collection.get()['ids'])}"
            collection.add(
                documents=[f"用户提到：{user_input}；你的回答：{answer}"],
                ids=[mem_id]
            )
            print(f"系统提示：已将该信息存入记忆库 💾")

# 启动！
chat_with_memory()