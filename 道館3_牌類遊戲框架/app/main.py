from pprint import pprint

def main():
    from app.models.uno import Uno

    def dump_model(m):
        name = getattr(m, "name", getattr(m, "_name", None))
        hand = None
        if hasattr(m, "hand"):
            try:
                hand = list(m._hand)
            except Exception:
                hand = getattr(m, "hand", None)
        elif hasattr(m, "_hand"):
            try:
                hand = list(m._hand)
            except Exception:
                hand = getattr(m, "_hand", None)

        if hand is not None:
            try:
                return {"name": name, "hand": [str(c) for c in hand]}
            except Exception:
                return {"name": name, "hand_count": len(hand) if hasattr(hand, "__len__") else None}
        return str(m)
    import sys
    interactive = sys.stdin.isatty()

    # Showdown example
    try:
        from app.models.showdown import Showdown
        from app.models.showdown.player import HumanPlayer_showdown, AIPlayer_showdown
        from app.models.strategy.player import HumanStrategy, RandomAIStrategy

        p1 = HumanPlayer_showdown(HumanStrategy()) if interactive else AIPlayer_showdown()
        p2 = AIPlayer_showdown(RandomAIStrategy())
        p3 = AIPlayer_showdown(RandomAIStrategy())
        p4 = AIPlayer_showdown(RandomAIStrategy())


        game = Showdown(players=[p1, p2, p3, p4])
        game._start_game(13)

        print('\n--- Showdown initial hands ---')
        pprint([dump_model(p) for p in game.players])
        game._take_turns()
    except Exception as e:
        import traceback
        print("\n[Skip] Showdown demo unavailable:", e)
        traceback.print_exc()
    # Uno example
    try:
        from app.models.uno import HumanPlayer_uno, AIPlayer_uno, Uno
        from app.models.strategy.player import HumanStrategy, RandomAIStrategy

        p1 = HumanPlayer_uno(HumanStrategy()) if interactive else AIPlayer_uno()
        p2 = AIPlayer_uno(RandomAIStrategy())
        p3 = AIPlayer_uno(RandomAIStrategy())
        p4 = AIPlayer_uno(RandomAIStrategy())

        ug = Uno(players=[p1, p2, p3, p4])
        ug._start_game(5)

        print('\n--- Uno initial hands ---')
        pprint([dump_model(p) for p in ug.players])

        ug._take_turns()
    except Exception as e:
        print(f"\n[Skip] Uno demo unavailable: {e}")


if __name__ == "__main__":
    main()
