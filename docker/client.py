from .api.client import APIClient
from .constants import DEFAULT_TIMEOUT_SECONDS
from .models.configs import ConfigCollection
from .models.containers import ContainerCollection
from .models.images import ImageCollection
from .models.networks import NetworkCollection
from .models.nodes import NodeCollection
from .models.plugins import PluginCollection
from .models.secrets import SecretCollection
from .models.services import ServiceCollection
from .models.swarm import Swarm
from .models.volumes import VolumeCollection
from .utils import kwargs_from_env


class DockerClient(object):
    """
    A client for communicating with a Docker server.

    Example:

        >>> import docker
        >>> client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    Args:
        base_url (str): URL to the Docker server. For example,
            ``unix:///var/run/docker.sock`` or ``tcp://127.0.0.1:1234``.
        version (str): The version of the API to use. Set to ``auto`` to
            automatically detect the server's version. Default: ``1.35``
        timeout (int): Default timeout for API calls, in seconds.
        tls (bool or :py:class:`~docker.tls.TLSConfig`): Enable TLS. Pass
            ``True`` to enable it with default options, or pass a
            :py:class:`~docker.tls.TLSConfig` object to use custom
            configuration.
        user_agent (str): Set a custom user agent for requests to the server.
        credstore_env (dict): Override environment variables when calling the
            credential store process.
    """
    def __init__(self, *args, **kwargs):
        self.api = APIClient(*args, **kwargs)

    @classmethod
    def from_env(cls, **kwargs):
        """
        Return a client configured 客户端配置 from environment variables 从个环境变量.

        The environment variables used are the same as those used by the
        Docker command-line client. They are:
        环境变量的使用就像是他们通过docker命令行被使用一样

        .. envvar:: DOCKER_HOST

            The URL to the Docker host.

        .. envvar:: DOCKER_TLS_VERIFY  验证

            Verify the host against a CA certificate. 验证主机代理CA证书

        .. envvar:: DOCKER_CERT_PATH

            A path to a directory containing TLS certificates to use when
            connecting to the Docker host.
            当连接docker主机的时候使用包含TLS证书的目录路径

        Args:
            version (str): The version of the API to use. Set to ``auto`` to
                automatically detect the server's version. Default: ``1.35``
            timeout (int): Default timeout for API calls, in seconds.默认API调用超时
            ssl_version (int): A valid `SSL version`_.
            assert_hostname (bool): Verify the hostname of the server.验证主机名
            environment (dict): The environment to read environment variables
                from. Default: the value of ``os.environ``默认读取的环境变量
            credstore_env (dict): Override environment variables when calling
                the credential store process.调用凭据存储进程时重写环境变量

        Example:

            >>> import docker
            >>> client = docker.from_env()

        .. _`SSL version`:
            https://docs.python.org/3.5/library/ssl.html#ssl.PROTOCOL_TLSv1
        """
        timeout = kwargs.pop('timeout', DEFAULT_TIMEOUT_SECONDS)  # 默认60秒
        version = kwargs.pop('version', None)
        return cls(
            timeout=timeout, version=version, **kwargs_from_env(**kwargs)
        )

    # Resources
    @property
    def configs(self):
        """
        An object for managing configs on the server. See the
        :doc:`configs documentation <configs>` for full details.
        """
        return ConfigCollection(client=self)

    @property
    def containers(self):
        """
        An object for managing containers on the server. See the
        :doc:`containers documentation <containers>` for full details.
        服务器上管理容器的对象
        """
        return ContainerCollection(client=self)

    @property
    def images(self):
        """
        An object for managing images on the server. See the
        :doc:`images documentation <images>` for full details.
        服务器上管理镜像的对象
        """
        return ImageCollection(client=self)

    @property
    def networks(self):
        """
        An object for managing networks on the server. See the
        :doc:`networks documentation <networks>` for full details.
        服务器上管理网络的镜像
        """
        return NetworkCollection(client=self)

    @property
    def nodes(self):
        """
        An object for managing nodes on the server. See the
        :doc:`nodes documentation <nodes>` for full details.
        服务器上管理几点的对象
        """
        return NodeCollection(client=self)

    @property
    def plugins(self):
        """
        An object for managing plugins on the server. See the
        :doc:`plugins documentation <plugins>` for full details.
        服务器上管理插件的对象
        """
        return PluginCollection(client=self)

    @property
    def secrets(self):
        """
        An object for managing secrets on the server. See the
        :doc:`secrets documentation <secrets>` for full details.
        服务器上管理密钥的对象
        """
        return SecretCollection(client=self)

    @property
    def services(self):
        """
        An object for managing services on the server. See the
        :doc:`services documentation <services>` for full details.
        服务器上管理服务的对象
        """
        return ServiceCollection(client=self)

    @property
    def swarm(self):
        """
        An object for managing a swarm on the server. See the
        :doc:`swarm documentation <swarm>` for full details.
        """
        return Swarm(client=self)

    @property
    def volumes(self):
        """
        An object for managing volumes on the server. See the
        :doc:`volumes documentation <volumes>` for full details.
        """
        return VolumeCollection(client=self)

    # Top-level methods
    def events(self, *args, **kwargs):
        return self.api.events(*args, **kwargs)
    events.__doc__ = APIClient.events.__doc__

    def df(self):
        return self.api.df()
    df.__doc__ = APIClient.df.__doc__

    def info(self, *args, **kwargs):
        return self.api.info(*args, **kwargs)
    info.__doc__ = APIClient.info.__doc__

    def login(self, *args, **kwargs):
        return self.api.login(*args, **kwargs)
    login.__doc__ = APIClient.login.__doc__

    def ping(self, *args, **kwargs):
        return self.api.ping(*args, **kwargs)
    ping.__doc__ = APIClient.ping.__doc__

    def version(self, *args, **kwargs):
        return self.api.version(*args, **kwargs)
    version.__doc__ = APIClient.version.__doc__

    def close(self):
        return self.api.close()
    close.__doc__ = APIClient.close.__doc__

    def __getattr__(self, name):
        s = ["'DockerClient' object has no attribute '{}'".format(name)]
        # If a user calls a method on APIClient, they
        if hasattr(APIClient, name):
            s.append("In Docker SDK for Python 2.0, this method is now on the "
                     "object APIClient. See the low-level API section of the "
                     "documentation for more details.")
        raise AttributeError(' '.join(s))


from_env = DockerClient.from_env
