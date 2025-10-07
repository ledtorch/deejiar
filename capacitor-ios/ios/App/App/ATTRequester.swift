import Foundation
import AppTrackingTransparency
import AdSupport

@objc public class ATTRequester: NSObject {
    @objc public static func request(completion: @escaping (Int) -> Void) {
        if #available(iOS 14, *) {
            // If user has already chosen, return immediately
            let status = ATTrackingManager.trackingAuthorizationStatus
            guard status == .notDetermined else {
                completion(status.rawValue)
                return
            }
            // Ask for permission
            ATTrackingManager.requestTrackingAuthorization { newStatus in
                completion(newStatus.rawValue)
            }
        } else {
            completion(3) // authorized for < iOS 14 metaphorically
        }
    }
}