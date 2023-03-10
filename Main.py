import random
import time
import numpy as np
from console.utils import cls
import matplotlib.pyplot as plt

def imprint():
    pass

class Params:
    def __init__(self):
        # This acts as a configuration object that holds various settings and parameters for the simulation
        self.minGenomeLength = 2 # Minimum intelligence level for the neural network
        self.maxGenomeLength = 64 # Maximum intelligence level for the neural network
        self.maxAge = 80 # Doesn't do anything
        self.grid_height = 70 # width
        self.grid_width = 20 # height
        self.grid_size = round((self.grid_height * self.grid_width) / ((self.grid_height + self.grid_width) / 2)) # Don't change
        self.speed = 1 # How much creatures move each time 
        self.biodiversityCount = 3 # How many species total
        self.creatureProportion = 3 # How many creatures are created depending on the grid_size
        self.minCreatures = 5 # The minimum value of any population until the simulation resets to the next generation
        self.mutationRate = 2 # How much a creature can mutate while reproducing
        self.mirror = False # Due to the borders of the grid using modulo, mirror prints the grid twice, seamlessly

p = Params()

import random

rst = '\033[0m'
def generate_display():
    # list of uppercase alphabet characters
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # list of ANSI escape sequence colors (roy g biv)
    colors = []
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            colors.append(u"\u001b[38;5;" + code + "m")

    # list to store selected characters and colors
    fselected = []

    # loop to select randok characters and colors
    for i in range(p.biodiversityCount):
        selected_char = random.choice(alphabet)
        alphabet.remove(selected_char)
        selected_color = random.choice(colors)
        colors.remove(selected_color)
        fselected.append(selected_color + selected_char)
    return fselected

class Gene:
    def __init__(self,): # Sink number represents the actions a gene could take
        self.sourceNum = random.randint(0,7)
        self.sinkNum = random.randint(0,13)
    def makeCustomGene(self, source, sink, weight):
        self.sourceNum = source
        self.sinkNum = sink
        self.weight = weight
        
def makeRandomGene():
    return Gene()
    
class Genome:
    def __init__(self):
        self.genes = []

    def add_gene(self, gene):
        self.genes.append(gene)
        
    def mutate(self):
        for i in range(random.randrange(p.mutationRate)): # It loops a random number of times based on mutationRate
            if random.random() <= 0.5:
                mutated_gene = random.randrange(len(self.genes))
                self.genes[mutated_gene].weight = random.uniform(-4.0, 4.0) # It randomly selects a gene in the genes list sets the weight to a random value
        return self
        

def makeRandomGenome(): # Creates a genome, and appends the Gene class to the genome: 'genes' list.
    genome = Genome()
    length = random.randint(p.minGenomeLength, p.maxGenomeLength)
    for _ in range(length):
        genome.add_gene(makeRandomGene())
    return genome

class NeuralNetwork:
    
    def create_network(self):
        # initialize weights and biases
        for i in range(len(self.genome.genes)):
            self.weights.append(random.uniform(-4, 4))
            self.biases.append(random.uniform(-1, 1))
        
        # reshape weights and biases into matrices
        self.weights = np.reshape(self.weights, (len(self.weights), 1))
        self.biases = np.reshape(self.biases, (len(self.biases), 1))

    def predict_feedforward(self, input_data):
        # calculate the dot product of the input data and weights
        self.input_layer = np.dot(self.weights, input_data)
        
        # add the biases to the input layer
        self.input_layer = np.add(self.input_layer, self.biases)
        
        # pass the input layer through a activation function
        self.hidden_layer = np.maximum(0, self.input_layer)
        
        # return the output of the network
        self.output_layer = self.hidden_layer
        return self.output_layer

    def __init__(self, genome):
        self.genome = genome
        self.weights = []
        self.biases = []
        
        self.input_layer = []
        self.hidden_layer = []
        self.output_layer = []
        
        self.create_network()

