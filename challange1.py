
import random
import sys
from typing import List, Optional


class Card:
	def __init__(self, rank: int, suit: int):
		self.rank = rank
		self.suit = suit

	def __repr__(self) -> str:
		return f"Card(rank={self.rank}, suit={self.suit})"

	def __str__(self) -> str:
		ranks = {11: 'J', 12: 'Q', 13: 'K', 1: 'A'}
		suits = {0: '♣', 1: '♦', 2: '♥', 3: '♠'}
		r = ranks.get(self.rank, str(self.rank))
		s = suits.get(self.suit, str(self.suit))
		return f"{r}{s}"

	def __lt__(self, other: 'Card') -> bool:
		# treat Ace (rank==1) as highest for comparisons
		self_rank = 14 if self.rank == 1 else self.rank
		other_rank = 14 if other.rank == 1 else other.rank
		if self_rank != other_rank:
			return self_rank < other_rank
		return self.suit < other.suit

	def _sort_key(self):
		# key used for selecting/ comparing cards: (adjusted rank, suit)
		return (14 if self.rank == 1 else self.rank, self.suit)


class Deck:
	def __init__(self):
		self._cards: List[Card] = []
		self._build()

	def _build(self) -> None:
		# ranks 1..13 (2..10, J=11, Q=12, K=13, A=1), suits 0..3
		self._cards = [Card(rank, suit) for suit in range(4) for rank in range(1, 14)]

	def shuffle(self) -> None:
		random.shuffle(self._cards)

	def draw_card(self) -> Optional[Card]:
		if not self._cards:
			return None
		return self._cards.pop()

	@property
	def cards(self) -> List[Card]:
		return self._cards

	@cards.setter
	def cards(self, val: List[Card]) -> None:
		if not isinstance(val, list):
			raise TypeError('cards must be a list of Card')
		self._cards = val


class Player:
	def __init__(self):
		# private attributes
		self._hand: List[Card] = []
		self._can_change_hand: bool = True
		# rounds remaining before exchanged hands swap back
		self._exchange_timer: int = 3
		# reference to the partner player when exchanged
		self._exchange_partner: Optional[Player] = None

	def name_itself(self) -> str:
		return self.name

	def turn(self, player: str) -> str:
		return f"{self.name} ({player}) takes a turn"

	@staticmethod
	def _exchange_hands(player1: 'Player', player2: 'Player') -> None:
		player1._hand, player2._hand = player2._hand, player1._hand

	def decide_exchange(self, others: List['Player']) -> Optional['Player']:
		"""If player wants to exchange, return the chosen partner (not self). Otherwise return None.
		Subclasses override to implement selection (Human input or AI random).
		"""
		return None

	def take_turn(self, players: List['Player']) -> Optional[Card]:
		"""Perform the player's full turn: may decide to exchange (one-time), then play or skip.
		Return the played Card or None if skipping / no cards.
		"""
		# default: no exchange, just play
		return self.play_card()

	def set_name(self, name: str) -> None:
		if not name or not name.strip():
			raise ValueError("Name cannot be empty")
		self.name = name
		

	def is_name_valid(self) -> bool:
		return bool(self.name and self.name.strip())

	# properties for controlled access to private attributes

	@property
	def hand(self) -> List[Card]:
		# return a reference intentionally for mutation by internal methods; external code should use provided methods
		return self._hand

	@hand.setter
	def hand(self, value: List[Card]) -> None:
		if not isinstance(value, list):
			raise TypeError('hand must be a list of Card')
		self._hand = value

	@property
	def can_change_hand(self) -> bool:
		return self._can_change_hand

	@can_change_hand.setter
	def can_change_hand(self, val: bool) -> None:
		if not isinstance(val, bool):
			raise TypeError('can_change_hand must be a bool')
		self._can_change_hand = val

	@property
	def exchange_timer(self) -> int:
		return self._exchange_timer

	@exchange_timer.setter
	def exchange_timer(self, val: int) -> None:
		if not isinstance(val, int) or val < 0:
			raise ValueError('exchange_timer must be a non-negative int')
		self._exchange_timer = val

	@property
	def exchange_partner(self) -> Optional['Player']:
		return self._exchange_partner

	@exchange_partner.setter
	def exchange_partner(self, val: Optional['Player']) -> None:
		if val is not None and not isinstance(val, Player):
			raise TypeError('exchange_partner must be a Player or None')
		self._exchange_partner = val

	def play_card(self) -> Optional[Card]:
		if not self._hand:
			return None
		return self._hand.pop(0)
	@staticmethod
	def _should_swap_back(player: 'Player') -> None:
		if not player._can_change_hand and player._exchange_timer > 0:
			player._exchange_timer -= 1
		if player._exchange_timer == 0 and player._exchange_partner is not None:
			partner = player._exchange_partner
			# swap back only once
			Player._exchange_hands(player, partner)
			print(f"{player.name} and {partner.name} swapped hands back after 3 rounds")
			player._exchange_partner = None
			player._exchange_timer = 0


