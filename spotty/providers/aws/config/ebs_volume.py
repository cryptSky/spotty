from spotty.config.abstract_instance_volume import AbstractInstanceVolume
from spotty.providers.aws.config.validation import validate_ebs_volume_parameters


class EbsVolume(AbstractInstanceVolume):

    DP_CREATE_SNAPSHOT = 'CreateSnapshot'
    DP_UPDATE_SNAPSHOT = 'UpdateSnapshot'
    DP_RETAIN = 'Retain'
    DP_DELETE = 'Delete'

    def __init__(self, volume_config: dict, project_name: str, instance_name: str):
        self._name = volume_config['name']
        self._params = validate_ebs_volume_parameters(volume_config['parameters'])

        self._project_name = project_name
        self._instance_name = instance_name

    @property
    def title(self):
        return 'EBS volume'

    @property
    def name(self):
        return self._name

    @property
    def size(self) -> int:
        return self._params['size']

    @property
    def type(self) -> str:
        return self._params['type']

    @property
    def deletion_policy(self) -> str:
        return self._params['deletionPolicy']

    @property
    def deletion_policy_title(self) -> str:
        return {
            EbsVolume.DP_CREATE_SNAPSHOT: 'Create Snapshot',
            EbsVolume.DP_UPDATE_SNAPSHOT: 'Update Snapshot',
            EbsVolume.DP_RETAIN: 'Retain Volume',
            EbsVolume.DP_DELETE: 'Delete Volume',
        }[self.deletion_policy]

    @property
    def ec2_volume_name(self) -> str:
        """Returns EBS volume name."""
        volume_name = self._params['volumeName']
        if not volume_name:
            volume_name = '%s-%s-%s' % (self._project_name.lower(), self._instance_name.lower(), self.name.lower())

        return volume_name

    @property
    def mount_dir(self) -> str:
        """A directory where the volume should be mounted on the host OS."""
        if self._params['mountDir']:
            mount_dir = self._params['mountDir']
        else:
            mount_dir = '/mnt/%s' % self.ec2_volume_name

        return mount_dir

    @property
    def host_path(self) -> str:
        """A path on the host OS that will be mounted to the container."""
        return self.mount_dir
