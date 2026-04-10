import threading
import requests
import time

api_urls = [
  "https://official-joke-api.appspot.com/random_joke",
  "https://dog.ceo/api/breeds/image/random",
  "https://api.agify.io?name=steve",
  "https://randomuser.me/api/",
  "https://api.adviceslip.com/advice"
]

def fetchExternalApi(_url):
  print(f"[fetchExternalApi] url = {_url}")
  start_time = time.time()
  try:
    response = requests.get(
        _url,
        timeout=5
    )
    
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"data = {data}")
        return end_time - start_time
    else:
        print(f"伺服器錯誤：{response.status_code}")
  except:
    print("請求失敗")
  finally:
    end_time = time.time()
    print(f"\033[31m執行時間：{(end_time - start_time):.3f} 秒\033[0m")  # 紅色顯示

if __name__ == "__main__":
  elapsed_time = 0 # 計時開始
  
  start_time = time.time()
  th1 = threading.Thread(target=fetchExternalApi, args=(api_urls[0],)) # 逗號必要，才會是 tuple，否則只是字串
  th2 = threading.Thread(target=fetchExternalApi, args=(api_urls[1],))
  th3 = threading.Thread(target=fetchExternalApi, args=(api_urls[2],))
  th4 = threading.Thread(target=fetchExternalApi, args=(api_urls[3],))
  th5 = threading.Thread(target=fetchExternalApi, args=(api_urls[4],))
  
  th1.start()
  th2.start()
  th3.start()
  th4.start()
  th5.start()
  
  th1.join()
  th2.join()
  th3.join()
  th4.join()
  th5.join()
  
  end_time = time.time() # 計時結束
  
  print(f"\033[32m所有請求已發出，等待結果中...\033[0m")  # 綠色顯示
  print(f"\033[32m總執行時間：{(end_time - start_time):.3f} 秒\033[0m")  # 綠色顯示