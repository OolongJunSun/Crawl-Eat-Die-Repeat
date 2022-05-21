import os

class Loader():
    def __init__(self, path) -> None:
        for folder in os.listdir(path):
            folders = []
            if "gen" in folder:
                folders.append(folder)
        
        print(folders[-1])

        gen_folder = os.path.join(path, folders[-1])

        print(gen_folder)

        self.gene_pool   = ""
        for file in os.listdir(gen_folder):
            if file.startswith("a"):
                pass
            else:
                with open(os.path.join(gen_folder,file), "r") as f:
                    l = f.readline().replace(" ","").strip("\n")
                    self.gene_pool += l


