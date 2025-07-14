// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MLCLlamaChat",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .iOSApplication(
            name: "MLCLlamaChat",
            targets: ["AppModule"],
            bundleIdentifier: "com.example.MLCLlamaChat",
            teamIdentifier: "",
            displayVersion: "1.0",
            bundleVersion: "1",
            appCategory: .education,
            iconAssetName: "AppIcon",
            accentColorAssetName: "AccentColor",
            supportedDeviceFamilies: [
                .phone,
                .pad
            ],
            supportedInterfaceOrientations: [
                .portrait,
                .portraitUpsideDown,
                .landscapeLeft,
                .landscapeRight
            ]
        )
    ],
    dependencies: [
        // Add MLC LLM when SPM package is available
    ],
    targets: [
        .executableTarget(
            name: "AppModule",
            path: "MLCLlamaChatApp"
        )
    ]
)