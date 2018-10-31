import osbrain
import random
import re
import time

from osbrain import run_agent
from osbrain import run_nameserver
from random import randint
from osbrain import Agent




class alice(Agent):
    def rand(self):
        self.a = random.randint(1, 9)
        while True:
            self.b = random.randint(0, 9)
            if self.a!=self.b :
                break
        while True:
            self.c = random.randint(0, 9)
            if self.c not in [self.a , self.b]:
                break
       
        return  self.a*100+self.b*10+self.c
   
    def verify_V(self, n1,n2):
        V=0   
        nn= [int(i) for i in str(n1)]
        for i in range(3):
                if n2[i] in nn and n2[i] != nn[i]:
	                V=V+1
        return V
    def verify_T(self, n1,n2):
        T=0
        nn= [int(i) for i in str(n1)]
        for i in range(3):
            if nn[i]== n2[i]:
                T=T+1
        return T

    def on_init(self):
        self.bind('REP', alias = 'main', handler = self.reply)
        self.secretNumber = self.rand()
        self.secretlist= [int(i) for i in str(self.secretNumber)]
        
    
    def reply(self, guess):
        T=self.verify_T(guess,self.secretlist)
        V=self.verify_V(guess,self.secretlist)
        if T==3:
            print ('Congrats Bob, it is the right number')
        else:
            print('No Bob, it is not. You have: ',  V,'V , ',T,'T')           
        return V,T
        

class Bob(Agent):
    
    def rand(self):
        self.a = random.randint(1, 9)
        while True:
            self.b = random.randint(0, 9)
            if self.a!=self.b :
                break
        while True:
            self.c = random.randint(0, 9)
            if self.c not in [self.a , self.b]:
                break
       
        return  self.a*100+self.b*10+self.c
    def guess(self):
        while True:
            n =self.rand()
            v=True
            l = [int(i) for i in str(n)]
            for i in l :
                if i in self.lnot :
                    v=False
            if v and n not in self.exist :
                break
        return n


    
    def on_init(self):
        self.lnot=[]
        self.exist=[]
        self.connect(alice.addr('main'), alias='main')
        while True:
            x = self.guess()
            print("alice : is it " + str(x) + " ?")
            self.send('main', x)
            self.v, self.t = self.recv('main')  
            if self.t==3:
                break          
            if self.t==0 and self.v==0:
                self.lnot=self.lnot+[int(i) for i in str(x)]
            self.exist.append(x)
                
if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    alice = run_agent('alice', base=alice)
    print("GUESS THE NUMBER")
    print('----------RULES-------')
    print('pick 3 different numbers in a certain order')
    print('V is the number of the existant digits not in the right place')
    print('T is the number of the digits in the right place')
    print ('----------------')
    time.sleep(5)
    bob = run_agent('Bob', base=Bob)
    ns.shutdown()
