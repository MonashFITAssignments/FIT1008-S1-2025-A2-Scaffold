from unittest import TestCase

from ed_utils.decorators import number, visibility
from enums import PlayerPosition
from player import Player


class TestTask3(TestCase):

    def setUp(self) -> None:
        self.sample_players = [
            Player("Alexey", PlayerPosition.STRIKER, 21),
            Player("Maria", PlayerPosition.MIDFIELDER, 21),
            Player("Brendon", PlayerPosition.DEFENDER, 21),
            Player("Saksham", PlayerPosition.GOALKEEPER, 23),
        ]

        self.sample_stats = [
            "WEIGHT",
            "HEIGHT",
            "GOALS",
            "ASSISTS",
            "TACKLES",
            "INTERCEPTIONS",
            "SAVES",
        ]

    @number("3.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_player_init(self) -> None:
        """
        Basic test to see if the player's init has been set up correctly.
        """
        alexey = self.sample_players[0]

        self.assertEqual(alexey.name, "Alexey")
        self.assertEqual(alexey.position, PlayerPosition.STRIKER)
        self.assertEqual(alexey.get_age(), 21)


    @number("3.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_player_stat_retrieval(self) -> None:
        """
        Testing the stat rettrieval of the player.
        This functionality should be implemented using the `__getitem__` method.
        """
        sample_player = self.sample_players[0]

        # Set some stats
        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val
        
        # Retrieve the stats
        for val, player_stat in enumerate(self.sample_stats):
            self.assertEqual(sample_player[player_stat], val, f"Stat {player_stat} not set to the requested value")

    @number("3.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_player_stat_update(self) -> None:
        """
        Ensure you pass the previous task first before attempting this test.
        This functionality should be implemented using the `__setitem__` method.
        """
        sample_player = self.sample_players[0]

        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val
        
        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val + 1
            self.assertEqual(
                sample_player[player_stat],
                val + 1,
                f"Stat {player_stat} not updated correctly: expected {val + 1} got {sample_player[player_stat]}"
            )

    @number("3.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_player_stat_reset(self) -> None:
        """
        Ensure you pass the previous task first before attempting this test.
        """
        sample_player = self.sample_players[0]

        for val, player_stat in enumerate(self.sample_stats):
            sample_player[player_stat] = val

        sample_player.reset_stats()

        for val, player_stat in enumerate(self.sample_stats):
            self.assertEqual(sample_player[player_stat], 0, f"Stat {player_stat} not reset to 0 after `reset_stats` method called.")
