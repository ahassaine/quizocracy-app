import type { CapacitorConfig } from '@capacitor/cli';

// One codebase for Android and iOS: both load the live web app, so every web deploy
// reaches the apps without a store release.
const config: CapacitorConfig = {
  appId: 'com.quizocracy.app',
  appName: 'Quizocracy',
  webDir: 'www',
  server: {
    url: process.env.QZ_APP_URL || 'https://quizocracy.com',
    cleartext: !!process.env.QZ_APP_URL?.startsWith('http://'),
    androidScheme: 'https',
  },
  android: { allowMixedContent: false },
  ios: { contentInset: 'always', limitsNavigationsToAppBoundDomains: false },
  plugins: {
    SplashScreen: { launchShowDuration: 500, launchAutoHide: true, backgroundColor: '#F7F8FC', showSpinner: false },
    StatusBar: { style: 'DARK', backgroundColor: '#4F46E5', overlaysWebView: false },
  },
};

export default config;
