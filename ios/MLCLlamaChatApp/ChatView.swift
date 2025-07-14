import SwiftUI

struct ChatMessage: Identifiable {
    let id = UUID()
    var text: String
    var isUser: Bool
}

struct ChatView: View {
    @State private var messages: [ChatMessage] = []
    @State private var input: String = ""
    @StateObject private var modelRunner = ModelRunner.shared

    var body: some View {
        VStack {
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 12) {
                        ForEach(messages) { message in
                            messageBubble(for: message)
                        }
                    }
                    .padding()
                    .onChange(of: messages.count) { _ in
                        if let last = messages.last?.id {
                            withAnimation {
                                proxy.scrollTo(last, anchor: .bottom)
                            }
                        }
                    }
                }
            }

            HStack {
                TextField("Type a message…", text: $input)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(minHeight: 40)

                Button("Send") {
                    send()
                }
                .disabled(input.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            }
            .padding()
        }
    }

    @ViewBuilder
    private func messageBubble(for message: ChatMessage) -> some View {
        HStack {
            if message.isUser { Spacer() }
            Text(message.text)
                .padding()
                .background(message.isUser ? Color.accentColor : Color.gray.opacity(0.2))
                .foregroundColor(message.isUser ? Color.white : Color.primary)
                .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            if !message.isUser { Spacer() }
        }
        .id(message.id)
    }

    private func send() {
        let userPrompt = input.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !userPrompt.isEmpty else { return }

        let userMsg = ChatMessage(text: userPrompt, isUser: true)
        messages.append(userMsg)
        input = ""

        Task {
            // Streaming response
            do {
                var botText = ""
                for try await delta in modelRunner.stream(prompt: userPrompt) {
                    botText += delta
                    await MainActor.run {
                        if let last = messages.last, last.isUser {
                            messages.append(ChatMessage(text: botText, isUser: false))
                        } else {
                            messages[messages.count - 1].text = botText
                        }
                    }
                }
            } catch {
                await MainActor.run {
                    messages.append(ChatMessage(text: "⚠️ Error: \(error.localizedDescription)", isUser: false))
                }
            }
        }
    }
}