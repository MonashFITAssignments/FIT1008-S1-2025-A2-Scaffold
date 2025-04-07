from unittest import TestCase

import ast
import inspect

from data_structures.referential_array import ArrayR
from tests.helper import take_out_from_adt, CollectionsFinder

from enums import PlayerPosition
from player import Player
from random_gen import RandomGen
from season import Season, WeekOfGames, Game
from team import Team


class TestTask5Setup(TestCase):
    def setUp(self):
        RandomGen.set_seed(123)

        first_names = [
            "John", "Jane", "Alice", "Bob", "Charlie", "David",
            "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
            "Mallory", "Niaj", "Olivia", "Peggy", "Robert", "Sybil",
            "Trent", "Uma", "Victor", "Walter", "Xena", "Yara", "Zane"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Jones", "Brown",
            "Davis", "Miller", "Wilson", "Moore", "Taylor",
            "Anderson", "Thomas", "Jackson", "White", "Harris",
            "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
        ]
        team_names = [
            "Tornadoes", "Sharks", "Wolves", "Eagles", "Lions", "Dragons",
            "Panthers", "Bears", "Hawks", "Falcons", "Tigers", "Mustangs",
        ]
        
        # Create random teams
        NUMBER_OF_TEAMS = 6
        NUMBER_OF_PLAYERS_PER_POSITION = 4
        
        self.teams = []
        used_names = set()
        for i in range(NUMBER_OF_TEAMS):
            players = []
            for pos in PlayerPosition:
                for _ in range(NUMBER_OF_PLAYERS_PER_POSITION):
                    player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                    while player_name in used_names:
                        player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                    used_names.add(player_name)
                    player = Player(player_name, pos, RandomGen.randint(18, 40))
                    players.append(player)
            team = Team(team_names[i], ArrayR.from_list(players), RandomGen.randint(5, 15))
            self.teams.append(team)

        self.arbitrary_games = [
            Game(RandomGen.random_choice(self.teams[:len(self.teams) // 2]), RandomGen.random_choice(self.teams[len(self.teams) // 2:]))
            for _ in range(10)
        ]

        self.week_of_games = WeekOfGames(1, ArrayR.from_list(self.arbitrary_games))

        self.season = Season(ArrayR.from_list(self.teams))


class TestTask5(TestTask5Setup):
    def test_week_of_games_iteration(self):
        """
        #name(Test the iteration of WeekOfGames)
        """
        for i, game in enumerate(self.week_of_games):
            self.assertIsInstance(game, Game, "WeekOfGames should iterate over Game objects")
            self.assertEqual(game, self.arbitrary_games[i])

    def test_season_attributes(self):
        """
        #name(Test the attributes of the Season class)
        """
        self.assertTrue(hasattr(self.season, "teams"), "Teams not initialized")
        season_teams = take_out_from_adt(self.season.teams).to_list()
        self.assertEqual(season_teams, self.teams, "Initial teams not setup correctly")
        
        # Leaderboard
        self.assertTrue(hasattr(self.season, "leaderboard"), "Leaderboard not initialized")
        self.assertIsNotNone(self.season.leaderboard, "Leaderboard not initialized")

        # Schedule
        self.assertTrue(hasattr(self.season, "schedule"), "Schedule not initialized")
        self.assertIsNotNone(self.season.schedule, "Schedule not initialized")
        self.assertNotEqual(len(self.season.schedule), 0, "Schedule is empty")
    
    def test_delay_match_basic(self):
        """
        #name(Test the delay match function)
        """
        # Check the function exists
        self.assertTrue(hasattr(self.season, "delay_week_of_games"), "delay_week_of_games function does not exist")
        
        schedule = take_out_from_adt(self.season.schedule).to_list()
        week1, week2 = schedule[0], schedule[1]

        self.season.delay_week_of_games(1, 2)
        new_schedule = take_out_from_adt(self.season.schedule).to_list()
        self.assertEqual(new_schedule[0], week2, "Week 2 should be moved to Week 1")
        self.assertEqual(new_schedule[1], week1, "Week 1 should be moved to Week 2")


class TestTask5Approach(TestTask5Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import season
        modules = [season]
        
        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                self.fail(failure)
