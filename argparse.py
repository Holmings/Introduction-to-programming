import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("a")
parser.add_argument("b")
args = parser.parse_args()
lista=[]
i=0
args.b = int(args.b)
random.seed(args.a, version=2)
for i in range (0,args.b):
    lista.append(random.randint(0,10000))
print(lista)
