import copy
import json

from player import Player
import numpy as np
import math


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.generation_number = 0

    def mutation(self , chromosome):
        mutate_probability = 0.5

        random_number = np.random.uniform(0, 1, 1)
        if(random_number <= mutate_probability) :

            chromosome.nn.w1 += np.random.normal(0,0.3,size=chromosome.nn.w1.shape)
            chromosome.nn.w2 += np.random.normal(0,0.3,size=chromosome.nn.w2.shape)

            chromosome.nn.b1 += np.random.normal(0, 0.3, size=chromosome.nn.b1.shape)
            chromosome.nn.b2 += np.random.normal(0, 0.3, size=chromosome.nn.b2.shape)

        return chromosome

    def crossover(self , array1 , array2):
        crossover_probability = 0.8
        crossover_place = math.floor(array1.shape[0]/2)

        random_number = np.random.uniform(0, 1, 1)
        if(random_number > crossover_probability) :
            return array1 , array2

        else:
            child1_array = np.concatenate((array1[:crossover_place], array2[crossover_place:]), axis=0)
            child2_array = np.concatenate((array2[:crossover_place], array1[crossover_place:]), axis=0)
        return child1_array , child2_array

    def q_tournament(self , num_players , players ,q ):
        selected_players = []
        for i in range(num_players) :
             random_selections = np.random.choice(players, q)
             selected_players.append(max(random_selections, key=lambda player: player.fitness))

        return selected_players

    def roulette_wheel(self , players , num_player):
        fitness_sum = sum([player.fitness for player in players])
        probabilities = [player.fitness / fitness_sum for player in players]
        nex_generation = np.random.choice(players, size=num_player, p=probabilities, replace=False)
        return nex_generation.tolist()




    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        players.sort(key=lambda x: x.fitness, reverse=True)
        fitness_list = [player.fitness for player in players]
        best_fitness = float(np.max(fitness_list))
        average_fitness = float(np.mean(fitness_list))
        worst_fitness = float(np.min(fitness_list))
        # best_fitness = players[0].fitness
        # worst_fitness = players[len(players)-1].fitness
        # average_fitness = 0
        # for p in players :
        #     average_fitness += p.fitness
        # average_fitness = average_fitness/len(players)
        self.save_fitness_results(best_fitness , worst_fitness , average_fitness)

        return players[: num_players]

        # q_tournament
        # players = self.q_tournament(num_players , players , 5 )
        # return players


        # TODO (Additional: Implement roulette wheel here)
        # players = self.roulette_wheel(players, num_players)
        # return players
        # TODO (Additional: Implement SUS here)
        # TODO (Additional: Learning curve)

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            new_players = self.q_tournament(num_players , prev_players , 3)
            children = []
            # new_players = prev_players
            for i in range( 0, len(new_players) , 2) :
                parent1 = new_players[i]
                parent2 = new_players[i+1]
                clone_child1 = self.clone_player(parent1)
                clone_child2 = self.clone_player(parent2)
                clone_child1.nn.w1 ,  clone_child2.nn.w1 = self.crossover(parent1.nn.w1 , parent2.nn.w1)
                clone_child1.nn.w2 , clone_child2.nn.w2  = self.crossover(parent1.nn.w2, parent2.nn.w2)
                clone_child1.nn.b1, clone_child2.nn.b1 = self.crossover(parent1.nn.b1, parent2.nn.b1)
                clone_child1.nn.b2, clone_child2.nn.b2 = self.crossover(parent1.nn.b2, parent2.nn.b2)
                clone_child1 = self.mutation(clone_child1)
                clone_child2 = self.mutation(clone_child2)
                children.append(clone_child1)
                children.append(clone_child2)

            # new_players.sort(key=lambda x: x.fitness, reverse=True)
            # new_players = new_players[: num_players]
            return children
    #
    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player


    def save_fitness_results(self , max_fitness , min_fitness , average_fitness):
        if(self.generation_number == 0) :
            generation_results ={
                'best_fitnesses': [max_fitness],
                'worst_fitnesses': [min_fitness],
                'average_fitnesses': [average_fitness]
            }
            with open('generation_results.json', 'w') as file:
                json.dump(generation_results, file)
            file.close()
        else:
            with open('generation_results.json', 'r') as file:
                generation_results = json.load(file)
            file.close()
            generation_results['best_fitnesses'].append(max_fitness)
            generation_results['worst_fitnesses'].append(min_fitness)
            generation_results['average_fitnesses'].append(average_fitness)

            with open('generation_results.json', 'w') as file:
                json.dump(generation_results, file)
            file.close()
        self.generation_number += 1





