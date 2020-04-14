from abc import abstractmethod
from provit import Provenance
from ..config import PROVIT_AGENT


class Builder:
    """
    This class mainly provides a wrapper around a build_dataset command.
    It is especially useful to handle provenance creation. This

    Every sublass is excpected to have both PROVIT_ACTIVITY and PROVIT_DESCRIPTION.
    """

    def __init__(self, sources=None, primary_source=""):
        if sources is None:
            sources = list()
        else:
            self.sources = sources
        self.primary_source = primary_source

    def build(self, outfilename):
        """
        Wrapper to build the dataset and write the provenance.
        """
        self.build_dataset(outfilename)
        self.save_provenance(outfilename)
        return outfilename

    @abstractmethod
    def build_dataset(self, outfilename):
        pass

    def save_provenance(self, outfilename):
        """
        Save the provenance.
        """
        prov = Provenance(outfilename, overwrite=True)
        prov.add(
            agents=[PROVIT_AGENT],
            activity=self.PROVIT_ACTIVITY,
            description=self.PROVIT_DESCRIPTION,
        )
        prov.add_sources(self.sources)
        prov.add_primary_source(self.primary_source)
        prov.save()
        return prov
