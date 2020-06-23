from abc import ABC, abstractmethod
from spotty.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotty.config.abstract_instance_config import AbstractInstanceConfig
from spotty.config.project_config import ProjectConfig


class AbstractInstanceManager(ABC):

    def __init__(self, project_config: ProjectConfig, instance_config: dict):
        self._project_config = project_config
        self._instance_config = self._get_instance_config(instance_config)

    @abstractmethod
    def _get_instance_config(self, instance_config: dict) -> AbstractInstanceConfig:
        """A factory method to create a provider's instance config."""
        raise NotImplementedError

    @abstractmethod
    def is_running(self):
        """Checks if the instance is running."""
        raise NotImplementedError

    @abstractmethod
    def start(self, output: AbstractOutputWriter, dry_run=False):
        """Creates a stack with the instance."""
        raise NotImplementedError

    @abstractmethod
    def stop(self, output: AbstractOutputWriter):
        """Deletes the stack."""
        raise NotImplementedError

    @abstractmethod
    def exec(self, command: list):
        """Executes a command on the host OS."""
        raise NotImplementedError

    @abstractmethod
    def clean(self, output: AbstractOutputWriter):
        """Deletes the stack."""
        raise NotImplementedError

    @abstractmethod
    def sync(self, output: AbstractOutputWriter, dry_run=False):
        """Synchronizes the project code with the instance."""
        raise NotImplementedError

    @abstractmethod
    def download(self, download_filters: list, output: AbstractOutputWriter, dry_run=False):
        """Downloads files from the instance."""
        raise NotImplementedError

    @abstractmethod
    def get_status_text(self) -> str:
        """Returns information about the started instance.

        It will be shown to the user once the instance is started and by using the "status" command.
        """
        raise NotImplementedError

    @property
    def use_tmux(self) -> bool:
        """Use tmux when running a custom script or connecting to the instance."""
        return True

    @property
    def project_config(self) -> ProjectConfig:
        return self._project_config

    @property
    def instance_config(self) -> AbstractInstanceConfig:
        return self._instance_config
