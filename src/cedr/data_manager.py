import os
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)


class Manager():
    def __init__(self) -> None:
        current_time = str(datetime.now())
        self.formatted_time = current_time.replace(" ", "_").replace(":", "-").split(".")[0]

    def make_output_dir(self, n=None):
        if isinstance(n, int):
            output_folder = f"runs\\{self.formatted_time}\\generation-{n}"
        else:
            output_folder = f"runs\\{self.formatted_time}"

        self.output_path = os.path.join(os.getcwd(), output_folder)

        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            print("Output folder for this run already exists.")


    def save_run_config(self, cfg):
        with open(f"{self.output_path}\\cfg.txt", "w") as f:
            for key, value in cfg.items():
                f.write(f"{str(key)} {str(value)}\n")


    def output_data(self, cohort, gen_results, gen_metrics, run_metrics):
        results_list = []
        for result in gen_results:
            cohort[result[0]]["fitness"] = result[1]

            o_string = f"{str(result[1])} - {cohort[result[0]]['genome']}"
            results_list.append(o_string)

        with open(f"{self.output_path}\\individuals.txt", "w") as f:
            for result in results_list:
                f.write(result+"\n")

        with open(f"{self.output_path}\\metrics.txt", "w") as f:
            f.write(str(gen_metrics))

        with open(f"{self.output_path}\\running_metrics.txt", "w") as f:
            for key, value in run_metrics.items():
                f.write(f"{str(key)} {str(value)}\n")

        pp.pprint(run_metrics)

    def load_population(self, pop_path: str) -> str:
        with open(os.path.join(pop_path, "individuals.txt")) as f:
            lines = f.readlines()

        return [line.split("-")[1][1:].strip() for line in lines]
