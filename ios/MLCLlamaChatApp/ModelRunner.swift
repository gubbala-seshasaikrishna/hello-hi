import Foundation
#if canImport(MLCLLM)
import MLCLLM
#endif

/// Singleton responsible for loading the model and generating responses.
@MainActor
final class ModelRunner: ObservableObject {
    static let shared = ModelRunner()

    #if canImport(MLCLLM)
    /// Handle to the compiled chat pipeline provided by MLC-LLM.
    private var chatModel: ChatModule?
    #endif

    private init() {
        loadModelIfNeeded()
    }

    private func loadModelIfNeeded() {
        #if canImport(MLCLLM)
        guard chatModel == nil else { return }

        // Location of the model folder inside the app bundle. Must match the name in Xcode.
        guard let modelFolder = Bundle.main.url(forResource: "llama1b-chat", withExtension: nil) else {
            assertionFailure("Model folder ‘llama1b-chat’ missing from bundle")
            return
        }

        do {
            /*
             The ChatModule initializer expects explicit paths for the compiled artifacts.
             The exact signature may vary slightly between releases – adjust if necessary.
             */

            let module = try ChatModule(
                modelJSON: modelFolder.appendingPathComponent("mod.json").path,
                modelLib:  modelFolder.appendingPathComponent("mlc_lib.metallib").path,
                paramsPath: modelFolder.path, // folder containing params_shard*.bin
                tokenizerPath: modelFolder.appendingPathComponent("tokenizer.json").path,
                maxSeqLen: 4096,
                chatTemplate: .llama3 // enum from MLCLLM mirroring ours
            )

            self.chatModel = module
        } catch {
            assertionFailure("Failed to create ChatModule: \(error)")
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
                    for try await token in chatModel.streamChat(prompt: prompt) {
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