class HumanPlayer(Player):
	def play_card(self) -> Optional[Card]:
		if not self.hand:
			return None
		# simple CLI: show hand and ask index; on invalid input raise an error
		print(f"{self.name}'s hand: ", ' '.join(f"[{i}]{c}" for i, c in enumerate(self.hand)))
		try:
			choice = input(f"Select card index to play (0..{len(self.hand)-1}): ")
		except EOFError:
			raise EOFError("No input available for card selection")
		if not choice or not choice.strip():
			raise ValueError("No card index entered")
		try:
			idx = int(choice.strip())
		except ValueError:
			raise ValueError(f"Invalid index value: {choice!r}")
		if idx < 0 or idx >= len(self.hand):
			raise IndexError(f"Selected index {idx} out of range (0..{len(self.hand)-1})")
		return self.hand.pop(idx)

	def decide_exchange(self, others: List[Player]) -> Optional[Player]:
		if not self.can_change_hand:
			return None
		while True:
			try:
				resp = input(f"{self.name}: do you want to exchange hands? (y/n) ")
			except EOFError:
				resp = 'n'
			if not resp:
				return None
			r = resp.strip().lower()
			if r in ('n', 'no', 'false', '0'):
				return None
			if r in ('y', 'yes', 'true', '1'):
				# list other players to choose
				for idx, op in enumerate(others):
					print(f"[{idx}] {op.name}")
					# build a compact player list for the prompt
				player_list = ', '.join(f"{i}={o.name}" for i, o in enumerate(others))
				prompt = f"Choose player to exchange with ({player_list}), or Enter to cancel: "
				while True:
					try:
						choice = input(prompt)
					except EOFError:
						choice = ''
					if choice.strip() == '':
						return None
					try:
						ci = int(choice)
						if 0 <= ci < len(others):
							return others[ci]
					except ValueError:
						pass
					print('Invalid index, try again.')
			print('Please answer y/yes or n/no.')

	def take_turn(self, players: List[Player]) -> Optional[Card]:
		# check if need to swap back first
		Player._should_swap_back(self)
		# before playing, allow exchange if available
		if self.can_change_hand:
			others = [op for op in players if op is not self]
			partner = self.decide_exchange(others)
			if partner is not None:
				Player._exchange_hands(self, partner)
				self.exchange_partner = partner
				partner.exchange_partner = self
				self.can_change_hand = False
				print(f"{self.name} exchanged hands with {partner.name} for 3 rounds")

		# then play (or skip)
		return self.play_card()


class AIPlayer(Player):
	def decide_exchange(self, others: List[Player]) -> Optional[Player]:
		if not self.can_change_hand:
			return None
		if not others:
			return None
		if random.choice([True, False]):
			return random.choice(others)
		return None

	def take_turn(self, players: List[Player]) -> Optional[Card]:
		# check if need to swap back first
		Player._should_swap_back(self)
		# before playing, allow exchange if available
		if self.can_change_hand:
			others = [op for op in players if op is not self]
			partner = self.decide_exchange(others)
			change = random.choice([True, False])
			if change and partner is not None:
				Player._exchange_hands(self, partner)
				self.exchange_partner = partner
				self.can_change_hand = False
				print(f"{self.name} exchanged hands with {partner.name} for 3 rounds")
		# then play
		if not self.hand:
			return None
		best_idx = max(range(len(self.hand)), key=lambda i: self.hand[i]._sort_key())
		return self.hand.pop(best_idx)


class Showdown:

	@property
	def players(self) -> List[Player]:
		return self._players

	@property
	def deck(self) -> Deck:
		return self._deck

	@property
	def points(self) -> dict:
		return self._points

	def start_game(self, interactive: bool = True) -> None:
		players: List[Player] = []
		for i in range(4):
			if interactive and i == 0 and sys.stdin.isatty():
				players.append(HumanPlayer())
			else:
				players.append(AIPlayer())
		for p in players:
			name = input("Enter name (cannot be empty): ")
			p.set_name(name.strip())
		self._players = players
		self._deck = Deck()
		self._points = {p.name: 0 for p in players}
		self._deck.shuffle()
		# deal 13 cards to each player
		for _ in range(13):
			for p in self.players:
				card = self.deck.draw_card()
				if card:
					p.hand.append(card)


	def show_card_and_compare(self) -> None:
		# play 13 rounds
		for round_no in range(1, 14):
			print(f"\n--- Round {round_no} ---")
			played = []
			for p in self.players:
				# each player performs their full turn (may exchange then play)
				c = p.take_turn(self.players)
				played.append((p, c))
				if c is None:
					print(f"{p.name} does not play this round")
				else:
					print(f"{p.name} plays {c}")

			# determine winner by highest card
			valid_played = [(p, c) for (p, c) in played if c is not None]
			if not valid_played:
				print("No cards played this round.")
				continue
			winner, winning_card = max(valid_played, key=lambda pc: pc[1]._sort_key())
			self.points[winner.name] += 1
			print(f"{winner.name} wins the round with {winning_card} (+1 point)")

		print("\n--- Game Over ---")
		for name, pts in self.points.items():
			print(f"{name}: {pts} points")
		# announce winner(s)
		max_pts = max(self.points.values())
		winners = [n for n, p in self.points.items() if p == max_pts]
		if len(winners) == 1:
			print(f"Winner: {winners[0]} with {max_pts} points")
		else:
			print(f"Tie between: {', '.join(winners)} with {max_pts} points each")


if __name__ == '__main__':
	print('Starting Showdown demo...')
	interactive = sys.stdin.isatty()
	game = Showdown()
	game.start_game(interactive=interactive)
	game.show_card_and_compare()

