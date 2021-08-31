import argparse

from game import train, GameEngine
from heuristics import evaluation_function
from minimax_agent import MinMax, AlphaBeta
from monte_carlo_agent import MonteCarloAgent
from random_agent import RandomAgent
from reinforcement_learning_agent import QLearningAgent


def _agent_random_provider(args):
    return RandomAgent()


def _agent_random_parser(base):
    pass


def _first_agent_minimax_provider(args):
    return MinMax(evaluation_function, depth=args.agent1_depth)


def _first_agent_minimax_parser(base):
    base.add_argument('--agent1-depth', type=int, help='The depth of the search to be performed', default=2)


def _second_agent_minimax_provider(args):
    return MinMax(evaluation_function, depth=args.agent2_depth)


def _second_agent_minimax_parser(base):
    base.add_argument('--agent2-depth', type=int, help='The depth of the search to be performed', default=2)


def _first_agent_alpha_beta_provider(args):
    return AlphaBeta(evaluation_function, depth=args.agent1_depth)


def _first_agent_alpha_beta_parser(base):
    base.add_argument('--agent1-depth', type=int, help='The depth of the search to be performed', default=2)


def _second_agent_alpha_beta_provider(args):
    return AlphaBeta(evaluation_function, depth=args.agent2_depth)


def _second_agent_alpha_beta_parser(base):
    base.add_argument('--agent2-depth', type=int, help='The depth of the search to be performed', default=2)


def _first_agent_monte_carlo_provider(args):
    return MonteCarloAgent(simulations_num=args.agent1_simulation_num)


def _first_agent_monte_carlo_parser(base):
    base.add_argument('--agent1-simulation-num', type=int, help='The number of actions to simulate', default=500)


def _second_agent_monte_carlo_provider(args):
    return MonteCarloAgent(simulations_num=args.agent2_simulation_num)


def _second_agent_monte_carlo_parser(base):
    base.add_argument('--agent2-simulation-num', type=int, help='The number of actions to simulate', default=500)


def _first_agent_q_learning_provider(args):
    agent = QLearningAgent(args.agent1_epsilon, args.agent1_gamma, args.agent1_alpha, args.agent1_training_episodes)
    train(agent)
    return agent


def _first_agent_q_learning_parser(base):
    base.add_argument('--agent1-alpha', type=float, help='The Q learning\'s learn rate', default=0.2)
    base.add_argument('--agent1-epsilon', type=float, help='The Q learning\'s exploration rate', default=0.05)
    base.add_argument('--agent1-gamma', type=float, help='The Q learning\'s discount factor', default=0.8)
    base.add_argument('--agent1-training-episodes', type=int, help='The amount of episodes to train', default=2000)


def _second_agent_q_learning_provider(args):
    agent = QLearningAgent(args.agent2_epsilon, args.agent2_gamma, args.agent2_alpha, args.agent2_training_episodes)
    train(agent)
    return agent


def _second_agent_q_learning_parser(base):
    base.add_argument('--agent2-alpha', type=float, help='The Q learning\'s learn rate', default=0.2)
    base.add_argument('--agent2-epsilon', type=float, help='The Q learning\'s exploration rate', default=0.05)
    base.add_argument('--agent2-gamma', type=float, help='The Q learning\'s discount factor', default=0.8)
    base.add_argument('--agent2-training-episodes', type=int, help='The amount of episodes to train', default=2000)


AGENT_PARSERS = {
    'R': (_agent_random_parser, _agent_random_parser),
    'MM': (_first_agent_minimax_parser, _second_agent_minimax_parser),
    'ABP': (_first_agent_alpha_beta_parser, _second_agent_alpha_beta_parser),
    'MCPE': (_first_agent_monte_carlo_parser, _second_agent_monte_carlo_parser),
    'QL': (_first_agent_q_learning_parser, _second_agent_q_learning_parser)
}


AGENT_BUILDERS = {
    'R': (_agent_random_provider, _agent_random_provider),
    'MM': (_first_agent_minimax_provider, _second_agent_minimax_provider),
    'ABP': (_first_agent_alpha_beta_provider, _second_agent_alpha_beta_provider),
    'MCPE': (_first_agent_monte_carlo_provider, _second_agent_monte_carlo_provider),
    'QL': (_first_agent_q_learning_provider, _second_agent_q_learning_provider)
}


def _to_unified_name(first, second):
    return f'{first}_vs_{second}'


def _from_unified_name(name):
    return name.strip().split('_vs_')


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--games', type=int, help='The number of games to play.', default=1)
    parser.add_argument('-q', '--quiet', action='store_true')
    subparsers = parser.add_subparsers(dest='match')

    for first_agent in AGENT_PARSERS:
        for second_agent in AGENT_PARSERS:
            sub = subparsers.add_parser(_to_unified_name(first_agent, second_agent))
            AGENT_PARSERS[first_agent][0](sub)
            AGENT_PARSERS[second_agent][1](sub)

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()
    if args.match is None:
        print(
            'Usage: santorini.py [-h] [-g Games] [-q] <agent1>_vs_<agent2>\n'
            '                    agent1 and agent2 can be any of [R, MM, ABP, MCPE, QL] where\n'
            '                    R:\t\tRandom Agent\n'
            '                    MM:\t\tMinimax Agent\n'
            '                    ABP:\tAlpha Beta Pruning Agent\n'
            '                    MCPE:\tMonte Carlo Policy Evaluation Agent\n'
            '                    QL:\t\tQ-Learning Agent\n'
        )
    else:
        agent1_name, agent2_name = _from_unified_name(args.match)
        agent1, agent2 = AGENT_BUILDERS[agent1_name][0](args), AGENT_BUILDERS[agent2_name][1](args)

        if args.games == 1:
            GameEngine().play_agents_versus(agent1, agent2, not args.quiet, not args.quiet)
        else:
            reset_agent1, reset_agent2 = agent1_name in ['MM', 'ABP'], agent2_name in ['MM', 'ABP']
            GameEngine().versus_multiple_rounds(agent1, agent2, args.games, reset_agent1, reset_agent2)


if __name__ == '__main__':
    main()