import Foundation
import Capacitor

@objc(ATTPlugin)
public class ATTPlugin: CAPPlugin {

    @objc func request(_ call: CAPPluginCall) {
        ATTRequester.request { status in
            self.bridge?.triggerJSEvent("attStatus", target: "window", data: "{\"status\": \(status)}")
            call.resolve(["status": status]) // 0: notDetermined, 1: restricted, 2: denied, 3: authorized
        }
    }

    @objc func status(_ call: CAPPluginCall) {
        if #available(iOS 14, *) {
            let raw = ATTrackingManager.trackingAuthorizationStatus.rawValue
            call.resolve(["status": raw])
        } else { call.resolve(["status": 3]) }
    }
}