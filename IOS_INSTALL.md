iOS Install / Build Guide for FieldTracker Mobile (Expo)

Prerequisites
- macOS with Xcode installed (for Simulator or native builds).
- Node.js (>=18) and npm or yarn.
- An Apple Developer account (required for App Store / TestFlight / device distribution).
- Expo CLI / EAS CLI installed globally if you plan to build packages:
  - npm install -g expo-cli
  - npm install -g eas-cli

Quick: Run in iOS Simulator (local dev)
1. Open a terminal in the `mobile` folder:
   ```bash
   cd mobile
   npm install
   npm run ios
   ```
2. This will open Expo dev tools and launch the iOS Simulator (requires Xcode).

Run on a physical device (Expo Go)
1. Install Expo Go from the App Store on the iOS device.
2. In the `mobile` folder run:
   ```bash
   npm install
   npm start
   ```
3. Scan the QR code from Expo dev tools (or open the project URL inside Expo Go) to load the app.

Create a standalone iOS build (.ipa) using EAS (recommended)
1. Configure EAS in the `mobile` folder:
   ```bash
   cd mobile
   eas login
   eas init
   ```
   - Choose the managed workflow (Expo) when prompted.
2. Create an `eas.json` with profiles (example):
   ```json
   {
     "build": {
       "production": { "workflow": "managed", "ios": { "simulator": false } },
       "development": { "workflow": "managed", "developmentClient": true }
     }
   }
   ```
3. Build for iOS (production):
   ```bash
   eas build -p ios --profile production
   ```
   - Follow prompts to connect your Apple Developer account and provide credentials/certificates. EAS can manage credentials for you.
4. When the build completes, download the resulting `.ipa` from the EAS build page.

Upload to TestFlight / App Store
- Use `eas submit -p ios` or Apple Transporter (or Xcode Organizer) to upload the `.ipa` to App Store Connect.
- From App Store Connect, create a TestFlight build and invite testers.

Ad-hoc / Enterprise distribution
- Use appropriate provisioning profiles and certificates in App Store Connect or via EAS credential management.

Troubleshooting & Notes
- To use native modules not supported by the managed Expo workflow, run `expo eject` (converts to bare React Native). That requires Xcode project work.
- EAS builds run in the cloud; for local native builds use Xcode: open the iOS project in Xcode and build/archive.
- Keep `app.json` / `app.config.js` updated with bundle identifier (e.g., com.yourorg.fieldtracker) and version.

Helpful commands summary
```bash
# Start dev server
cd mobile
npm install
npm start

# Run in iOS simulator
npm run ios

# EAS cloud build (production)
eas login
eas build -p ios --profile production

# Submit to App Store Connect via EAS
eas submit -p ios --latest
```

If you want, I can:
- Add an `eas.json` template to the `mobile` folder.
- Create an `app.json` sample with a recommended `bundleIdentifier`.
- Walk you through creating the Apple Developer credentials and connecting EAS.
