import chromadb

# 1. 初始化数据库（数据会存在内存中，重启即消失，适合实验）
chroma_client = chromadb.Client()

# 2. 创建一个“集合”（类似数据库里的表），命名为 "cat_history"
collection = chroma_client.create_collection(name="cat_history")

# 3. 添加一些具有特定语义的记忆片段
collection.add(
    documents=[
        "那只猫叫小黑，它最喜欢的太空零食是冷冻干鱼。",
        "小黑穿着一件银色的宇航服，尾巴上还挂着一个发光的球。",
        "在火星任务中，小黑成功修理了飞船的制氧系统。"
    ],
    ids=["id1", "id2", "id3"] # 每个片段需要一个唯一的 ID
)

# 4. 模拟用户提问并进行“语义搜索”
query_text = "那只猫在火星做了什么？"
results = collection.query(
    query_texts=[query_text],
    n_results=1 # 返回最相关的一个结果
)

print(f"问题: {query_text}")
print(f"检索到的最相关记忆: {results['documents'][0][0]}")