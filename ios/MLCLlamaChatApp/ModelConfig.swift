import Foundation

/// Representation of the different chat templates supported by the app.
/// Extend as needed when adding additional models.
enum ChatTemplate: String, Codable {
    case llama3 // Uses the Hugging Face Llama 3 chat format
    // case yourNextTemplate

    /// Returns the system prompt prefix depending on template.
    func systemPromptPrefix() -> String {
        switch self {
        case .llama3:
            return "<|start_header_id|>system<|end_header_id|>\n"
        }
    }
}

/// Associates a local model folder with display metadata.
struct ModelConfig: Identifiable, Hashable, Codable {
    var id: String { displayName }

    /// File-URL pointing to the folder that contains `mod.json`, `params_*.bin`, tokenizer etc.
    var modelURL: URL

    /// Human-friendly name that shows up in the UI.
    var displayName: String

    /// The chat template used to wrap user prompts.
    var chatTemplate: ChatTemplate
}

/// Convenience helper to ship app with a pre-bundled model config list.
struct ModelRegistry {
    static let defaultModel = ModelConfig(
        modelURL: Bundle.main.url(forResource: "llama1b-chat", withExtension: nil)!,
        displayName: "Llama-3-1B",
        chatTemplate: .llama3
    )
}