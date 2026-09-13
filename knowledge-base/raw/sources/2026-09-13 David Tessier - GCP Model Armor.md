---
type: raw-source
source_id: src-2026-09-13-tessier-gcp-model-armor
title: "Leveraging GCP Model Armor for Robust LLM and Agentic AI Security"
author: David Tessier
url: "https://medium.com/google-cloud/leveraging-gcp-model-armor-for-robust-llm-and-agentic-ai-security-777558c6cee2"
published: 2025-03-26
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - ai-agents
  - security
  - google-cloud
status: active
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UOktbl6F_NCJ30MKRhCaTw.jpeg)

The landscape of artificial intelligence is rapidly evolving with the emergence of **Agentic AI**, defined as Large Language Model (LLM)-based systems capable of autonomous decision-making and action with minimal human intervention1. This paradigm shift holds immense potential across various sectors such as customer service, supply chain management, and financial services1. However, the very autonomy and dynamic interaction capabilities that make these systems powerful also introduce **critical security and privacy challenges**, leaving them vulnerable to various threats.

These vulnerabilities include:

- **Prompt Injection**: Where malicious actors manipulate the agent’s behavior by inserting crafted prompts into its input stream2.
- **Data Poisoning**: Corrupting the training data to introduce biases or vulnerabilities into the model2.
- **Model Extraction**: Stealing the model’s parameters or architecture to create a copy or understand its weaknesses2.
- • **Unintended Consequences**: The agent’s actions might have unforeseen and potentially harmful effects due to its complex decision-making process.
- **Ethical Concerns**: The agent’s behavior might violate ethical principles or societal norms.

To address these critical security and privacy challenges, a concept analogous to physical armor for a soldier has emerged: **“Model Armor”**. Model Armor aims to safeguard these intelligent agents from malicious attacks and unintended consequences.

### What is “Model Armor”?

**Model Armor** is not a single tool but rather a **conceptual framework** encompassing a suite of techniques and strategies designed to enhance the robustness, security, and resilience of AI models, particularly those deployed in agentic contexts …. It represents a **layered approach**, addressing vulnerabilities at various stages of an agent’s lifecycle.

Key aspects of Model Armor include:

- **Input Validation and Sanitization**: Filtering and cleaning input data to prevent injection attacks and adversarial prompts.
- **Output Monitoring and Control**: Scrutinizing the agent’s actions and outputs for anomalies or potentially harmful behaviors.
- **Model Hardening**: Strengthening the underlying AI model against adversarial attacks, such as prompt injection, data poisoning, and model extraction.
- **Runtime Monitoring and Anomaly Detection**: Continuously observing the agent’s behavior and detecting deviations from expected patterns.
- **Explainability and Interpretability**: Providing insights into the agent’s decision-making process to identify and mitigate potential biases or errors.
- **Policy Enforcement and Guardrails**: Defining clear boundaries and rules for the agent’s actions, ensuring adherence to ethical and safety standards.
- **Feedback loops and reinforcement learning**: Allowing the agent to learn from its mistakes and improve its safety over time.

Model Armor provides a **multi-layered defense**, mitigating the previously listed risks and ensuring that the agent operates safely and reliably. There are various solutions on the market leveraging this type of conceptual framework, including Prompt Security, Meta’s Prompt Guard, Kong’s AI Prompt Guard, and open-source options like GPTSafe Prompt Guard, PromptMap, and LLM Guard. However the focus of this article is Google Cloud’s new service called *“Model Armor”.*

### Google Cloud — Model Armor Service

Recently, **Google Cloud introduced its own managed solution called *Model Armor***. This **fully managed service** provided by Google Cloud Platform offers capabilities to enhance the safety and security of AI applications by leveraging the concepts of Model Armor. Model Armor screens LLM prompts and responses for various types of security and safety risks.

GCP’s Model Armor offers the following core features:

