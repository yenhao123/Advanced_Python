

# Advanced Python

Chapters
* OOP
* Exception
* Iterator & Generator
* Decorator
* Multi-threading
* Multi-processing
* Unitest
* Others (yeild v.s. return)

## OOP

Object-Oriented Programming (OOP) make programs more flexible and extensible. 

Three main focuses OOP:
* **Encapsulation**: Hides internal details, allowing users to interact only with the public interface.
* **Inheritance**: Extends functionalities and promotes code reuse.
* **Polymorphism**: Different classes can share the same interface behavior.

Common magic methods (dunder methods):
* `__len__`, `__iter__`, and other frequently used methods.
* Use `dir(object)` to inspect an object's available attributes and methods.

---

## Exception

Handles errors that occur during program execution, improving stability and maintainability.

Basic template:
```python
try:
    # Code that might raise an error
except SpecificError as e:
    # Code to handle the error
    raise Exception("Custom error message")
finally:
    # Code that always executes, e.g., closing files or releasing resources
```

Key concepts:
* `Exception` is a built-in Python error type.
* `except` blocks are executed when a matching error is encountered.

---

## Iterator & Generator

Techniques for saving memory and generating data lazily.

### Iterator

* Objects that allow you to retrieve elements one at a time.
* **Example**: Handing out race bibs — prepared beforehand, given one at a time.

Basic usage:
```python
lst = [1, 2, 3, 4]
it = iter(lst)
print(next(it))  # 1
print(next(it))  # 2
```
Using a `for` loop automatically turns a list into an iterator and retrieves items one by one.

### Generator

* Dynamically generates data without producing all items at once.
* **Example**: Printing receipts — generate one for each customer when needed.

Example:
```python
def count_up_to():
    count = 1
    while True:
        yield count
        count += 1

for num in count_up_to():
    if num > 5:
        break
    print(num)
```
---

## Decorator

A technique to add extra functionality to existing functions, such as timing, logging, or caching.

Pros: Modularity, Readability

Basic template:
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # Decoration before
        result = func(*args, **kwargs)
        # Decoration after
        return result
    return wrapper

@my_decorator
def func():
    pass
```

Timer example:
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' took {end - start:.6f} seconds.")
        return result
    return wrapper

@timer
def say_hello():
    print("Hello!")

say_hello()
```

---

## Multi-threading

Running multiple threads concurrently within the same process, suitable for **I/O-bound tasks**.

Features:
* Threads share **code sections, data sections, and system resources** (e.g., open files).
* Each thread has its own stack and program counter.

Basic example:
```python
import threading
import time

def worker():
    print(f"Thread {threading.current_thread().name} starts")
    time.sleep(2)
    print(f"Thread {threading.current_thread().name} ends")

if __name__ == "__main__":
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Main thread ends")
```

Limitations:
* Due to the **Global Interpreter Lock (GIL)**, only one thread can execute Python bytecode at a time.
* Best suited for I/O-bound tasks such as networking, disk I/O, and user input.

---

## Multi-processing

Launching multiple independent processes, suitable for **CPU-bound tasks** and bypassing the GIL limitation.

Example (running the same function multiple times):
```python
import multiprocessing

def square(x):
    return x * x

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        numbers = [1, 2, 3, 4, 5]
        result = pool.map(square, numbers)
    print(result)
```

Shared variables:
```python
import multiprocessing

def worker(shared_list):
    for i in range(5):
        shared_list.append(i)

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_list = manager.list()

    p = multiprocessing.Process(target=worker, args=(shared_list,))
    p.start()
    p.join()

    print("Result:", list(shared_list))
```

Shared file writing (using a lock to prevent race conditions):
```python
import multiprocessing

def write_file(lock, filename, content):
    with lock:
        with open(filename, 'a') as f:
            f.write(content + '\n')

if __name__ == "__main__":
    lock = multiprocessing.Lock()
    filename = "shared_output.txt"

    p1 = multiprocessing.Process(target=write_file, args=(lock, filename, "Process 1 writing"))
    p2 = multiprocessing.Process(target=write_file, args=(lock, filename, "Process 2 writing"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Done writing.")
```

## Unitest

### Rules

* The test file name must start with `test_`.
* The test function name must start with `test_`.
* The test class name must start with `Test`.

**Run all tests**:
```bash
python3 -m pytest
```

---

### Skip Testing

* `@pytest.mark.skip(reason="Passed it")`
* `@pytest.mark.skipif(sys.version_info > (3, 5), reason="Passed it")`: Skip if Python version > 3.5.
* **Run a specific test function**:  
  ```bash
  pytest -k {substring of function name}
  ```
* **Run tests with specific markers**:
  ```bash
  pytest -m {marker name}
  ```

**Bug Note**:  
When running `pytest -k calc`, even test functions without "calc" in their name might still be tested.  
This happens because `-k` matches **the entire path**, including filenames.  
If the file name contains "calc", all functions inside that file will be included.

---

### Fixture

#### Goal
Helps automatically **set up resources before a test** and **clean up after the test**.  
> e.g., Before each test run, you can prepare data, connect to a database, or initialize environments to avoid repeated loading overhead.

#### Steps

1. Define a fixture function and specify the resource it returns (before `yield`).
2. During testing, the fixture’s returned value is automatically injected into the test function.
3. After the test, the resource is cleaned up (after `yield`).

#### Example

```python
import pytest

@pytest.fixture
def resource():
    # Setup
    print("== Setting up resource ==")
    res = {"db_conn": "Connected to database"}
    # Testing
    yield res
    # Teardown
    print("== Cleaning up resource ==")
    res["db_conn"] = None

def test_example_1(resource):
    print(f"test_example_1 using {resource}")
    assert resource["db_conn"] == "Connected to database"

def test_example_2(resource):
    print(f"test_example_2 using {resource}")
    assert resource["db_conn"] == "Connected to database"
```

> * pytest first runs the fixture function and captures its return value.  
> * Then, the returned value is automatically injected into the corresponding test function for testing.

## Others
### yeild vs return
| | `return` | `yield` |
|:---|:---|:---|
| Purpose | Ends the function and returns a value | Pauses the function and yields a value; resumes from there next time |
| Does it end the function? | ✅ Immediately ends | ❌ No, just pauses |
| Suitable for | Returning a single result | Large data streams / Lazy loading |
| Function type | Regular function | Generator function |

---

✅ `return` Example:

```python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)  # Output: 5
```
- `return` directly sends the result back and ends the function.

---

✅ `yield` Example:

```python
def count_up():
    yield 1
    yield 2
    yield 3

gen = count_up()
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3
```
- `yield` produces one value at a time, **pausing the function between each yield**, and resumes from the same point on the next call.

## References
codebasics

https://www.youtube.com/watch?v=l32bsaIDoWk&list=PLeo1K3hjS3uv5U-Lmlnucd7gqF-3ehIh0&index=36