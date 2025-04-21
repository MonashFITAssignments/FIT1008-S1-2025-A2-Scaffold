from unittest import TestCase

import ast
import inspect

from data_structures.referential_array import ArrayR
from tests.helper import take_out_from_adt, CollectionsFinder
from enums import PlayerPosition
from player import Player
from team import Team
from enums import TeamGameResult


class TestTask4Setup(TestCase):
    def setUp(self):
        self.init_players_data = [
            ("Alexey", PlayerPosition.STRIKER, 18),
            ("Maria", PlayerPosition.MIDFIELDER, 31),
            ("Brendon", PlayerPosition.DEFENDER, 21),
            ("Saksham", PlayerPosition.GOALKEEPER, 23),
        ]
        self.init_players = [
            Player(name, position, age) for name, position, age in self.init_players_data
        ]
        
        self.extra_players_data = [
            ("Crystal", PlayerPosition.GOALKEEPER, 24),
            ("Sophie", PlayerPosition.DEFENDER, 20),
            ("John", PlayerPosition.MIDFIELDER, 27),
            ("Bobby", PlayerPosition.STRIKER, 30),
        ]
        self.extra_players = [
            Player(name, position, age) for name, position, age in self.extra_players_data
        ]

        self.sample_history_length = 10
        self.sample_team = Team("Sample Team", ArrayR.from_list(self.init_players), self.sample_history_length)


class TestTask4(TestTask4Setup):

    def test_team_init_basic(self):
        """
        #name(Test attributes are set correctly)
        """
        self.assertEqual(self.sample_team.name, "Sample Team", "The team name is incorrect.")
        self.assertEqual(self.sample_team.points, 0, "The team points should be 0 initially.")
        try:
            self.sample_team.players
        except AttributeError:
            self.fail("The players attribute should be set on the team at initialisation.")
        
        self.assertEqual(self.sample_team.get_history(), None, "The team history should be None initially.")

    def test_teams_len_method(self):
        """
        #name(Test the len method)
        """
        self.assertEqual(
            len(self.sample_team), len(self.init_players),
            f"The team should have {len(self.init_players)} players"
        )
        
        self.sample_team.add_player(self.extra_players[0])
        self.assertEqual(
            len(self.sample_team), len(self.init_players) + 1, 
            f"The team should have {len(self.init_players) + 1} players"
        )
        
        self.sample_team.add_player(self.extra_players[1])
        self.assertEqual(
            len(self.sample_team), len(self.init_players) + 2,
            f"The team should have {len(self.init_players) + 2} players"
        )
    
    def test_teams_results_history(self):
        """
        #name(Test the team results history)
        """
        self.assertIsNone(self.sample_team.get_history(), "The team should have an empty history initially.")

        # Add results
        self.sample_team.add_result(TeamGameResult.WIN)    
            
        # Check if the history len is correct
        history = take_out_from_adt(self.sample_team.get_history())
        self.assertEqual(len(history), min(1, self.sample_history_length), "Incorrect number of results in history.")
        
        # Add a second result
        self.sample_team.add_result(TeamGameResult.DRAW)
        
        # Check the history len and order is correct
        history = take_out_from_adt(self.sample_team.get_history())
        self.assertEqual(len(history), min(2, self.sample_history_length), "Incorrect number of results in history.")
        self.assertEqual(history[0], TeamGameResult.WIN, "Incorrect result in history.")
        self.assertEqual(history[1], TeamGameResult.DRAW, "Incorrect result in history.")
    
    def test_teams_results_points(self):
        """
        #name(Test the team results points)
        """
        expected_points = 0
        self.assertEqual(self.sample_team.points, expected_points, f"The team should have {expected_points} points initially.")

        # Add results
        self.sample_team.add_result(TeamGameResult.WIN)
        expected_points += TeamGameResult.WIN.value
        self.assertEqual(self.sample_team.points, expected_points, f"The team should have {expected_points} points after winning.")
        
        self.sample_team.add_result(TeamGameResult.DRAW)
        expected_points += TeamGameResult.DRAW.value
        self.assertEqual(
            self.sample_team.points,
            expected_points,
            f"The team should have {expected_points} points after drawing."
        )
        
        self.sample_team.add_result(TeamGameResult.LOSS)
        expected_points += TeamGameResult.LOSS.value
        self.assertEqual(self.sample_team.points, expected_points, f"The team should have {expected_points} points after losing.")

    def _check_get_players_on_all_positions(self, expected_players):
        for query_position in PlayerPosition:
            team_players = self.sample_team.get_players(query_position)
            self.assertFalse(isinstance(team_players, list), "Using built in list objects.")

            expected_players_in_position = list(filter(lambda x: x.position == query_position, expected_players))

            self.assertIsNotNone(
                team_players, 
                f"None player was returned for get_players({query_position.name}) "
                "This is incorrect as there is a player in the team with the wanted position."
            )
            
            self.assertEqual(
                len(team_players), len(expected_players_in_position),
                f"Incorrect number of players returned for {query_position.name}."
            )

            # Make sure all matching players are returned, in the correct order
            team_players = take_out_from_adt(team_players)

            for i in range(len(team_players)):
                self.assertTrue(isinstance(team_players[i], Player), "The returned player should be of type Player")
                self.assertEqual(
                    team_players[i].position, query_position,
                    f"Incorrect player position, expected {query_position.name} got {team_players[i].position.name}"
                )
                self.assertEqual(
                team_players[i].name, expected_players_in_position[i].name,
                "Incorrect player returned for Striker"
            )
    
    def _check_get_players_without_position(self, expected_players):

        # Reorder expected players to match the positions order
        orders = [PlayerPosition.GOALKEEPER, PlayerPosition.DEFENDER, PlayerPosition.MIDFIELDER, PlayerPosition.STRIKER]
        expected_players = list(sorted(expected_players, key=lambda x: orders.index(x.position)))

        team_players = self.sample_team.get_players()
        self.assertFalse(isinstance(team_players, list), "Using built in list objects.")

        self.assertIsNotNone(
            team_players, 
            "None player was returned for get_players()"
        )
        
        self.assertEqual(
            len(team_players), len(expected_players),
            "Incorrect number of players returned for get_players()"
        )

        # Make sure all matching players are returned, in the correct order
        team_players = take_out_from_adt(team_players)

        for i in range(len(team_players)):
            self.assertTrue(isinstance(team_players[i], Player), "The returned player should be of type Player")
            self.assertEqual(
                team_players[i].name, expected_players[i].name,
                "Incorrect order of players returned for get_players()"
            )

    def test_team_players(self):
        """
        #name(Test get_players with initial players)
        """
        self._check_get_players_without_position(self.init_players)
        self._check_get_players_on_all_positions(self.init_players)
 
    def test_teams_players_remove(self):
        """
        #name(Test removing a player)
        """
        self._check_get_players_without_position(self.init_players)
        self._check_get_players_on_all_positions(self.init_players)
        
        # Remove a player
        self.sample_team.remove_player(self.init_players[0])
        
        # Check if the players are still correct
        self._check_get_players_without_position(self.init_players[1:])
            
    def test_call_post_update(self):
        """
        #name(Test calling the make_post method)
        """
        try:
            self.sample_team.make_post("2025/10/01", "Hello World")
        except Exception as e:
            self.fail(f"Team make_post() raised an exception: {e}")


class TestTask4Approach(TestTask4Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import team
        modules = [team]
        
        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                self.fail(failure[3])
