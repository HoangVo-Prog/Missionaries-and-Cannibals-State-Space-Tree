import os
import emoji
import pydot
import random
from collections import deque

# Không cần set Graphviz PATH trên Colab

# Dictionaries to backtrack solution nodes
Parent, Move, node_list = dict(), dict(), dict()

class Solution():
    def __init__(self):
        # Start (3M, 3C, Left) → Goal (0M, 0C, Right)
        self.start_state = (3, 3, 1)
        self.goal_state = (0, 0, 0)
        self.options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
        self.boat_side = ["right", "left"]

        self.graph = pydot.Dot(
            graph_type='graph',
            bgcolor="#fff3af",
            label="fig: Missionaries and Cannibal State Space Tree",
            fontcolor="red",
            fontsize="24"
        )

        self.visited = {}
        self.solved = False

    def is_valid_move(self, m, c):
        """Check number constraints"""
        return (0 <= m <= 3) and (0 <= c <= 3)

    def is_goal_state(self, m, c, s):
        return (m, c, s) == self.goal_state

    def is_start_state(self, m, c, s):
        return (m, c, s) == self.start_state

    def number_of_cannibals_exceeds(self, m, c):
        m_right, c_right = 3 - m, 3 - c
        return (m > 0 and c > m) or (m_right > 0 and c_right > m_right)

    def write_image(self, file_name="state_space.png"):
        try:
            self.graph.write_png(file_name)
            print(f"File '{file_name}' successfully written.")
        except Exception as e:
            print("Error while writing file:", e)

    def solve(self, solve_method="dfs"):
        self.visited = {}
        Parent[self.start_state] = None
        Move[self.start_state] = None
        node_list[self.start_state] = None
        return self.dfs(*self.start_state, 0) if solve_method == "dfs" else self.bfs()

    def draw_legend(self):
        """Draw color legend on graph"""
        graphlegend = pydot.Cluster(
            graph_name="legend",
            label="Legend",
            fontsize="20",
            color="gold",
            fontcolor="blue",
            style="filled",
            fillcolor="#fff4f4"
        )

        nodes = [
            ("1", "Start Node", "blue"),
            ("2", "Killed Node", "red"),
            ("3", "Solution nodes", "yellow"),
            ("4", "Can't be expanded", "gray"),
            ("5", "Goal node", "green"),
            ("7", "Node with child", "gold")
        ]
        for nid, label, color in nodes:
            n = pydot.Node(
                nid, style="filled", fillcolor=color,
                label=label, width="2", fixedsize="true"
            )
            graphlegend.add_node(n)

        desc = (
            "Each node (m, c, s) represents a state where m=missionaries, c=cannibals, s=side\n"
            "‘1’ = left, ‘0’ = right\n"
            "Goal: move all to right side (0, 0, 0)\n"
            "Boat options: (1,0), (0,1), (1,1), (0,2), (2,0)"
        )
        desc_node = pydot.Node(
            "6", style="filled", label=desc, shape="plaintext", fontsize="20", fontcolor="red"
        )
        graphlegend.add_node(desc_node)
        self.graph.add_subgraph(graphlegend)

    def draw(self, *, number_missionaries_left, number_cannibals_left, number_missionaries_right, number_cannibals_right):
        """Draw state using emojis"""
        left_m = emoji.emojize(':old_man:') * number_missionaries_left
        left_c = emoji.emojize(':ogre:') * number_cannibals_left
        right_m = emoji.emojize(':old_man:') * number_missionaries_right
        right_c = emoji.emojize(':ogre:') * number_cannibals_right
        print("({} {}) ---{:>40}--- ({} {})".format(left_m, left_c, "", right_m, right_c))
        print("")

    def show_solution(self):
        """Backtrack and display full solution path"""
        state = self.goal_state
        path, steps, nodes = [], [], []

        while state is not None:
            path.append(state)
            steps.append(Move[state])
            nodes.append(node_list[state])
            state = Parent[state]

        steps, nodes = steps[::-1], nodes[::-1]
        mL, cL, mR, cR = 3, 3, 0, 0

        print("*" * 60)
        self.draw(number_missionaries_left=mL, number_cannibals_left=cL,
                  number_missionaries_right=mR, number_cannibals_right=cR)

        for i, ((m, c, s), node) in enumerate(zip(steps[1:], nodes[1:])):
            if node and node.get_label() == str(self.start_state):
                node.set_style("filled")
                node.set_fillcolor("yellow")

            print(f"Step {i+1}: Move {m} missionaries and {c} cannibals from {self.boat_side[s]} side.")

            op = -1 if s == 1 else 1
            mL += op * m
            cL += op * c
            mR = 3 - mL
            cR = 3 - cL
            self.draw(number_missionaries_left=mL, number_cannibals_left=cL,
                      number_missionaries_right=mR, number_cannibals_right=cR)
        print("*" * 60)
        print("🎉 Congratulations! You have solved the problem!")

    def draw_edge(self, m, c, side, depth_level):
        u, v = None, None
        if Parent[(m, c, side)] is not None:
            u = pydot.Node(str(Parent[(m, c, side)]),
                           label=str(Parent[(m, c, side)][:3]))
            self.graph.add_node(u)

            v = pydot.Node(str((m, c, side)),
                           label=str((m, c, side)))
            self.graph.add_node(v)

            edge = pydot.Edge(str(Parent[(m, c, side)]),
                              str((m, c, side)),
                              dir='forward')
            self.graph.add_edge(edge)
        else:
            v = pydot.Node(str((m, c, side)),
                           label=str((m, c, side)))
            self.graph.add_node(v)
        return u, v

    def bfs(self):
        q = deque()
        q.append((*self.start_state, 0))
        self.visited[self.start_state] = True

        while q:
            m, c, s, d = q.popleft()
            u, v = self.draw_edge(m, c, s, d)

            if self.is_start_state(m, c, s):
                v.set_style("filled"); v.set_fillcolor("blue"); v.set_fontcolor("white")
            elif self.is_goal_state(m, c, s):
                v.set_style("filled"); v.set_fillcolor("green")
                return True
            elif self.number_of_cannibals_exceeds(m, c):
                v.set_style("filled"); v.set_fillcolor("red"); continue
            else:
                v.set_style("filled"); v.set_fillcolor("orange")

            op = -1 if s == 1 else 1
            can_be_expanded = False

            for x, y in self.options:
                next_m, next_c, next_s = m + op * x, c + op * y, int(not s)
                if self.is_valid_move(next_m, next_c) and (next_m, next_c, next_s) not in self.visited:
                    self.visited[(next_m, next_c, next_s)] = True
                    q.append((next_m, next_c, next_s, d + 1))
                    Parent[(next_m, next_c, next_s)] = (m, c, s)
                    Move[(next_m, next_c, next_s)] = (x, y, s)
                    node_list[(next_m, next_c, next_s)] = v
                    can_be_expanded = True

            if not can_be_expanded:
                v.set_style("filled")
                v.set_fillcolor("gray")
        return False

    def dfs(self, m, c, s, d):
        self.visited[(m, c, s)] = True
        u, v = self.draw_edge(m, c, s, d)

        if self.is_start_state(m, c, s):
            v.set_style("filled"); v.set_fillcolor("blue")
        elif self.is_goal_state(m, c, s):
            v.set_style("filled"); v.set_fillcolor("green"); return True
        elif self.number_of_cannibals_exceeds(m, c):
            v.set_style("filled"); v.set_fillcolor("red"); return False
        else:
            v.set_style("filled"); v.set_fillcolor("orange")

        solution_found = False
        operation = -1 if s == 1 else 1
        can_be_expanded = False

        for x, y in self.options:
            next_m, next_c, next_s = m + operation * x, c + operation * y, int(not s)
            if (next_m, next_c, next_s) not in self.visited:
                if self.is_valid_move(next_m, next_c):
                    can_be_expanded = True
                    Parent[(next_m, next_c, next_s)] = (m, c, s)
                    Move[(next_m, next_c, next_s)] = (x, y, s)
                    node_list[(next_m, next_c, next_s)] = v
                    solution_found = self.dfs(next_m, next_c, next_s, d + 1)
                    if solution_found:
                        return True

        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("gray")

        self.solved = solution_found
        return solution_found


if __name__ == "__main__":
    solver = Solution()
    solver.solve("bfs")  # hoặc "dfs"
    solver.show_solution()
    solver.draw_legend()
    solver.write_image("missionaries_cannibals.png")
