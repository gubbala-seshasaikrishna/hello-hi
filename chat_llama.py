import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import gradio as gr

MODEL_ID = "unsloth/Llama-3.2-1B-bnb-4bit"

# -----------------------------------------------------------------------------
# Model & tokenizer loading
# -----------------------------------------------------------------------------
print("Loading model... This can take a few minutes on first run.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",          # sends layers to available GPU(s) if present, else CPU
    torch_dtype=torch.float16,   # 4-bit block-quantised weights still de-quantise to fp16 in kernels
)
model.eval()

# -----------------------------------------------------------------------------
# Generation helper
# -----------------------------------------------------------------------------

def generate_response(message: str, chat_history: list) -> tuple[str, list]:
    """Generate a model response and update the chat history.

    Parameters
    ----------
    message : str
        The newest user message.
    chat_history : list
        List of [user, assistant] message pairs.

    Returns
    -------
    tuple[str, list]
        A tuple of the (cleared textbox value, updated chat history).
    """
    # Build the full conversation in Llama-3 style chat template.
    history_plus_new = chat_history + [["user", message]]
    prompt = tokenizer.apply_chat_template(
        history_plus_new,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Only take the newly generated tokens
    generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    chat_history.append([message, response])
    return "", chat_history


# -----------------------------------------------------------------------------
# Gradio UI
# -----------------------------------------------------------------------------

def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Llama-3.2-1B Chatbot") as demo:
        gr.Markdown("""# 🤖 Llama-3.2-1B Chatbot\nChat with a quantised Llama-3 model running locally.""")

        chatbot = gr.Chatbot([], elem_id="chatbot").style(height=450)
        msg_box = gr.Textbox(placeholder="Type your message and press Enter", show_label=False)
        clear_btn = gr.Button("🗑️ Clear chat")

        msg_box.submit(generate_response, [msg_box, chatbot], [msg_box, chatbot])
        clear_btn.click(lambda: [], None, chatbot, queue=False)

    return demo


def main():
    demo = build_demo()
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))


if __name__ == "__main__":
    main()