# Species
class Life:


    # Individual
    class Creature:
            
        # Find the distance from an alien
        def DETECTION_ALIEN_RADIUS(self):
            distances = []

            # Skip if the same species
            for j in range(len(species_list)):
                if j != self.index:

                    # Calculate the the grid size minus the absolute value of the difference between distances divided by the grid size
                    for i in range(len(species_list[j].creature_list)):
                        x = (p.grid_width - abs(self.x - species_list[j].creature_list[i].x)) / p.grid_width
                        y = (p.grid_height - abs(self.y - species_list[j].creature_list[i].y)) / p.grid_height
                        distances.append((x + y)/2)
                    
            # Sort distance values by biggest to smallest (closest to farthest)
            distances.sort(reverse=True)
            
            # Return the largest distance value if other species exist, else return 0
            return distances[0] if len([i for i in range(len(species_list)) if i != self.index]) > 0 else 0


        # Find the distance from family
        def DETECTION_FAMILY_RADIUS(self):
            distances = []
            
            # Calculate the the grid size minus the absolute value of the difference between distances divided by the grid size
            for i,creature in enumerate(species_list[self.index].creature_list):
                if creature != self:
                    x = (p.grid_width - abs(self.x - species_list[self.index].creature_list[i].x)) / p.grid_width
                    y = (p.grid_height - abs(self.y - species_list[self.index].creature_list[i].y)) / p.grid_height
                    distances.append((x + y)/2)
                
            # Sort distance values by biggest to smallest (closest to farthest)
            distances.sort(reverse=True)
            
            # Return the largest distance value if other species exist, else return 0
            return distances[0] if len(species_list[self.index].creature_list) > 0 else 0
        
        def FAMILY_NICHE(self):
            sorted_list = sorted(species_list[self.index].creature_list, key=lambda creature: creature.hunger, reverse=True)
            for creature in sorted_list:
                if abs(self.x - creature.x) <= self.vision and abs(self.y - creature.y) <= self.vision:
                    creature.hunger -= 1
                    self.hunger += 2
                return True

        # Change coordinates randomly
        def MOVE_RANDOM(self):
            self.x = (self.x + random.randint(-self.speed, self.speed))%p.grid_width
            self.y = (self.y + random.randint(-self.speed, self.speed))%p.grid_height
            self.hunger += 1
            self.age += 1 
            
        
        def MOVE_X(self):
            self.x = (self.x + random.randint(-self.speed, self.speed))%p.grid_width
            self.hunger += 1
            self.age += 1 
        
        
        def MOVE_Y(self):
            self.y = (self.y + random.randint(-self.speed, self.speed))%p.grid_height
            self.hunger += 1
            self.age += 1 



        # Changes a single coordinate to the modulo of the grid
        def MOVE_EAST(self):
            self.x = (self.x + self.speed)%p.grid_width
            self.hunger += 1
            self.age += 1
            
        
        def MOVE_WEST(self):
            self.x = (self.x - self.speed)%p.grid_width
            self.hunger += 1
            self.age += 1
            

        def MOVE_NORTH(self):
            self.y = (self.y + self.speed)%p.grid_height
            self.hunger += 1
            self.age += 1
            
        
        def MOVE_SOUTH(self):    
            self.y = (self.y - self.speed)%p.grid_height
            self.hunger += 1
            self.age += 1

        # Duplicates and mutates an offspring if the following requirements are met
        def REPRODUCE(self):
            if self.hunger < 10 and self.age > 8 and self.health > 0:
                species_list[self.index].creature_list.append(
                    species_list[self.index].Creature(
                        (self.x + random.randint(-1, 1))%p.grid_width, 
                        (self.y + random.randint(-1, 1))%p.grid_height, 
                        self.speed, self.vision,
                        self.genome.mutate(), 
                        self.direction, 
                        self.enemy_index
                    )
                )


        # This is how the creatures eat and get food
        def KILL_FORWARD(self):
            for i in range(len(species_list[self.enemy_index].creature_list)):
                if abs(self.x - species_list[self.enemy_index].creature_list[i].x) <= self.vision and abs(self.y - species_list[self.enemy_index].creature_list[i].y) <= self.vision:
                    grid[species_list[self.enemy_index].creature_list[i].x][species_list[self.enemy_index].creature_list[i].y] = " "
                    species_list[self.enemy_index].creature_list.pop(i)
                    self.hunger = 0
                    self.foodHighscore += 1
                    self.health += 5
                    if self.health > 100: self.health = 100
                    return True
            return False



        #  Randomly select an input from 1 to 0
        def RANDOM(self):
            return random.random()



        # Make an input depending on how extinct their food is
        def ECO_NICHE(self):
            try:
                return (p.grid_size/5) / len(species_list[self.enemy_index].creature_list) 
            except ZeroDivisionError: 
                return 0



        # If their last moves are the same as their direction
        def LAST_MOVE_NORTH(self):
            return 1 if self.orientation[self.last_dir] == "NORTH" else 0
            
        def LAST_MOVE_EAST(self):
            return 1 if self.orientation[self.last_dir] == "EAST" else 0
            
        def LAST_MOVE_SOUTH(self):
            return 1 if self.orientation[self.last_dir] == "SOUTH" else 0
            
        def LAST_MOVE_WEST(self):
            return 1 if self.orientation[self.last_dir] == "WEST" else 0



        # Rotate directions
        def ROTATE_RIGHT(self):
            if self.direction + 1 > 3:
                self.direction = 0
            else:    
                self.direction += 1


        def ROTATE_LEFT(self):
            if self.direction - 1 < 0:
                self.direction = 3
            else:
                self.direction -= 1



        # Move depending on the direction
        def MOVE_FORWARD(self):
            if self.orientation[self.direction] == "NORTH":
                self.y = (self.y + self.speed)%p.grid_height

            elif self.orientation[self.direction] == "EAST":
                self.x = (self.x + self.speed)%p.grid_width
            
            elif self.orientation[self.direction] == "WEST":
                self.x = (self.x - self.speed)%p.grid_width

            elif self.orientation[self.direction] == "SOUTH":
                self.y = (self.y - self.speed)%p.grid_height
                
            self.hunger += 1
            self.age += 1
            self.last_dir = self.direction

        def MOVE_REVERSE(self):
            if self.orientation[self.direction] == "NORTH":
                self.y = (self.y - self.speed)%p.grid_height
                self.hunger += 1
                self.age += 1
                self.last_dir = (self.direction + 2) % 4

            elif self.orientation[self.direction] == "EAST":
                self.x = (self.x - self.speed)%p.grid_width
                self.hunger += 1
                self.age += 1
                self.last_dir = (self.direction + 2) % 4
            
            elif self.orientation[self.direction] == "WEST":
                self.x = (self.x + self.speed)%p.grid_width
                self.hunger += 1
                self.age += 1
                self.last_dir = (self.direction + 2) % 4

            elif self.orientation[self.direction] == "SOUTH":
                self.y = (self.y + self.speed)%p.grid_height
                self.hunger += 1
                self.age += 1
                self.last_dir = (self.direction + 2) % 4

        def MOVE_LEFT(self):
            if self.orientation[self.direction] == "NORTH":
                self.x = (self.x - self.speed)%p.grid_width

            elif self.orientation[self.direction] == "EAST":
                self.y = (self.y + self.speed)%p.grid_height
            
            elif self.orientation[self.direction] == "WEST":
                self.y = (self.y - self.speed)%p.grid_height

            elif self.orientation[self.direction] == "SOUTH":
                self.x = (self.x + self.speed)%p.grid_width
            
            self.hunger += 1
            self.age += 1
            self.last_dir = (self.direction - 1) % 4


        def MOVE_RIGHT(self):
            if self.orientation[self.direction] == "NORTH":
                self.x = (self.x + self.speed)%p.grid_width

            elif self.orientation[self.direction] == "EAST":
                self.y = (self.y - self.speed)%p.grid_height
            
            elif self.orientation[self.direction] == "WEST":
                self.y = (self.y + self.speed)%p.grid_height

            elif self.orientation[self.direction] == "SOUTH":
                self.x = (self.x - self.speed)%p.grid_width
            
            self.hunger += 1
            self.age += 1
            self.last_dir = (self.direction + 1) % 4


        def MOVE_LEFTandRIGHT(self):
            
            direction = random.randint(-self.speed, self.speed)
            
            if self.orientation[self.direction] == "NORTH" or self.orientation[self.direction] == "SOUTH":
                self.x = (self.x + direction)%p.grid_width
                self.hunger += 1
                self.age += 1
                self.last_dir = 3 if direction < 0 else 1
                
            elif self.orientation[self.direction] == "EAST" or self.orientation[self.direction] == "WEST":
                self.y = (self.y + direction)%p.grid_height
                self.hunger += 1
                self.age += 1
                self.last_dir = 2 if direction < 0 else 0


        # Initialize the creature:
        def __init__(self, x: int, y: int, speed: int, vision: int, genome: Genome, direction: int, enemy_index: int):
            self.x = x
            self.y = y
            self.speed = speed
            self.vision = vision
            self.hunger = 1
            self.age = 0
            self.health = 100
            self.genome = genome
            self.last_dir = direction
            self.direction = direction
            self.orientation = ["NORTH", "EAST", "SOUTH", "WEST"]
            self.enemy_index = enemy_index
            self.index = (self.enemy_index) - 1
            self.display = selected[self.index]
            self.foodHighscore = 0
            
            # Initialize the neural network with the weights and biases from the genome
            self.neural_network = NeuralNetwork(self.genome)

            self.Sensors = [
                self.DETECTION_ALIEN_RADIUS,
                self.DETECTION_FAMILY_RADIUS,
                self.RANDOM,
                self.ECO_NICHE,
                self.LAST_MOVE_NORTH,
                self.LAST_MOVE_EAST,
                self.LAST_MOVE_SOUTH,
                self.LAST_MOVE_WEST,
            ]
            
            self.Actions = [
                self.FAMILY_NICHE,
                self.MOVE_RANDOM,
                self.MOVE_EAST,
                self.MOVE_WEST,
                self.MOVE_NORTH,
                self.MOVE_SOUTH,
                self.KILL_FORWARD,
                self.MOVE_FORWARD,
                self.ROTATE_LEFT,
                self.ROTATE_RIGHT,
                self.MOVE_REVERSE,
                self.MOVE_LEFT,
                self.MOVE_RIGHT,
                self.MOVE_LEFTandRIGHT,
            ]            


        # Use the functions and environment to decide what to do
        def executeActions(self):
            def possible_actions(self) -> list: # Create a list of possible actions a single creature can take depending on the sinkNums in their genome.
                Actions_list = []
                for gene in self.genome.genes:
                    Actions_list.append(self.Actions[gene.sinkNum])
                return Actions_list
            a = possible_actions(self)

            # Get the input values from the sensors
            input_data = [[self.DETECTION_ALIEN_RADIUS(), self.DETECTION_FAMILY_RADIUS(), self.RANDOM(), self.ECO_NICHE(), self.LAST_MOVE_NORTH(), self.LAST_MOVE_EAST(), self.LAST_MOVE_SOUTH(), self.LAST_MOVE_WEST()]*len(self.genome.genes)]

            # Pass the input values through the neural network to get the output values
            outputs = self.neural_network.predict_feedforward(input_data).argmax(axis=1)

            # Calculate the probabilities using the softmax function
            probabilities = np.exp(outputs) / np.sum(np.exp(outputs))

            # Choose an action based on the highest probabilities
            action_index = np.random.choice(range(len(a)), p=probabilities)

            # Perform the selected action
            a[action_index]()
            self.REPRODUCE()



    def findIndex(self):
        for i in range(len(species_list)):
            if species_list[i] == self:
                return i


    def __init__(self):
        self.creature_list = []
        self.values = []


    def create_population(self, size):
        self.creature_list = [
            self.Creature(
                random.randint(0, p.grid_width), 
                random.randint(0, p.grid_height), 
                p.speed, 
                0, 
                best_creatures[self.findIndex()].genome.mutate() if best_creatures != 0 else makeRandomGenome(), 
                random.randrange(4), 
                self.findIndex() - 1) 
            for i in range(size)
        ]

