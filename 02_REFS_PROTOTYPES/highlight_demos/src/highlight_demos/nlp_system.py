# Advanced NLP System with Fine-Tuning and Domain Adaptation

import torch
import numpy as np
import pandas as pd
# Transformers and PEFT imports are largely for the Hugging Face-based model handling.
# With Ollama, these might be less central for basic inference, but kept for now
# if other functionalities of this class are to be preserved and adapted.
from transformers import (
    AutoTokenizer, # Still potentially useful for text processing, even with Ollama
    Trainer, TrainingArguments, DataCollatorForLanguageModeling # For fine-tuning, needs adaptation for Ollama
)
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
# PEFT/LoRA is specific to Hugging Face model modification. 
# If fine-tuning via Ollama or for models used in Ollama, the approach would differ.
# from peft import (
#     LoraConfig,
#     get_peft_model,
#     prepare_model_for_kbit_training,
#     TaskType
# )
import logging
import os
from typing import Dict, List, Optional, Tuple, Union
import json
from tqdm import tqdm
import re # Added for improved JSON parsing

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DomainSpecificNLP:
    """
    Advanced NLP system with domain adaptation capabilities
    for specialized knowledge domains.
    """

    def __init__(
        self,
        base_model_name: str = "google/gemma-3-4b-it", # Default to Gemma 3 (4B instruction-tuned)
        domain: str = "knowledge_management",
        device: str = None,
        quantization: str = None, # Default to no quantization for CPU
        lora_config: Optional[Dict] = None
    ):
        self.base_model_name = base_model_name # This will now be the Ollama model name, e.g., "gemma3:latest"
        self.domain = domain
        # Device and quantization are handled by Ollama server, so these are less relevant here for inference.
        # They might be relevant if this class were to manage Ollama model pulling/configuration.
        self.device = device 
        self.quantization = quantization 

        # LoRA config is specific to HuggingFace PEFT. Not directly applicable to Ollama client-side.
        # Fine-tuning would happen before loading into Ollama, or via Ollama's own mechanisms if any.
        self.lora_config = lora_config # Kept for now, but its application is removed from init.

        logger.info(f"DomainSpecificNLP initialized for Ollama model: {self.base_model_name}")
        logger.info("Note: Model loading, PEFT/LoRA are now primarily handled by Ollama server and api.py.")
        
        # Tokenizer might still be useful for other text processing tasks, independent of Ollama model loading
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name if not ":" in self.base_model_name else "google/gemma-3-4b-it", trust_remote_code=True) # Fallback for tokenizer if ollama name not on hf
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            logger.info("Tokenizer initialized (may be used for pre/post-processing).")
        except Exception as e:
            logger.warning(f"Could not initialize tokenizer for {self.base_model_name}: {e}. Some functionalities might be limited.")
            self.tokenizer = None
        
        self.model = None # Model object is not held by this class when using Ollama client.

        # Domain-specific templates and configurations
        self._load_domain_config()

    # _initialize_model_and_tokenizer is removed as Ollama handles model serving.
    # The tokenizer initialization is moved to __init__ if needed for other tasks.

    def _load_domain_config(self):
        """Load domain-specific configurations and templates."""
        self.domain_configs = {
            "knowledge_management": {
                "prompt_template": "<s>[INST] You are a knowledge management expert.\nYour task is to analyze, organize, and extract insights from the following information:\n\n{input}\n\n{instruction} [/INST]",
                "entity_types": ["concept", "document", "source", "relation", "person", "organization"],
                "relation_types": ["contains", "references", "authored_by", "based_on", "contradicts", "supports"]
            },
            "software_development": {
                "prompt_template": "<s>[INST] You are a software development expert.\nAnalyze the following code or technical information:\n\n{input}\n\n{instruction} [/INST]",
                "entity_types": ["class", "method", "function", "module", "library", "framework", "pattern"],
                "relation_types": ["imports", "inherits_from", "calls", "implements", "uses", "depends_on"]
            }
        }
        self.current_config = self.domain_configs.get(
            self.domain,
            self.domain_configs["knowledge_management"]
        )
        logger.info(f"Loaded configuration for domain: {self.domain}")

    def fine_tune(
        self,
        training_data: Union[str, pd.DataFrame, List[Dict]],
        output_dir: str = "./domain_model",
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 4,
        gradient_accumulation_steps: int = 4,
        learning_rate: float = 3e-4,
        warmup_ratio: float = 0.03,
        evaluation_data: Optional[Union[str, pd.DataFrame, List[Dict]]] = None,
        save_steps: int = 100
    ):
        """Fine-tune the model on domain-specific data."""
        logger.info("Preparing training data for fine-tuning")
        train_dataset = self._prepare_dataset(training_data)
        eval_dataset = self._prepare_dataset(evaluation_data) if evaluation_data else None

        data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_ratio=warmup_ratio,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=10,
            save_steps=save_steps,
            save_total_limit=3,
            evaluation_strategy="steps" if eval_dataset else "no",
            eval_steps=save_steps if eval_dataset else None,
            load_best_model_at_end=True if eval_dataset else False,
            fp16=torch.cuda.is_available(), # Enable FP16 if CUDA is available
            report_to="tensorboard",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            compute_metrics=self._compute_metrics
        )

        logger.info("Starting fine-tuning process")
        trainer.train()
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        logger.info(f"Fine-tuned model saved to {output_dir}")
        return trainer

    def _prepare_dataset(self, data_source: Union[str, pd.DataFrame, List[Dict], None]) -> Optional[Dataset]:
        """Prepare dataset from various input formats."""
        if data_source is None:
            return None
        if isinstance(data_source, str):
            if data_source.endswith('.csv'):
                data = pd.read_csv(data_source)
            elif data_source.endswith('.json'):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {data_source}")
        elif isinstance(data_source, pd.DataFrame):
            data = data_source
        elif isinstance(data_source, list):
            data = pd.DataFrame(data_source) # Convert list of dicts to DataFrame
        else:
            raise ValueError("Unsupported data format")

        formatted_data = []
        for _, row in tqdm(data.iterrows(), total=len(data), desc="Processing data"):
            formatted_text = self.current_config["prompt_template"].format(
                input=row.get("input", ""),
                instruction=row.get("instruction", "")
            )
            tokenized = self.tokenizer(
                formatted_text,
                truncation=True,
                max_length=2048, # Consider making this configurable
                padding="max_length",
                return_tensors="pt"
            )
            formatted_data.append({
                "input_ids": tokenized["input_ids"][0],
                "attention_mask": tokenized["attention_mask"][0],
                "labels": tokenized["input_ids"][0].clone()
            })
        return Dataset.from_pandas(pd.DataFrame(formatted_data))

    def _compute_metrics(self, eval_pred):
        """Compute metrics for evaluation."""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=2)
        mask = labels != -100
        labels_filtered = labels[mask]
        predictions_filtered = predictions[mask]
        accuracy = accuracy_score(labels_filtered, predictions_filtered)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels_filtered,
            predictions_filtered,
            average='weighted',
            zero_division=0
        )
        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}

    def generate_response(self, input_text: str, instruction: str, **generation_kwargs) -> str:
        """Generate a response using the fine-tuned model."""
        formatted_text = self.current_config["prompt_template"].format(input=input_text, instruction=instruction)
        inputs = self.tokenizer(formatted_text, return_tensors="pt").to(self.device)
        default_params = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "num_beams": 1,
            "repetition_penalty": 1.1,
            "pad_token_id": self.tokenizer.eos_token_id
        }
        generation_params = {**default_params, **generation_kwargs}
        with torch.no_grad():
            output_ids = self.model.generate(**inputs, **generation_params)
        response = self.tokenizer.decode(output_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        # The prompt template includes "[/INST]", so we split after it to get the model's actual response.
        # This assumes the model's output will follow the prompt structure.
        response_parts = formatted_text.split("[/INST]")
        # If the model correctly appends to the prompt, the generated text is what we want.
        # The tokenizer.decode already skips special tokens and handles the generated part.
        # The original split logic might be too aggressive if the model doesn't include [/INST] in its output.
        # Let's refine this: the output from model.generate is only the new tokens if not passing full input back.
        # So, `response` should be the clean model output.
        # The prompt structure is `<s>[INST] ... {instruction} [/INST] {model_response}</s>`
        # The `response` variable after decode should be `{model_response}`.
        return response.strip()

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract domain-specific entities from text."""
        instruction = f"""Extract and list all entities from the text.
Focus on these entity types: {', '.join(self.current_config['entity_types'])}.
For each entity, provide: (1) The entity text (verbatim), (2) The entity type, (3) Any relevant attributes or properties as a dictionary.
Format your response strictly as a JSON list of objects. Each object must have 'text', 'type', and 'attributes' keys.
Example: [{{"text": "example entity", "type": "concept", "attributes": {{"source": "document A"}}}}]"""
        response_str = self.generate_response(text, instruction)
        logger.debug(f"Raw entity extraction response: {response_str}")
        try:
            json_match = re.search(r'(\[\s\S]*?\])', response_str, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                entities = json.loads(json_str)
                if not isinstance(entities, list):
                    logger.warning(f"Parsed JSON for entities is not a list: {entities}")
                    return []
                return entities
            else:
                logger.warning("Could not find a JSON list structure in response for entity extraction.")
                return []
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from entity extraction response: {e}. Response: {response_str}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred during entity JSON parsing: {e}")
            return []

    def extract_relations(self, text: str) -> List[Dict]:
        """Extract relations between entities in the text."""
        instruction = f"""Analyze the text and identify relationships between entities.
Focus on these relation types: {', '.join(self.current_config['relation_types'])}.
For each relation, provide: (1) Source entity text, (2) Target entity text, (3) Relation type, (4) Confidence score (0.0-1.0, estimate if not directly available).
Format your response strictly as a JSON list of objects. Each object must have 'source', 'target', 'type', and 'confidence' keys.
Example: [{{"source": "entity A", "target": "entity B", "type": "related_to", "confidence": 0.8}}]"""
        response_str = self.generate_response(text, instruction)
        logger.debug(f"Raw relation extraction response: {response_str}")
        try:
            json_match = re.search(r'(\[\s\S]*?\])', response_str, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                relations = json.loads(json_str)
                if not isinstance(relations, list):
                    logger.warning(f"Parsed JSON for relations is not a list: {relations}")
                    return []
                return relations
            else:
                logger.warning("Could not find a JSON list structure in response for relation extraction.")
                return []
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from relation extraction response: {e}. Response: {response_str}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred during relation JSON parsing: {e}")
            return []

    def summarize(self, text: str, max_length: int = 200) -> str:
        """Generate a concise summary of the text."""
        instruction = f"Summarize the main points from this text. Keep your summary under {max_length} words and focus on the key insights. Maintain the domain-specific terminology and concepts."
        return self.generate_response(text, instruction)

    def answer_question(self, context: str, question: str) -> str:
        """Answer a specific question based on the provided context."""
        instruction = f"Based on the provided information, answer the following question: Question: {question}. Provide a comprehensive answer using only the facts presented in the text."
        return self.generate_response(context, instruction)

    def generate_knowledge_graph(self, text: str) -> Dict:
        # This method's core logic is now handled by api.py using the Ollama client.
        # This class might still be used for formatting the prompt or post-processing,
        # but the direct LLM call is externalized.

        logger.info(f"Knowledge graph generation for text (first 50 chars): '{text[:50]}...' is now primarily handled by the Ollama client in api.py.")
        logger.info("This method can be used for pre/post-processing if needed, or be deprecated if all logic moves to api.py.")

        # If this method were to still be involved, it might prepare a prompt or structure data.
        # For now, it returns a placeholder or could raise a NotImplementedError if it's meant to be fully bypassed.
        # Example prompt preparation (if used by api.py):
        # instruction = "Generate a knowledge graph with nodes and edges from the input text. Format the output as a JSON object with 'nodes' and 'edges' keys."
        # prompt = self.current_config["prompt_template"].format(input=text, instruction=instruction)
        # return prompt # Or return a more structured request for api.py to use with Ollama

        # Placeholder response, as the actual generation is in api.py
        return {"nodes": [{"id":"placeholder_node","label":"Placeholder - Generation via Ollama in API"}], "edges":[]}

    def load_fine_tuned_model(self, model_path: str):
        """Load a previously fine-tuned model (adapter)."""
        logger.info(f"Loading fine-tuned PEFT adapter from {model_path}")
        # Re-initialize base model first with quantization, etc.
        self._initialize_model_and_tokenizer() # This sets up self.model as base PEFT model
        from peft import PeftModel
        self.model = PeftModel.from_pretrained(self.model, model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        logger.info("Fine-tuned PEFT model (adapter) loaded successfully onto base model.")

# Example Usage (Optional, for testing the class directly)
if __name__ == '__main__':
    # Create dummy data for testing
    sample_text_km = """
    Project Alpha is a new initiative focused on knowledge graphs.
    It uses advanced AI models, including LLMs, to process documents.
    Dr. Eva Smith leads the project, which is funded by FutureTech Corp.
    The main goal is to improve information retrieval and discovery.
    A key document, "KG_Fundamentals.pdf", outlines the core concepts.
    This document references several seminal papers in the field.
    """

    # Initialize for Knowledge Management
    # Ensure you have enough memory/GPU for Mixtral. For CPU testing, use a smaller model.
    # e.g., base_model_name="gpt2" and quantization=None
    try:
        nlp_km = DomainSpecificNLP(
            base_model_name="mistralai/Mixtral-8x7B-Instruct-v0.1", # or a smaller model for CPU
            domain="knowledge_management",
            quantization="4bit" # Requires bitsandbytes and accelerate. Set to None for CPU if issues.
        )

        print("\n--- Knowledge Management Domain ---")
        print("\nGenerating Knowledge Graph (KM):")
        graph_km = nlp_km.generate_knowledge_graph(sample_text_km)
        print(json.dumps(graph_km, indent=2))

        print("\nSummarizing (KM):")
        summary_km = nlp_km.summarize(sample_text_km)
        print(summary_km)

        print("\nAnswering Question (KM):")
        question_km = "Who leads Project Alpha?"
        answer_km = nlp_km.answer_question(sample_text_km, question_km)
        print(f"Q: {question_km}\nA: {answer_km}")

    except Exception as e:
        logger.error(f"Error during example usage: {e}")
        print(f"Example usage failed. This might be due to resource constraints (e.g., RAM/VRAM) or missing dependencies for the large model.")
        print("Consider using a smaller model like 'gpt2' and quantization=None for initial CPU testing.")