import asyncio, time

async def consumer(q):
    print('consumer starts.')
    while True:
        item = await q.get()        
        if item is None:
            q.task_done() # Indicate that a formerly enqueued task is complete.
            break
        else:
            await asyncio.sleep(1) # take 1s to consume
            print('consume %d' % item)
            q.task_done()            
    print('consumer ends.')

async def producer(q):
    print('producer starts.')
    for i in range(5):        
        await asyncio.sleep(1) # take 1s to produce        
        print('produce %d' % i)
        await q.put(i)        
    await q.put(None)    
    await q.join()  # Block until all items in the queue have been gotten and processed.
    print('producer ends.')
    
q = asyncio.Queue(maxsize=10)
t0 = time.time()
loop = asyncio.get_event_loop()
tasks = [producer(q), consumer(q)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print(time.time() - t0, " s")