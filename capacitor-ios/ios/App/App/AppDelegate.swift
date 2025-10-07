import UIKit
import Capacitor
import AppTrackingTransparency
import AdSupport

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

        // Request App Tracking Transparency on first launch, after app becomes active momentarily
        if #available(iOS 14, *) {
            let status = ATTrackingManager.trackingAuthorizationStatus
            if status == .notDetermined {
                // Ensure we present after the app has a window; slight delay avoids presenting too early
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                    ATTrackingManager.requestTrackingAuthorization { newStatus in
                        print("[ATT] authorization status: \(newStatus.rawValue)")
                    }
                }
            } else {
                print("[ATT] existing authorization status: \(status.rawValue)")
            }
        }

        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, etc.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate.
    }

    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
        // Keep this call for Capacitor URL handling
        return ApplicationDelegateProxy.shared.application(app, open: url, options: options)
    }

    func application(_ application: UIApplication, continue userActivity: NSUserActivity, restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
        // Keep this call for Capacitor Universal Links
        return ApplicationDelegateProxy.shared.application(application, continue: userActivity, restorationHandler: restorationHandler)
    }
}