def fitness_function():
    foodHighscores = []
    bestCreatures = []
    for i,species in enumerate(species_list):
        bestCreatures.append(0)
        foodHighscores.append(-1)
        for creature in species_list[i].creature_list:
            if creature.foodHighscore > foodHighscores[i]: bestCreatures[i], foodHighscores[i] = creature, creature.foodHighscore
    return bestCreatures


def go(lists):
    # Move and eat for creatures
    j = 0
    # Iterates a while loop for every creature in the simulation
    while j < len(lists):
        grid[lists[j].x][lists[j].y] = ' '
        lists[j].executeActions()
        # Repeats the loop if a creature dies so the index (j) doesn't go out of range
        if lists[j].hunger >= 30 or lists[j].age > p.maxAge+random.randint(0,20) or lists[j].health < 0:
            lists.pop(j)
        else:
            #put the prey on the grid
            if lists[j].age > (p.maxAge / 4.44444444444):
                grid[lists[j].x][lists[j].y] = lists[j].display
                
            else:
                grid[lists[j].x][lists[j].y] = str.lower(lists[j].display)
            j += 1


def popu(species):
    return sum(list(map(lambda x: len(x.creature_list), species)))


# Functions for every 'frame' in the simulation
def simulate():
    
    # Activate each species in the species list and clear the previous grid
    for species in species_list:
        go(species.creature_list)
    cls() # Clears screen

    # Create the population variable and print the total populations of each species
    population = 0
    for i,species in enumerate(species_list):
        print(f"{selected[i]}: {len(species.creature_list)}")

    # Print outputs for better understanding]
    print(f"{rst}Population: {popu(species_list)}")
    print(f"Current gen: {gen}")
    print(f"Current sim: {simulationLength}")
    print(f"Longest sim: {simulationLengthHighest}")
    
    # Use mirrored mode if enabled
    if p.mirror == True:
        for row in grid:
            print(*row, sep =' ', end=" ", flush=True)
            print(*row, sep =' ', end=" ", flush=True)
            print()
        return

    # Print grid values
    for row in reversed(grid): print(*row, sep=" ", flush=True)


