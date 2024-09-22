from typing import Optional

import torch

from vllm import ModelRegistry
from vllm.model_executor.models.opt import OPTForCausalLM
from vllm.model_executor.models.phi3v import Phi3VForCausalLM
from vllm.model_executor.sampling_metadata import SamplingMetadata


class MyOPTForCausalLM(OPTForCausalLM):

    def compute_logits(
            self, hidden_states: torch.Tensor,
            sampling_metadata: SamplingMetadata) -> Optional[torch.Tensor]:
        # this dummy model always predicts the first token
        logits = super().compute_logits(hidden_states, sampling_metadata)
        if logits is not None:
            logits.zero_()
            logits[:, 0] += 1.0
        return logits


class MyPhi3VForCausalLM(Phi3VForCausalLM):

    def compute_logits(
            self, hidden_states: torch.Tensor,
            sampling_metadata: SamplingMetadata) -> Optional[torch.Tensor]:
        # this dummy model always predicts the first token
        logits = super().compute_logits(hidden_states, sampling_metadata)
        if logits is not None:
            logits.zero_()
            logits[:, 0] += 1.0
        return logits


def register():
    # register our dummy model
    if "MyOPTForCausalLM" not in ModelRegistry.get_supported_archs():
        ModelRegistry.register_model("MyOPTForCausalLM", MyOPTForCausalLM)

    # register our dummy multimodal model
    if "MyPhi3VForCausalLM" not in ModelRegistry.get_supported_archs():
        ModelRegistry.register_model("MyPhi3VForCausalLM",
                                     MyPhi3VForCausalLM,
                                     is_multimodal=True)
