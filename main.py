from solve import Solution
import argparse

# Parse CLI args
arg = argparse.ArgumentParser()
arg.add_argument("-m", "--method", required=False, default="bfs",
                 help="Specify which method to use: bfs or dfs")
arg.add_argument("-l", "--legend", required=False, default="false",
                 help="Set true to draw legend on the graph")
args = vars(arg.parse_args())

solve_method = args.get("method", "bfs")
legend_flag = str(args.get("legend", "false"))

def want_true(s):
    s = str(s).strip().lower()
    return s in {"1", "y", "yes", "t", "true"}

def main():
    s = Solution()

    if s.solve(solve_method):
        # Print solution steps on console
        s.show_solution()

        # Build output filename and optional legend
        output_file_name = f"{solve_method}"
        if want_true(legend_flag):
            s.draw_legend()
            output_file_name += "_legend.png"
        else:
            output_file_name += ".png"

        # Write state space tree
        s.write_image(output_file_name)
    else:
        raise Exception("No solution found")

if __name__ == "__main__":
    main()
