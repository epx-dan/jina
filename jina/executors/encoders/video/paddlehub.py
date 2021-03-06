__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

from ..paddlehub import PaddlehubEncoder


class VideoPaddlehubEncoder(PaddlehubEncoder):
    """
    :class:`VideoPaddlehubEncoder` encodes data from a ndarray, potentially B x T x (Channel x Height x Width) into a
        ndarray of `B x D`.
    Internally, :class:`VideoPaddlehubEncoder` wraps the models from `paddlehub`.
    https://github.com/PaddlePaddle/PaddleHub
    """
    def __init__(self,
                 model_name: str = 'tsn_kinetics400',
                 output_feature: str = '@HUB_tsn_kinetics400@reduce_mean_0.tmp_0',
                 pool_strategy: str = None,
                 *args, **kwargs):
        """

        :param model_name: the name of the model. Supported models include ``tsn_kinetics400``, ``stnet_kinetics400``,
            ``tsm_kinetics400``
        :param output_feature: the name of the layer for feature extraction. Please use the following values for the
            supported models:
            ``tsn_kinetics400``: `@HUB_tsn_kinetics400@reduce_mean_0.tmp_0`
            ``stnet_kinetics400``: ``@HUB_stnet_kinetics400@reshape2_6.tmp_0``
            ``tsm_kinetics400``: ``@HUB_tsm_kinetics400@reduce_mean_0.tmp_0``
        :param pool_strategy: the pooling strategy
            - `None` means that the output of the model will be the output feature.
            - `mean` means that global average pooling will be applied to the output feature, and thus the output of the
                model will be a 2D tensor.
            - `max` means that global max pooling will be applied.
        """
        if 'pool_strategy' in kwargs:
            kwargs.pop('pool_strategy')
        if 'output_feature' in kwargs:
            kwargs.pop('output_feature')
        super().__init__(model_name, output_feature, pool_strategy, *args, **kwargs)
        if pool_strategy not in ('mean', 'max', None):
            raise NotImplementedError('unknown pool_strategy: {}'.format(self.pool_strategy))

    def get_inputs_and_outputs_name(self, input_dict, output_dict):
        self.inputs_name = input_dict[0].name

    def close(self):
        self.exe.close()
