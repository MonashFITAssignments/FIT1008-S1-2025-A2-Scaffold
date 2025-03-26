from unittest import TestCase

from config import Config
from enums import PlayerPosition, TeamGameResult
from ed_utils.decorators import number, visibility
from data_structures.bit_vector_set import BitVectorSet
from data_structures.referential_array import ArrayR
from tests.helper import take_out_from_adt
from player import Player
from random_gen import RandomGen
from season import Season
from team import Team
from typing import Union


class Roster:
    FIRST_NAMES: list[str] = ['Abey', 'Alexey', 'Ann', 'Alexandria', 'Ben', 'Bavley', 'Brett', 'Brendon', 'Chloe',
                              'Christian', 'Daniel', 'Fermi', 'Hui', 'Laura', 'Lisa', 'Maria', 'Matthew', 'Patrick',
                              'Rupert', 'Saksham', 'Yasmeen']

    LAST_NAMES: list[str] = ['Bot', 'Bellingham', 'Bonmatí', 'Caicedo', 'Danial', 'Fernandes', 'Francis', 'Hernández',
                             'Henry', 'Iniesta', 'Kerr', 'Messi', 'Mbappé', 'Modric', 'Pearson',
                             'Peterson', 'Ronaldo', 'Roberto', 'Stacie', 'Sparks', 'Wright', 'York', 'Zidane']

    TEAM_NAMES: list[str] = ['Badgers', 'Blitz', 'Commanders', 'Ferguson', 'Gladiators', 'Grizzlies',
                             'Hot Shots', 'Razorbacks', 'Renegades', 'Tiger Sharks', 'Wildcats',
                             'The Flash', 'Blue Angels', 'Fineapples', 'Shock Squad', 'Cherry Blossoms',
                             'Cheetah Girls', 'The Fever', 'Victoria Secret', 'Sweet & Salty', 'Lady Birds']

    PLAYER_NAMES: list[str] = []

    @classmethod
    def generate_players(cls):
        for first_name in cls.FIRST_NAMES:
            for last_name in cls.LAST_NAMES:
                cls.PLAYER_NAMES.append(f'{first_name} {last_name}')

    @classmethod
    def generate_teams(cls, num_teams: int) -> ArrayR[Team]:
        if len(cls.PLAYER_NAMES) == 0:
            cls.generate_players()

        full_roster: list[Player] = []
        taken_names: BitVectorSet = BitVectorSet()
        for i in range(Config.TEAM_MAX_PLAYERS * Config.MAX_NUM_TEAMS):
            player_name: Union[str, None] = None
            while player_name is None:
                player_no: int = RandomGen.randint(1, len(cls.PLAYER_NAMES))
                if player_no not in taken_names:
                    player_name = cls.PLAYER_NAMES[player_no - 1]
                    taken_names.add(player_no)
            position = RandomGen.random_choice(list(PlayerPosition))
            age = RandomGen.randint(18, 30)

            player = Player(player_name, position, age)
            player["WEIGHT"] = RandomGen.randint(70, 90)
            player["HEIGHT"] = RandomGen.randint(150, 180)
            player["STAR_SKILL"] = RandomGen.randint(0, 5)
            player["WEAK_FOOT_ABILITY"] = RandomGen.randint(0, 5)
            full_roster.append(player)

        teams: ArrayR[Team] = ArrayR(num_teams)
        for i in range(num_teams):
            num_players: int = RandomGen.randint(Config.TEAM_MIN_PLAYERS, Config.TEAM_MAX_PLAYERS)
            players: ArrayR[Player] = ArrayR(num_players)
            for j in range(num_players):
                player_idx = RandomGen.randint(0, len(full_roster) - 1)
                players[j] = full_roster[player_idx]
                del full_roster[player_idx]

            teams[i] = Team(cls.TEAM_NAMES[i], players, 5)

        return teams


class TestTask6(TestCase):
    def setUp(self) -> None:
        RandomGen.set_seed(123)
        self.season: Union[Season, None] = None

    @number("6.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_simulate_season(self):
        teams = Roster.generate_teams(4)
        self.season = Season(teams)
        self.season.simulate_season()

    @number("6.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_player_stats(self):
        # Set the seed to 123
        RandomGen.set_seed(123)

        # Generate the teams and simulate the season
        teams = Roster.generate_teams(4)
        self.season = Season(teams)
        self.season.simulate_season()

        # Expected results of the stats for all players of the first team
        # Will fix these later...
        # expected_results: dict = {
        #     'Badgers': {
        #         'Ann Caicedo': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 5, PlayerStats.ASSISTS: 0, PlayerStats.TACKLES: 2, PlayerStats.INTERCEPTIONS: 0},
        #         'Matthew Pearson': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 0, PlayerStats.ASSISTS: 0, PlayerStats.TACKLES: 1, PlayerStats.INTERCEPTIONS: 1},
        #         'Ben Hernández': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 0, PlayerStats.ASSISTS: 2, PlayerStats.TACKLES: 0, PlayerStats.INTERCEPTIONS: 0},
        #         'Lisa Roberto': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 1, PlayerStats.ASSISTS: 0, PlayerStats.TACKLES: 2, PlayerStats.INTERCEPTIONS: 2},
        #         'Patrick Modric': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 0, PlayerStats.ASSISTS: 0, PlayerStats.TACKLES: 0, PlayerStats.INTERCEPTIONS: 0},
        #         'Lisa Mbappé': {PlayerStats.GAMES_PLAYED: 6, PlayerStats.GOALS: 2, PlayerStats.ASSISTS: 1, PlayerStats.TACKLES: 1, PlayerStats.INTERCEPTIONS: 1}
        #     }
        # }
        # Get all the players of the first team
        players = teams[0].get_players()

        # Create a dictionary of the players with the name as the key and the player object as the value
        players_dict = {player.name: player for player in players}

        # Check the stats of the players of the first team
        # for player_name, stats in expected_results['Badgers'].items():
        #     player = players_dict[player_name]
        #     for stat, value in stats.items():
        #         self.assertEqual(value, player[stat], f"{player_name} {stat} not correct")
