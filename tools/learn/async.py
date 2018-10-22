import asyncio
import types

@asyncio.coroutine
def hello():
    print('api called....')
    r = yield from asyncio.sleep(10)
    print('api called again')

def function():
    return 1

def generator():
    yield 1

async def function_a():
    return 1

async def generator_a():
    yield 1

if __name__ == '__main__':
   #loop = asyncio.get_event_loop()
   #loop.run_until_complete(hello())
   #loop.close()

    print(type(function) is types.FunctionType)
    print(type(generator()) is types.GeneratorType)
    print(type(function_a()) is types.CoroutineType)
    print(type(generator_a()) is types.AsyncGeneratorType)
