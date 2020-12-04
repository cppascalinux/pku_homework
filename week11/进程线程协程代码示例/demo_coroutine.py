import asyncio, time

async def hello(id):
    print('Hello world! %d' % id)
    await asyncio.sleep(1)
    print('Hello again! %d' % id)

t0 = time.time()
loop = asyncio.get_event_loop()
tasks = [hello(1), hello(2)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print(time.time() - t0, " s")