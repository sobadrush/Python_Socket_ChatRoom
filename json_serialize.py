import json

package = {"id": "player1", "x": 100, "y": 200, "hp": 5}

# 打包成字串
string_data = json.dumps(package) 
print("轉換後的字串是：", string_data)

# 拆開變成字典
original_dict = json.loads(string_data) 
print("這是一個字典物件，我們可以直接拿裡面的值：", original_dict['x'])