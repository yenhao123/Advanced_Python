import time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()  # 開始時間
        result = func(*args, **kwargs)  # 執行原本的函式
        end = time.time()    # 結束時間
        print(f"Function '{func.__name__}' took {end - start:.6f} seconds.")
        return result
    return wrapper   
    
@timer
def say_hello():
    print("Hello!")

say_hello()