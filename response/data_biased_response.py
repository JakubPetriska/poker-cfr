import random
import numpy as np

from cfr.main import Cfr


class DataBiasedResponse(Cfr):
    def __init__(
            self,
            game,
            opponent_sample_tree,
            p_max=0.8,
            show_progress=True):
        super().__init__(game, show_progress)
        self.opponent_sample_tree = opponent_sample_tree
        self.p_max = p_max

    def _start_iteration(self):
        self._cfr(
            ([self.game_tree] * self.player_count) + [self.opponent_sample_tree],
            np.ones(self.player_count),
            None,
            [],
            [False] * self.player_count)

    def _get_current_strategy(self, nodes):
        samples_node = nodes[-1]
        samples_count = np.sum(samples_node.action_decision_counts)
        p_conf = self.p_max * min(1, samples_count / 10)
        if random.random() <= p_conf:
            return samples_node.action_decision_counts / samples_count
        else:
            return super(DataBiasedResponse, self)._get_current_strategy(nodes)