# Define game variables
simulationLengthHighest = 0
best_creatures = 0
selected = generate_display()
gen = 0

# Permanent simulation loop
while True:

    # Define generational variables
    grid_sp = 1
    grid = [[' ' for _ in range(p.grid_height+2)] for _ in range(p.grid_width+2)]
    simulationLength = 0
    species_list = []
    length = []
    gen += 1
    
    # Create a species and population for each 
    for i in range(p.biodiversityCount):
        species_list.append(Life())
        species_list[i].create_population(round(p.grid_size/(p.biodiversityCount / p.creatureProportion)))
    
    # Simulation loop for every frame
    breakloop = False
    while True:
        
        # Detect when to reset and go to the next generation
        for species in species_list:
            if len(species.creature_list) < p.minCreatures:
                best_creatures = fitness_function()
                print("Fail!")
                breakloop = True
        if breakloop: break

        # Simulate a frame and increase the simulationLength/time for the pyplot
        simulate()
        simulationLength += 1
        length.append(simulationLength)
        for species in species_list:
            species.values.append(len(species.creature_list))
            plt.plot(length,species.values)
        plt.draw()
        plt.pause(0.01)
        plt.clf()
        if simulationLength > simulationLengthHighest: simulationLengthHighest = simulationLength
        time.sleep(0.03) # Allows the user to see the simulation images 1 by 1
