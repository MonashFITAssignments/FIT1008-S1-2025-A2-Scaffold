from __future__ import annotations

from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from typing import Collection, TypeVar

T = TypeVar("T")


class Team:
    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            initial_players (ArrayR[Player]): The players the team starts with initially
            history_length (int): The number of `GameResult`s to store in the history

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def get_players(self, position: PlayerPosition | None = None) -> Collection[Player]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (PlayerPosition or None): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder.
            
            This includes the ArrayR, which was previously prohibited.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError
        
    def add_result(self, result: TeamGameResult) -> None:
        """
        Add the `result` to this `Team`'s history

        Args:
            result (GameResult): The result to add
            
        Complexity:
            Best Case Complexity: 
            Worst Case Complexity: 
        """
        raise NotImplementedError

    def get_history(self) -> Collection[TeamGameResult] | None:
        """
        Returns the `GameResult` history of the team.
        If the team has played less than this team's `history_length`,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the result should be a container with 4 objects in this order:
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The most recent `GameResult`s for this team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError
    
    def make_post(self, post_date: str, post_content: str) -> None:
        """
        Publish a team blog `post` for a particular `post_date`.
       
        A `Team` can have one published post per day. Any duplicate
        posts should overwrite the original post for that day.
        
        Args:
            `post_date` (`str`) - The date of the post
            `post_content` (`str`) - The content of the post
        
        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure.
        """
        return str(self)
