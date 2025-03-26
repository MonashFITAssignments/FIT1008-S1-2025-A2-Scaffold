from unittest import TestCase

from data_structures.referential_array import ArrayR
from ed_utils.decorators import number, visibility
from enums import PlayerPosition
from config import Config
from player import Player
from random_gen import RandomGen
from season import Season
from team import Team


class TestTask5(TestCase):
    FIRST_NAMES: list[str] = ['Abey', 'Alexey', 'Brendon', 'Lisa', 'Maria', 'Rupert', 'Saksham', 'Yasmeen']
    LAST_NAMES: list[str] = ['Bellingham', 'Bonmatí', 'Caicedo', 'Fernandes', 'Kerr', 'Messi', 'Modric', 'Roberto']
    TEAM_NAMES: list[str] = ['Team 1', 'Team 2', 'Team 3', 'Team 4']

    def setUp(self) -> None:
        self.players: list[Player] = []
        for i in range(Config.TEAM_MAX_PLAYERS * Config.MAX_NUM_TEAMS):
            first_name = RandomGen.random_choice(self.FIRST_NAMES)
            last_name = RandomGen.random_choice(self.LAST_NAMES)
            position = RandomGen.random_choice(list(PlayerPosition))
            age = RandomGen.randint(18, 30)
            self.players.append(Player(f"{first_name} {last_name}", position, age))

        self.teams: ArrayR[Team] = ArrayR(len(self.TEAM_NAMES))
        for i in range(len(self.TEAM_NAMES)):
            num_players: int = RandomGen.randint(Config.TEAM_MIN_PLAYERS, Config.TEAM_MAX_PLAYERS)
            players: ArrayR[Player] = ArrayR(num_players)
            for j in range(num_players):
                player_idx = RandomGen.randint(0, len(self.players) - 1)
                players[j] = self.players[player_idx]
                del self.players[player_idx]

            self.teams[i] = Team(self.TEAM_NAMES[i], players, 5)

    @number("5.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_get_teams(self):
        self.season = Season(self.teams)
        self.assertEqual(self.season.teams, self.teams, "Initial teams not setup correctly")

    @number("5.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_season_setup(self):
        self.season = Season(self.teams[0:3])
        # Check if the season is set up correctly
        # Check if the leaderboard is not None
        self.assertIsNotNone(self.season.leaderboard, "Leaderboard not initialized")
        # Check if the schedule is not None
        self.assertIsNotNone(self.season.schedule, "Schedule not initialized")
        # Check if the schedule is not empty
        self.assertNotEqual(len(self.season.schedule), 0, "Schedule is empty")
        expected_matches: list[list[int]] = [[0, 1], [0, 2], [1, 2], [1, 0], [2, 0], [2, 1]]
        match_no: int = 0
        for game in self.season.get_games():
            self.assertEqual(self.teams[expected_matches[match_no][0]].name, game.home_team.name)
            self.assertEqual(self.teams[expected_matches[match_no][1]].name, game.away_team.name)
            match_no += 1

    @number("5.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_delay_match(self):
        self.season = Season(self.teams)

        # Initial schedule with 4 teams
        # W1 Team 1 vs Team 2
        # W1 Team 3 vs Team 4
        # W2 Team 1 vs Team 3
        # W2 Team 2 vs Team 4
        # W3 Team 1 vs Team 4
        # W3 Team 2 vs Team 3
        # W4 Team 2 vs Team 1
        # W4 Team 4 vs Team 3
        # W5 Team 3 vs Team 1
        # W5 Team 4 vs Team 2
        # W6 Team 4 vs Team 1
        # W6 Team 3 vs Team 2

        self.season.delay_week_of_games(2, 4)

        # [[Team 1 vs Team 3], [Team 2 vs Team 4]]
        expected_matches: list[list[int]] = [[0, 2], [1, 3]]
        match_no: int = 0
        for i, week_of_games in enumerate(self.season.schedule):
            for game in week_of_games:
                week_no: int = i + 1
                if week_no == 4:
                    self.assertEqual(self.teams[expected_matches[match_no][0]].name, game.home_team.name)
                    self.assertEqual(self.teams[expected_matches[match_no][1]].name, game.away_team.name)
                    match_no += 1

    @number("5.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_delay_match_till_end(self):
        self.season = Season(self.teams)

        # Initial schedule with 4 teams
        # W1 Team 1 vs Team 2
        # W1 Team 3 vs Team 4
        # W2 Team 1 vs Team 3
        # W2 Team 2 vs Team 4
        # W3 Team 1 vs Team 4
        # W3 Team 2 vs Team 3
        # W4 Team 2 vs Team 1
        # W4 Team 4 vs Team 3
        # W5 Team 3 vs Team 1
        # W5 Team 4 vs Team 2
        # W6 Team 4 vs Team 1
        # W6 Team 3 vs Team 2

        self.season.delay_week_of_games(3)

        # [[Team 1 vs Team 4], [Team 2 vs Team 3]]
        expected_matches: list[list[int]] = [[0, 3], [1, 2]]
        match_no: int = 0
        for i, week_of_games in enumerate(self.season.schedule):
            for game in week_of_games:
                week_no: int = i + 1
                if week_no == 6:
                    self.assertEqual(self.teams[expected_matches[match_no][0]].name, game.home_team.name)
                    self.assertEqual(self.teams[expected_matches[match_no][1]].name, game.away_team.name)
                    match_no += 1


    @number("5.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_leaderboard_setup(self):
        self.season = Season(self.teams)
        # Check if the leaderboard is not empty
        self.assertNotEqual(len(self.season.leaderboard), 0, "Leaderboard should not be empty")

        # Check the order of the leaderboard should be according to the name of the teams
        sorted_teams: ArrayR[Team] = sorted(self.teams, key=lambda team: team.name)
        for i, team in enumerate(self.season.leaderboard):
            self.assertEqual(team.name, sorted_teams[i].name, "Leaderboard not sorted correctly")