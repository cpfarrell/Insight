import os
import subprocess
import redis
import ast
import sys
import time

class RedisDatabase:
    def __init__(self):
        processes = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE).communicate()[0].split('\n')

        daemon_running = False
        for process in processes:
            terms = process.split()

            if len(terms) >= 5:
                if 'redis-server' in terms[4]:
                    daemon_running = True

        if not daemon_running:
            print 'DEBUG1'
            path = '/Users/chrisfarrell/Work/redis-2.6.14/src/'
            os.system(path + 'redis-server ' + path + 'redis.conf &')
            print 'DEBUG2'
            time.sleep(10)
            print 'DEBUG3'

        self.database = redis.StrictRedis(host='localhost', port=6379, db=6)

    def add_key(self, key):
        self.database.set(key, "{}")

    #Update key information. Creates key in database if not already stored.
    def add_info(self, key, key_info):
        #Add key if not previously exists
        if not self.database.exists(key):
            self.add_key(key)

        #Get info casting as dict
        info = ast.literal_eval(self.database.get(key))
        info.update(key_info)
        self.database.set(key, info)
        
    #Get key info stored in databse
    def get_info(self, key):
        return ast.literal_eval(self.database.get(key))

    def key_known(self, key):
        return self.database.exists(key)

    def add_to_group(self, group, key):
        self.database.sadd(group, key)

    def get_members(self, group):
        return self.database.smembers(group)

    def is_member(self, group, key):
        return self.database.sismember(group, key)

    def remove_member(self, group, key):
        return self.database.srem(group, key)

    def num_members(self, group):
        return self.database.scard(group)

    def random_member(self, group):
        return self.database.srandmember(group)
