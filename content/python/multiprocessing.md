Title: multiprocessing with map
Slug: multiprocessing_map
Category: Python
Author: twmht

[參考](https://medium.com/building-things-on-the-internet/parallelism-in-one-line-40e9b2b36148)

一般來說，會利用 Producer/Consumer 來處理 Multithread。

    :::python
    '''
    Standard Producer/Consumer Threading Pattern
    '''
     
    import time 
    import threading 
    import Queue 
     
    class Consumer(threading.Thread): 
        def __init__(self, queue): 
            threading.Thread.__init__(self)
            self._queue = queue 
     
        def run(self):
            while True: 
                # queue.get() blocks the current thread until 
                # an item is retrieved. 
                msg = self._queue.get() 
                # Checks if the current message is 
                # the "Poison Pill"
                if isinstance(msg, str) and msg == 'quit':
                    # if so, exists the loop
                    break
                # "Processes" (or in our case, prints) the queue item   
                print "I'm a thread, and I received %s!!" % msg
            # Always be friendly! 
            print 'Bye byes!'
     
    def Producer():
        # Queue is used to share items between
        # the threads.
        queue = Queue.Queue()
     
        # Create an instance of the worker
        worker = Consumer(queue)
        # start calls the internal run() method to 
        # kick off the thread
        worker.start() 
     
        # variable to keep track of when we started
        start_time = time.time() 
        # While under 5 seconds.. 
        while time.time() - start_time < 5: 
            # "Produce" a piece of work and stick it in 
            # the queue for the Consumer to process
            queue.put('something at %s' % time.time())
            # Sleep a bit just to avoid an absurd number of messages
            time.sleep(1)
     
        # This the "poison pill" method of killing a thread. 
        queue.put('quit')
        # wait for the thread to close down
        worker.join()
     
    if __name__ == '__main__':
        Producer()

以上的 worker 只有一個。

以下是多個 worker 的例子，需要建立一個 worker pool。

    :::python
    '''
    A more realistic thread pool example 
    '''
    import time 
    import threading 
    import Queue 
    import urllib2 
     
    class Consumer(threading.Thread): 
        def __init__(self, queue): 
            threading.Thread.__init__(self)
            self._queue = queue 
     
        def run(self):
            while True: 
                content = self._queue.get() 
                if isinstance(content, str) and content == 'quit':
                    break
                response = urllib2.urlopen(content)
            print 'Bye byes!'
     
    def Producer():
        urls = [
            'http://www.python.org', 'http://www.yahoo.com'
            'http://www.scala.org', 'http://www.google.com'
            # etc.. 
        ]
        queue = Queue.Queue()
        worker_threads = build_worker_pool(queue, 4)
        start_time = time.time()
     
        # Add the urls to process
        for url in urls: 
            queue.put(url)  
        # Add the poison pillv
        for worker in worker_threads:
            queue.put('quit')
        for worker in worker_threads:
            worker.join()
     
        print 'Done! Time taken: {}'.format(time.time() - start_time)
     
    def build_worker_pool(queue, size):
        workers = []
        for _ in range(size):
            worker = Consumer(queue)
            worker.start() 
            workers.append(worker)
        return workers
     
    if __name__ == '__main__':
        Producer()

但這不是最好的方法。而又因為 GIL 的限制，不論多少個 thread，只能佔用一個 CPU 的 core。

使用 multiprocessing 加上 map。

    :::python
    import urllib2 
    from multiprocessing.dummy import Pool as ThreadPool 
     
    urls = [
        'http://www.python.org', 
        'http://www.python.org/about/',
        'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
        'http://www.python.org/doc/',
        'http://www.python.org/download/',
        'http://www.python.org/getit/',
        'http://www.python.org/community/',
        'https://wiki.python.org/moin/',
        'http://planet.python.org/',
        'https://wiki.python.org/moin/LocalUserGroups',
        'http://www.python.org/psf/',
        'http://docs.python.org/devguide/',
        'http://www.python.org/community/awards/'
        # etc.. 
        ]
     
    # Make the Pool of workers
    pool = ThreadPool(4) 
    # Open the urls in their own threads
    # and return the results
    results = pool.map(urllib2.urlopen, urls)
    #close the pool and wait for the work to finish 
    pool.close() 
    pool.join()


處理大量圖片的例子。

    :::python
    import os 
    import PIL 
     
    from multiprocessing import Pool 
    from PIL import Image
     
    SIZE = (75,75)
    SAVE_DIRECTORY = 'thumbs'
     
    def get_image_paths(folder):
        return (os.path.join(folder, f) 
                for f in os.listdir(folder) 
                if 'jpeg' in f)
     
    def create_thumbnail(filename): 
        im = Image.open(filename)
        im.thumbnail(SIZE, Image.ANTIALIAS)
        base, fname = os.path.split(filename) 
        save_path = os.path.join(base, SAVE_DIRECTORY, fname)
        im.save(save_path)
     
    if __name__ == '__main__':
        folder = os.path.abspath(
            '11_18_2013_R000_IQM_Big_Sur_Mon__e10d1958e7b766c3e840')
        os.mkdir(os.path.join(folder, SAVE_DIRECTORY))
     
        images = get_image_paths(folder)
     
        pool = Pool()
        pool.map(create_thumbnail,images)
        pool.close()
        pool.join()
