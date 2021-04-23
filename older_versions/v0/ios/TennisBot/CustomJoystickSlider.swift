//
//  CustomJoystickSlider.swift
//  TennisBot
//
//  Created by Sujay Garlanka on 10/15/20.
//  Copyright © 2020 TennisBot. All rights reserved.
//

import Foundation
import UIKit

class CustomJoystickSlider: UISlider {
    override func trackRect(forBounds bounds: CGRect) -> CGRect {
        let point = CGPoint(x: bounds.minX, y: bounds.midY)
        return CGRect(origin: point, size: CGSize(width: bounds.width, height: 30))
    }
}
