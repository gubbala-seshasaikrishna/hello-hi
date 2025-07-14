import Foundation
#if canImport(MLCLLM)
import MLCLLM
#endif

/// Singleton responsible for loading the model and generating responses.
@MainActor
final class ModelRunner: ObservableObject {
    static let shared = ModelRunner()

    #if canImport(MLCLLM)
    private var chatModel: ChatModule? // Replace with actual type from MLCLLM
    #endif

    private init() {
        loadModelIfNeeded()
    }

    private func loadModelIfNeeded() {
        #if canImport(MLCLLM)
        guard chatModel == nil else { return }
        if let url = Bundle.main.url(forResource: "llama1b-chat", withExtension: nil) {
            do {
                // NOTE: Replace `ChatModule` init with the correct call once MLCLLM is available.
                self.chatModel = try ChatModule(contentsOf: url)
            } catch {
                assertionFailure("Failed to load model: \(error)")
            }
        } else {
            assertionFailure("Model bundle not found")
        }
        #endif
    }

    /// Returns an async stream of token deltas for the given prompt.
    /// This thin wrapper hides MLCLLM specifics from the UI layer.
    func stream(prompt: String) -> AsyncThrowingStream<String, Error> {
        return AsyncThrowingStream { continuation in
            #if canImport(MLCLLM)
            guard let chatModel else {
                continuation.finish(throwing: NSError(domain: "Model not loaded", code: -1))
                return
            }

            Task {
                do {
                    for try await token in chatModel.generateTokens(prompt: prompt) {
                        continuation.yield(token)
                    }
                    continuation.finish()
                } catch {
                    continuation.finish(throwing: error)
                }
            }
            #else
            // Placeholder implementation for environments without MLCLLM.
            // Echos back the prompt with a delay.
            Task {
                for word in ("Echo: " + prompt).split(separator: " ") {
                    try? await Task.sleep(for: .milliseconds(150))
                    continuation.yield(String(word) + " ")
                }
                continuation.finish()
            }
            #endif
        }
    }
}