import random
import math

class DNA:
    def __init__(self, len):
        self.genes = [chr(math.floor(random.uniform(97, 123))) for i in range(len)]
        self.fitness = 0
    
    def __str__(self):
        return "".join(self.genes)

    def calcFitness(self, target):
        self.fitness = 0
        for i in range(len(self.genes)):
            if self.genes[i] == target[i]:
                self.fitness += 1
                
    def crossover(self, Y):
        XY = DNA(len(self.genes))
        mid = round(len(self.genes))
        for i in range(len(self.genes)):
            if i < mid:
                XY.genes[i] = self.genes[i]
            else:
                XY.genes[i] = Y.genes[i]
        return XY

    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if random.random() < mutationRate:
                self.genes[i] = chr(math.floor(random.uniform(97, 123)))


class Population:
    def __init__(self, target, popMax, mutationRate):
        self.target = target
        self.popMax = popMax
        self.mutationRate = mutationRate
        self.sumFitness = 0
        self.generation = 1
        self.maxFitness = len(target)
        self.best = ""
        self.finished = False
        self.population = []
        self.newPopulation = []

        for _ in range(popMax):
            self.population.append(DNA(len(target)))

    def __str__(self):
        res = ""
        for i in self.population:
            res += str(i) + "\n"
        print(res)

    def calcFitness(self):
        for i in self.population:
            i.calcFitness(self.target)

    def initFitness(self):
        self.sumFitness = 0
        for i in self.population:
            self.sumFitness += i.fitness

    def getWeightedRandom(self):
        rand = round(random.uniform(1, self.sumFitness+1))
        for i in self.population:
            rand -= i.fitness
            if rand < 1:
                return i
        return self.population[-1]

    def updatePopulation(self):
        self.generation += 1
        max = 0
        for i in self.population:
            if i.fitness > max:
                max = i.fitness
                self.best = "".join(i.genes)
        if max == self.maxFitness:
            self.finished = True

    def naturalSelection(self):
        self.initFitness()
        self.newPopulation.clear()
        for _ in range(len(self.population)):
            X, Y = self.getWeightedRandom(), self.getWeightedRandom()
            XY, YX = X.crossover(Y), Y.crossover(X)
            XY.mutate(self.mutationRate), YX.mutate(self.mutationRate)
            self.newPopulation.append(XY if XY.fitness > YX.fitness else YX)
        self.population = [ i for i in self.newPopulation]

def main():
    target = "mynameisharish"
    popMax = 200
    mutationRate = 0.01

    population = Population(target, popMax, mutationRate)
    population.calcFitness()

    while(not(population.finished)):
        population.naturalSelection()
        population.calcFitness()
        population.updatePopulation()
        print(population.generation, " : ", population.best)

main()