- **Universal Model and Cloud Compatibility**: Operates independently of specific AI models or cloud platforms, enabling **seamless integration across multi-cloud and multi-model environments**.
- **Centralized Policy Management**: Provides a **unified platform for managing and enforcing security and safety policies** across all deployed AI models.
- **API-Driven Integration**: Offers a **public REST API for direct integration of prompt and response screening into applications**, supporting diverse deployment architectures.
- **Granular Access Control**: Implements **Role-Based Access Control (RBAC)** to precisely manage user permissions and access levels.
- **Low-Latency Regional Endpoints**: Delivers API access through regional endpoints to **minimize latency and optimize performance**.
- **Global Availability**: Deployed across multiple regions in the United States and Europe for **broad accessibility**.
- **Security Command Center Integration**: **Seamlessly integrates with Security Command Center**, allowing for centralized visibility, violation detection, and remediation.

**GCP Model Armor also offers enhanced safety and security**:

- **Comprehensive Content Safety Filters**: Includes filters for detecting and mitigating harmful content, such as sexually explicit material, dangerous content, harassment, and hate speech.
- **Advanced Threat Detection**: Detects and prevents **prompt injection and jailbreak attacks**, safeguarding AI models from manipulation9. It also **detects Malicious URLs within prompts and responses**.
- **Integrated Data Loss Prevention (DLP)**: Leverages Google Cloud’s Sensitive Data Protection to discover, classify, and protect sensitive data (e.g., PII, intellectual property), preventing unauthorized disclosure.
- **PDF Content Screening**: Supports the screening of text within PDF documents for malicious content.

Model Armor is accessible through a Global endpoint *(modelarmor.googleapis.com)* or regional endpoints in supported regions like Iowa (us-central1), Northern Virginia (us-east4), Oregon (us-west1) in the United States, and Netherlands (europe-west4) in Europe9. It can be purchased as a standalone service or integrated as part of Security Command Center.

### Configuring GCP’s Model Armor

The standard reference architecture for Model Armor involves an application using it to protect an LLM and a user.

The following IAM Roles can be used to control access to Model Armor:

- *modelarmor.admin & modelarmor.floorSettingsAdmin*: For Administrators and owners.
- *modelarmor.user*: For users and applications planning to screen prompts and responses.
- *modelarmor.viewer*: For template viewers11.
- *modelarmor.floorSettingsViewer*: For Floor Settings Viewers11.

### Enabling Model Armor

Model Armor can be configured using the GCP Console or the gcloud command-line tool11. To enable the Model Armor API, you first configure the endpoint override with the regional endpoint if desired12:

```c
gcloud config set api_endpoint_overrides/modelarmor "https://modelarmor.LOCATION.rep.googleapis.com/"
```

Replace LOCATION with the desired supported region. Otherwise, the default global endpoint is used (modelarmor.googleapis.com)12. Finally, enable the API:

```c
gcloud services enable modelarmor.googleapis.com --project=PROJECT_ID
```

### Templates

To screen prompts and responses, you must create **Model Armor Templates**, which are sets of customized filters for safety and security thresholds12. These templates allow control over the content being flagged by configuring confidence thresholds and triggers for various risks:

- **Prompt Injection & Jailbreak Attacks**: Detects and blocks manipulative inputs.
- **Sensitive Data Leakage**: Protects personally identifiable information (PII) and intellectual property.
- **Malicious URLs**: Identifies phishing links embedded in prompts or responses.
- **Harmful Content**: Filters explicit, violent, or biased outputs.
- **PDF Content Scanning**: Inspects text within PDFs for security risks.

These thresholds represent **confidence levels**, indicating how confident the service is about the prompt and/or response including any offending content. An example JSON shows how to set confidence levels for different harmful content filters14. You can create a template using the gcloud command, also including custom error codes and messages to be returned upon a filter match.

```c
[
    { "filterType": "HATE_SPEECH", "confidenceLevel": "MEDIUM_AND_ABOVE" },
    { "filterType": "DANGEROUS", "confidenceLevel": "MEDIUM_AND_ABOVE"},
    { "filterType": "HARASSMENT", "confidenceLevel": "MEDIUM_AND_ABOVE" },
    { "filterType": "SEXUALLY_EXPLICIT", "confidenceLevel": "MEDIUM_AND_ABOVE" }
]
```

## Model Armor Integration

Once a Model Armor template is created, you have two main options for validation and/or sanitization: **User Prompt Inspection/Sanitization** and **LLM Model Response Inspection/Sanitization**.

For **User Prompt Inspection/Sanitization**, the Model Armor service validates the user’s prompt against the configured safety and protection filters16. The following Python code demonstrates integration17:

```c
from google.cloud import modelarmor_v1
# Create the model armor client
ml_armor_client = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options={"api_endpoint": "https://modelarmor.us-central1.rep.googleapis.com"},
    credentials=creds
)
# inspect user prompt
user_prompt_data = modelarmor_v1.DataItem()
user_prompt_data.text = prompt
request = modelarmor_v1.SanitizeUserPromptRequest(
    name=gcp_model_armor_template,
    user_prompt_data=user_prompt_data
)
response = client.sanitize_user_prompt(request)
```

If a match is found, you can prevent the prompt from reaching the LLM and display a custom message, such as: “Unfortunately I cannot process that question, please refine your request and avoid any explicit content.”18.

Similarly, for **LLM Model Response Inspection/Sanitization**, you can inspect and sanitize the response returned by the LLM before displaying it to the user18. The Python code for this is similar19:

```c
from google.cloud import modelarmor_v1
# Create the model armor client
ml_armor_client = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options={"api_endpoint": "https://modelarmor.us-central1.rep.googleapis.com"},
    credentials=creds
)
# inspect LLM response
client = get_model_armor_client()
llm_resp_data = modelarmor_v1.DataItem()
llm_resp_data.text = llm_response
request = modelarmor_v1.SanitizeModelResponseRequest(
    name=gcp_model_armor_template,
    model_response_data=llm_resp_data
)
response = client.sanitize_model_response(request)
```

If a match is found in the LLM response, you can restrict its display and show a message like: “The content returned from the LLM has been reviewed for harmful or explicit content. Unfortunate we cannot display this content.”.

A **sample sanitization output** demonstrates the structure of the response, indicating whether a match was found for different filter types (like sdp, rai, pi\_and\_jailbreak, malicious\_uris, csam) and including sanitization metadata with error codes and messages.

```c
filter_match_state: MATCH_FOUND
filter_results {
  key: "sdp"
  value {
    sdp_filter_result {
      inspect_result {
        execution_state: EXECUTION_SUCCESS
        match_state: NO_MATCH_FOUND
      }
    }
  }
}
filter_results {
  key: "rai"
  value {
    rai_filter_result {
      execution_state: EXECUTION_SUCCESS
      match_state: NO_MATCH_FOUND
      rai_filter_type_results {
        key: "sexually_explicit"
        value {
          match_state: NO_MATCH_FOUND
        }
      }
      rai_filter_type_results {
        key: "hate_speech"
        value {
          match_state: NO_MATCH_FOUND
        }
      }
      rai_filter_type_results {
        key: "harassment"
        value {
          match_state: NO_MATCH_FOUND
        }
      }
      rai_filter_type_results {
        key: "dangerous"
        value {
          match_state: NO_MATCH_FOUND
        }
      }
    }
  }
}
filter_results {
  key: "pi_and_jailbreak"
  value {
    pi_and_jailbreak_filter_result {
      execution_state: EXECUTION_SUCCESS
      match_state: MATCH_FOUND
      confidence_level: MEDIUM_AND_ABOVE
    }
  }
}
filter_results {
  key: "malicious_uris"
  value {
    malicious_uri_filter_result {
      execution_state: EXECUTION_SUCCESS
      match_state: NO_MATCH_FOUND
    }
  }
}
filter_results {
  key: "csam"
  value {
    csam_filter_filter_result {
      execution_state: EXECUTION_SUCCESS
      match_state: NO_MATCH_FOUND
    }
  }
}
sanitization_metadata {
  error_code: 799
  error_message: "Unfortunately I cannot process that question, please refine your request and avoid any explicit content."
}
invocation_result: SUCCESS
```

### Floor Settings

**Floor settings** provide a mechanism for Security Architects and CISOs to control the minimum security requirements for all Model Armor templates within a Google Cloud resource hierarchy (organization, folder, or project). They define rules that dictate the minimum requirements for templates created at a specific level, preventing individual developers from lowering security standards. Project-level settings override folder-level settings in case of conflicts.

For example, a folder might enforce malicious URL filtering, while a project within it requires prompt injection and jailbreak detection with medium confidence. Templates in that project will enforce the project policy. **Violations of floor settings trigger security findings in Security Command Center (Premium or Enterprise tier)**, highlighting non-compliant pre-existing templates.

