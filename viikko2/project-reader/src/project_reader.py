from urllib import request
from project import Project
import toml


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        
        parsittu = toml.loads(content)
        poetry_data=parsittu.get("tool",{}).get("poetry",{})
        nim = poetry_data.get("name", "noname")
        kuvaus = poetry_data.get("description", "-")
        lisenssi = poetry_data.get("license","-")
        authors= poetry_data.get("authors","-")
        dependencies = list(poetry_data.get("dependencies", {}).keys())
        dev_dependencies = list(poetry_data.get("group", {}).get("dev", {}).get("dependencies", {}).keys())

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(nim, kuvaus,lisenssi,authors, dependencies, dev_dependencies)
