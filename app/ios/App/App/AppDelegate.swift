import UIKit
import Capacitor

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

  var window: UIWindow?
  var bridge: CAPBridgeViewController?

  func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    bridge = CAPBridgeViewController()
    window = UIWindow(frame: UIScreen.main.bounds)
    window?.rootViewController = bridge
    window?.makeKeyAndVisible()
    return true
  }
}