Floor settings can be enabled and updated using the gcloud command as show below, specifying the enforcement status and confidence levels for different filters at the project, folder, or organization level. Model Armor detects high-severity security violations when templates don’t meet these minimum floor settings, triggering alerts in Security Command Center.

```c
gcloud model-armor floorsettings update \
      --malicious-uri-filter-settings-enforcement=ENABLED \
      --pi-and-jailbreak-filter-settings-enforcement=DISABLED \
      --pi-and-jailbreak-filter-settings-confidence-level=LOW_AND_ABOVE \
      --basic-config-filter-enforcement=ENABLED \
      --add-rai-settings-filters='[{"confidenceLevel": "low_and_above", "filterType": "HARASSMENT"}, {"confidenceLevel": "high", "filterType": "SEXUALLY_EXPLICIT"}]'
      --full-uri='folders/FOLDER_ID/locations/global/floorSetting' \
      --enable-floor-setting-enforcement=true
```

An example, below, shows the source\_properties field of a finding when a floor setting violation occurs.

```c
{
  "filterConfig": {
    "raiSettings": {
      "raiFilters": [
        {
          "filterType": "HATE_SPEECH",
          "confidenceLevel": {
            "floorSettings": "LOW_AND_ABOVE",
            "template": "MEDIUM_AND_ABOVE"
          }
        },
        {
          "filterType": "HARASSMENT",
          "confidenceLevel": {
            "floorSettings": "MEDIUM_AND_ABOVE",
            "template": "HIGH"
          }
        }
      ]
    },
    "piAndJailbreakFilterSettings": {
      "confidenceLevel": {
        "floorSettings": "LOW_AND_ABOVE",
        "template": "HIGH"
      }
    },
    "maliciousUriFilterSettings": {
      "floorSettings": "ENABLED",
      "template": "DISABLED"
    }
  }
}
```

## Logging and Auditing

Model Armor is an **auditable resource in GCP**, with all actions logged to Cloud Logging. Entries can be filtered using *protoPayload.serviceName=”modelarmor.googleapis.com”*.

## Conclusion

In closing, with the increasing power of LLMs and Agentic AI necessitates a commitment to security, safety, and responsible implementation. Leveraging tools like Model Armor is important, but a foundation of ethical principles is critical for securing your workloads. Here are some guiding principles to help:

- **Secure Input Handling:** Always implement strong input filtering (with support from Model Armor) to block harmful characters and code. Employ regular expressions and NLP techniques to detect and neutralize adversarial prompts. Use input validation libraries to enforce data type and format constraints.
- **Control Output and Behavior:** Establish systems to monitor agent actions and outputs. Implement rule-based or machine learning-based anomaly detection to identify unusual behavior. Filter outputs to block potentially harmful or sensitive information (leveraging tools like Model Armor). Provide a “kill switch” for human intervention.
- **Strengthen Model Resilience:** Train models on diverse and robust datasets to improve resilience to attacks. Use adversarial training to expose and mitigate vulnerabilities. Apply techniques like differential privacy to protect against model extraction. Utilize prompt hardening and prompt engineering (where Model Armor can assist) to counter prompt injection.
- **Monitor Runtime Activity:** Continuously monitor resource usage, network activity, and behavior patterns. Use machine learning models to detect anomalies and trigger alerts. Implement logging and auditing mechanisms.
- **Enhance Transparency:** Employ techniques like LIME or SHAP to explain decision-making. Visualize internal states and activations. Implement methods to trace reasoning to input data.
- **Enforce Policies and Safeguards:** Define clear rules and constraints for agent actions. Use formal verification to ensure adherence. Implement a policy engine for access control and data privacy. Employ techniques like Reinforcement Learning from Human Feedback (RLHF) to align behavior with human values.
- **Incorporate Feedback and Learning:** Create systems for human feedback. Use reinforcement learning to encourage safe behaviors and discourage unsafe ones. Enable agents to learn from experience and improve safety.

Future research directions include developing more effective adversarial training, robust anomaly detection, improved explainability, and ethical guidelines for Agentic AI. Prioritizing security and safety is crucial for ensuring that these powerful technologies benefit society while mitigating potential risks.