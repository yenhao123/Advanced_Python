def count_up_to():
    count = 1
    while True:
        yield count
        count += 1


for num in count_up_to():
    if num > 5: 
        break
    else: 
        print(num)