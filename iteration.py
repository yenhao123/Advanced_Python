class RemoteControl():
    def __init__(self):
        self.channels = ["HBO", "CNN", "ABC", "ESPN"]
        self.idx = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 2
        if self.idx > len(self.channels):
            raise StopIteration
        
        return self.channels[self.idx - 1]
    
r = RemoteControl()
itr = iter(r)
print(next(itr))
print(next(itr))