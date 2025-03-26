from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import PlayerPosition
from player import Player
from random_gen import RandomGen
from team import Team


class GameSimulationOutcome:
    def __init__(self, home_goals: int, away_goals: int, goal_scorers: ArrayList[str]):
        """
        Constructor for the GameResults class

        Args:
            home_goals (int): The number of goals scored by the home team
            away_goals (int): The number of goals scored by the away team
            goal_scorers (ArrayList[str]): A list of the goal scorers in the game

        Returns:
            None
        """
        self.home_goals: int = home_goals
        self.away_goals: int = away_goals
        self.goal_scorers: ArrayList[str] = goal_scorers

        # You see how redundant the code above is? We take the argument, we set it on the object exactly as it is,
        # without even changing its name or anything. That's what dataclasses are for, as you can see in season.py.
        # We didn't use them for this class, so you can compare the two approaches.


class GameSimulator:

    @staticmethod
    def simulate(home_team: Team, away_team: Team) -> GameSimulationOutcome:
        """
        Simulates a game between two teams, considering player stats for a more probabilistic outcome.
        Note: To call this method, use: GameSimulator.simulate(home_team, away_team)

        Args:
            home_team (Team): The home team.
            away_team (Team): The away team.

        Returns:
            LinearProbeTable: A table with keys 'Home Goals', 'Away Goals', 'Goal Scorers',
                            'Goal Assists', 'Interceptions', 'Tacklers'
        """
        # 1. Determine goals scored by each team with a higher likelihood of low scores
        goal_distribution: list[int] = [0] * 30 + [1] * 30 + [2] * 20 + [3] * 10 + [4] * 5 + [5] * 5
        home_goals: int = RandomGen.random_choice(goal_distribution)
        away_goals: int = RandomGen.random_choice(goal_distribution)

        # 2. Select goal scorers based on stats
        goal_scorers = ArrayList[str]()
        home_players: ArrayR[Player] = home_team.get_players()
        away_players: ArrayR[Player] = away_team.get_players()

        # Get a list of outfield player from both teams
        home_outfield: list[Player] = [player for player in home_players if player.position != PlayerPosition.GOALKEEPER]
        away_outfield: list[Player] = [player for player in away_players if player.position != PlayerPosition.GOALKEEPER]

        all_players: ArrayR[Player] = ArrayR(len(home_players) + len(away_players))

        for i in range(len(home_players)):
            all_players[i] = home_players[i]

        for i in range(len(away_players)):
            all_players[i + len(home_players)] = away_players[i]

        for _ in range(home_goals):
            scorer: Player = RandomGen.random_choice(home_outfield)
            goal_scorers.append(scorer.name)

        for _ in range(away_goals):
            scorer: Player = RandomGen.random_choice(away_outfield)
            goal_scorers.append(scorer.name)

        return GameSimulationOutcome(home_goals, away_goals, goal_scorers)
