from semantic_kernel import Kernel
from src.services import Service
from src.service_settings import ServiceSettings
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatPromptExecutionSettings,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig


async def generate_response(anomaly: str, rule: str) -> str:
    # Use Semantic Kernel to generate a human-readable response.
    kernel = Kernel()

    service_settings = ServiceSettings.create()

    # Select a service to use for this notebook (available services: OpenAI, AzureOpenAI, HuggingFace)
    selectedService = (
        Service.OpenAI
        if service_settings.global_llm_service is None
        else Service(service_settings.global_llm_service.lower())
    )
    print(f"Using service type: {selectedService}")

    service_id = None

    if selectedService == Service.OpenAI:
        from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

        service_id = "default"
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
            ),
        )
    elif selectedService == Service.AzureOpenAI:
        from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

        service_id = "default"
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
            ),
        )

    prompt = """You are a cybersecurity expert. Based on the following inputs, provide a one- or two-sentence defensive recommendation. Be brief and straightforward.
    
    Anomaly detected: {{$anomaly}}
    Rule match: {{$rule}}

    Recommended Action:

    """

    if selectedService == Service.OpenAI:
        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            ai_model_id="gpt-4o-mini",
            max_tokens=2000,
            temperature=0.7,
        )
    elif selectedService == Service.AzureOpenAI:
        execution_settings = AzureChatPromptExecutionSettings(
            service_id=service_id,
            ai_model_id="gpt-35-turbo",
            max_tokens=2000,
            temperature=0.7,
        )

    prompt_template_config = PromptTemplateConfig(
        template=prompt,
        name="defence_recommendation",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(
                name="anomaly", description="The detected anomaly", is_required=True
            ),
            InputVariable(
                name="rule", description="The rule that was matched", is_required=True
            ),
        ],
        execution_settings=execution_settings,
    )

    defence = kernel.add_function(
        function_name="defenceFunc",
        plugin_name="defencePlugin",
        prompt_template_config=prompt_template_config,
    )

    res = await kernel.invoke(defence, input={"anomaly": anomaly, "rule": rule})

    return res
