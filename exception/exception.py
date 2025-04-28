def process_file():
    try:
        f = open("data.txt", "r")
        content = f.read()
        result = 10 / 0  # 製造錯誤
    except ZeroDivisionError as e:
        print(f"除以零錯誤：{e}")
        raise Exception("無法運算")  # 自訂錯誤
    except FileNotFoundError as e:
        print(f"檔案找不到：{e}")
    finally:
        print("一定會執行這裡")
        if 'f' in locals():
            f.close()

process_file()