from unittest import TestCase
from unittest import mock

import datetime

import ast
import inspect

from tests.helper import CollectionsFinder

from enums import PlayerPosition

import player
from player import Player


class TestTask3Setup(TestCase):
    def setUp(self):
        self.sample_players_data = [
            ("Alexey", PlayerPosition.STRIKER, 21),
            ("Maria", PlayerPosition.MIDFIELDER, 21),
            ("Brendon", PlayerPosition.DEFENDER, 21),
            ("Saksham", PlayerPosition.GOALKEEPER, 23),
        ]
        self.sample_players = [
            Player(name, position, age) for name, position, age in self.sample_players_data
        ]

        self.sample_stats = [
            "WEIGHT",
            "HEIGHT",
            "ASSISTS",
            "TACKLES",
            "INTERCEPTIONS",
            "SAVES",
        ]


class TestTask3(TestTask3Setup):
    def test_player_init(self):
        """
        #name(Test the player constructor)
        """
        alexey = self.sample_players[0]

        self.assertEqual(alexey.name, self.sample_players_data[0][0])
        self.assertEqual(alexey.position, self.sample_players_data[0][1])
        self.assertEqual(alexey.get_age(), self.sample_players_data[0][2])
        self.assertEqual(alexey.goals, 0)

    def test_player_age(self):
        """
        #name(Test player age calculation)
        """
        move_time_forward_years = 2
        
        alexey = self.sample_players[0]

        mock_datetime_class = mock.MagicMock(wraps=datetime.datetime)
        mock_datetime_class.now = mock.MagicMock(return_value=datetime.datetime(datetime.datetime.now().year + move_time_forward_years, 1, 1))
        mock_datetime_class.today = mock.MagicMock(return_value=datetime.date(datetime.datetime.now().year + move_time_forward_years, 1, 1))

        mock_datetime_module = mock.MagicMock(wraps=datetime)
        mock_datetime_module.date.today = datetime.date(datetime.datetime.now().year + move_time_forward_years, 1, 1)
        mock_datetime_module.datetime = mock_datetime_class

        try:
            with mock.patch(f"{player.__name__}.datetime", mock_datetime_module):
                self.assertEqual(alexey.get_age(), self.sample_players_data[0][2] + move_time_forward_years)
        except AttributeError:
            self.fail("Player.py: do not change the datetime import statement from the scaffold.")
    
    def test_player_stat_retrieval(self):
        """
        #name(Test the stat retrieval of the player)
        """
        sample_player = self.sample_players[0]

        # Set some stats
        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val
        
        # Retrieve the stats
        for val, player_stat in enumerate(self.sample_stats):
            self.assertEqual(sample_player[player_stat], val, f"Stat {player_stat} not set to the requested value")

    def test_player_stat_reset(self):
        """
        #name(Test the stat reset of the player)
        """
        sample_player = self.sample_players[0]

        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val

        sample_player.reset_stats()

        for val, player_stat in enumerate(self.sample_stats):
            self.assertEqual(sample_player[player_stat], 0, f"Stat {player_stat} not reset to 0 after `reset_stats` method called.")


class TestTask3Approach(TestTask3Setup):    
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import player
        modules = [player]
        
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
