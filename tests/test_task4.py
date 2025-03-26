from unittest import TestCase

from data_structures.referential_array import ArrayR
from ed_utils.decorators import number, visibility
from tests.helper import take_out_from_adt
from enums import PlayerPosition
from player import Player
from team import Team


class TestTask4(TestCase):

    def setUp(self) -> None:
        self.sample_players = [
            Player("Alexey", PlayerPosition.STRIKER, 22),
            Player("Maria", PlayerPosition.MIDFIELDER, 22),
            Player("Brendon", PlayerPosition.DEFENDER, 22),
            Player("Saksham", PlayerPosition.GOALKEEPER, 22),
            Player("Rupert", PlayerPosition.GOALKEEPER, 45),
        ]
        self.sample_team = Team("Sample Team", ArrayR.from_list(self.sample_players), 5)

    @number("4.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_team_init_basic(self) -> None:
        self.assertEqual(self.sample_team.name, "Sample Team", "The team name is incorrect")

    @number("4.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_teams_additional_methods(self) -> None:
        # checking __len__ method
        self.assertEqual(len(self.sample_team), 5, "The team should have 5 players")

        self.assertEqual(self.sample_team.name, "Sample Team", "The team name is incorrect")

    @number("4.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_teams_with_player_teams(self) -> None:
        """
        Testing if the team has the correct number of players.
        """

        #### STRIKER ####
        team_player = self.sample_team.get_players(PlayerPosition.STRIKER)
        self.assertIsNotNone(team_player,"None player was returned for get_players('PlayerPosition.STRIKER') This is incorrect as there is a player in the team with the position Striker.")
        self.assertEqual(len(team_player), 1, f"Only one player should be returned for Striker you have returned {len(team_player)}")
        team_player = take_out_from_adt(team_player)
        self.assertEqual(team_player[0].name, "Alexey", "Incorrect player found for Striker")


        #### MIDFIELDER ####
        team_player = self.sample_team.get_players(PlayerPosition.MIDFIELDER)
        self.assertIsNotNone(team_player,"None player was returned for get_players('PlayerPosition.MIDFIELDER') This is incorrect as there is a player in the team with the position Midfielder.")
        self.assertEqual(len(team_player), 1, f"Only one player should be returned for Midfielder you have returned {len(team_player)}")
        team_player = take_out_from_adt(team_player)
        self.assertEqual(team_player[0].name, "Maria", "Incorrect player found for Midfielder")


        #### DEFENDER ####
        team_player = self.sample_team.get_players(PlayerPosition.DEFENDER)
        self.assertIsNotNone(team_player,"None player was returned for get_players('PlayerPosition.DEFENDER') This is incorrect as there is a player in the team with the position Defender.")
        self.assertEqual(len(team_player), 1, f"Only one player should be returned for Defender you have returned {len(team_player)}")
        team_player = take_out_from_adt(team_player)
        self.assertEqual(team_player[0].name, "Brendon", "Incorrect player found for Defender")


    @number("4.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_teams_with_player_teams_2(self) -> None:
        """
        Testing if the team has the correct number of players.
        """

        # Get the GOALKEEPER (should return two players)
        team_players = self.sample_team.get_players(PlayerPosition.GOALKEEPER)
        self.assertIsNotNone(team_players, "No player was returned for team > get_players> 'PlayerPosition.GOALKEEPER'")
        self.assertEqual(len(team_players), 2,
                         f"Two players should be returned for Goalkeeper you have returned {len(team_players)}")
        team_players = take_out_from_adt(team_players)

        """
        Note the ordering matters
        Saksham is the first goalkeeper to be added
        then Rupert is the second goalkeeper to be added
        """
        expected_names = ["Saksham", "Rupert"]
        for idx, player in enumerate(team_players):
            self.assertEqual(player.position, PlayerPosition.GOALKEEPER,
                             f"Incorrect player position, expected {PlayerPosition.GOALKEEPER} got {player.position}")
            self.assertEqual(player.name, expected_names[idx],
                             f"Expected player {expected_names[idx]} got {player.name}.")

    @number("4.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_adding_players_to_teams(self) -> None:
        """
        Testing if the players are added to the team correctly.
        """
        sample_team = self.sample_team
        sample_players = self.sample_players
        for player in self.sample_players:
            self.assertIn(player, sample_team.get_players(), f"Player {player.name} not found in the team")

        # remove the players from the team
        for i, player in enumerate(self.sample_players):
            player_position = player.position
            sample_team.remove_player(player)
            # Check if they were removed
            if player_position is not PlayerPosition.GOALKEEPER:
                self.assertEqual(len(sample_team.get_players(player_position)), 0, f"Player {player.name} not removed from the team")
            elif player.name == "Saksham":
                self.assertEqual(len(sample_team.get_players(PlayerPosition.GOALKEEPER)), 1, "Only one goalkeeper should be left in the team")
            else:
                # Final removal
                self.assertEqual(len(sample_team.get_players(PlayerPosition.GOALKEEPER)), 0, f"Player {player.name} not removed from the team")
                self.assertEqual(len(sample_team.get_players()), 0, "All players should have been removed from the team so None should be returned.")
                self.assertEqual(len(sample_team), 0, "All players should have been removed from the team")



        sample_team.add_player(sample_players[0])
        self.assertEqual(len(sample_team), 1, "The team should have 1 player")
        sample_team.add_player(sample_players[1])
        self.assertEqual(len(sample_team), 2, "The team should have 2 players")
        sample_team.add_player(sample_players[2])
        self.assertEqual(len(sample_team), 3, "The team should have 3 players")
        sample_team.add_player(sample_players[3])
        self.assertEqual(len(sample_team), 4, "The team should have 4 players")
        sample_team.add_player(sample_players[4])
        self.assertEqual(len(sample_team), 5, "The team should have 5 players")
        self.assertEqual(len(sample_team.get_players(PlayerPosition.GOALKEEPER)),
                         2, "The team should have 2 goalkeepers")
        self.assertEqual(len(sample_team.get_players(PlayerPosition.STRIKER)), 1, "The team should have 1 striker")
        self.assertEqual(len(sample_team.get_players(PlayerPosition.MIDFIELDER)),
                         1, "The team should have 1 midfielder")
        self.assertEqual(len(sample_team.get_players(PlayerPosition.DEFENDER)), 1, "The team should have 1 defender")
        self.assertEqual(len(sample_team.get_players(PlayerPosition.GOALKEEPER)),
                         2, "The team should have 2 goalkeepers")

    @number("4.6")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_get_players(self):
        """
        Testing if the players are returned correctly.
        """
        # Create a sample team different to the one in the setup
        sample_team = Team("Sample Team", ArrayR.from_list(self.sample_players[0:1]), 5)

        # Get the players
        players = sample_team.get_players()

        # Expected result
        expected = [self.sample_players[0]]

        # Check if the players are correct
        self.assertEqual(len(players), len(expected), "Incorrect number of players returned")
        self.assertEqual(players[0], expected[0], "Incorrect player returned")

        # Add all the rest of the players
        for player in self.sample_players[1:]:
            sample_team.add_player(player)

        # Get the players
        players = sample_team.get_players()

        # Expected result in order
        expected = ArrayR.from_list([self.sample_players[3], self.sample_players[4], self.sample_players[2], self.sample_players[1], self.sample_players[0]])

        # Check if the players are correct
        self.assertEqual(len(players), len(expected), "Incorrect number of players returned")
        for i in range(len(players)):
            self.assertEqual(players[i], expected[i], "Incorrect player returned / order of players incorrect")
