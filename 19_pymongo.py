from pymongo import MongoClient


#实例化client，建立连接
client = MongoClient(host="127.0.0.1", port=27017)
collection = client["test1"]["t250"]

# 插入一条数据
ret1 = collection.insert({"name":"quin","age":"22"})
print(ret1)

# 插入多条数据
data_list = [{"name":"test{}"}.format(i) for i in range(10)]
collection.insert_many(data_list)

# 查询一个记录
t = collection.find_one({"name":"quin"})
print(t)

# 查询所有记录
t = collection.find({"name":"quin"})
print(t)


