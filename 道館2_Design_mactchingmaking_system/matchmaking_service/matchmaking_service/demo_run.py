from pprint import pprint

def main():
    from matchmaking_service.models.individual import Individual
    from matchmaking_service.models.matchmaking_system import MatchmakingSystem

    
    def dump_model(m):
        if hasattr(m, "model_dump"):
            return m.model_dump()
        return m.dict()

    ind1 = Individual(id=1, gender="MALE", age=28, intro="Loves hiking", habits="hiking", coord=[24, 120])
    ind2 = Individual(id=2, gender="FEMALE", age=26, intro="Avid reader", habits="reading", coord=[15, 43])
    ind3 = Individual(id=3, gender="MALE", age=30, intro="Plays games", habits="gaming, reading", coord=[-34, 7])

    system = MatchmakingSystem(id=0)
    system._add_individuals([ind1, ind2, ind3])

    for ind in [ind1, ind2, ind3]:
        ind.partner = None

    print("\n--- Running Distance-Based (auto match) using Strategy instance ---")
    from matchmaking_service.models.strategies import (
        DistanceStrategy,
        HabitStrategy,
        NegateStrategy,
    )

    system._execute_strategies(DistanceStrategy())
    
    for ind in [ind1, ind2, ind3]:
        print(f"User {ind.id} matched with -> {ind.partner}")
    print("Individuals after Distance-Based:")
    pprint([dump_model(ind) for ind in [ind1, ind2, ind3]])

    for ind in [ind1, ind2, ind3]:
        ind.partner = None
    print("\n--- Running Habit-Based (auto match) using Strategy instance ---")
    system._execute_strategies(HabitStrategy())
    print("Individuals after Habit-Based:")
    pprint([dump_model(ind) for ind in [ind1, ind2, ind3]])

    for ind in [ind1, ind2, ind3]:
        ind.partner = None
    print("\n--- Running Distance-Reverse (pair farthest) using NegateStrategy ---")
    reverse_distance = NegateStrategy(DistanceStrategy())
    system._execute_strategies(reverse_distance)
    pprint([dump_model(ind) for ind in [ind1, ind2, ind3]])

    for ind in [ind1, ind2, ind3]:
        ind.partner = None
    print("\n--- Running Habit-Reverse (pair least common interest) using NegateStrategy ---")
    reverse_habit = NegateStrategy(HabitStrategy())
    system._execute_strategies(reverse_habit)
    pprint([dump_model(ind) for ind in [ind1, ind2, ind3]])


if __name__ == "__main__":
    main()
