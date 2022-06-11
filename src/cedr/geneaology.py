import os

from datetime import datetime


class History():
    def __init__(self) -> None:
        current_time = str(datetime.now())
        self.formatted_time = current_time.replace(" ", "_").replace(":", "-").split(".")[0]

    def make_output_dir(self, n=None):
        if n:
            output_folder = f"runs\\{self.formatted_time}\\generation-{n}"
        else:
            output_folder = f"runs\\{self.formatted_time}"

        output_path = os.path.join(os.getcwd(), output_folder)

        try:
            os.mkdir(output_path)
        except FileExistsError:
            print("Output folder for this run already exists.")
