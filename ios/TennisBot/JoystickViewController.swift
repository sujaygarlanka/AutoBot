//
//  JoystickViewController.swift
//  TennisBot
//
//  Created by Sujay Garlanka on 10/15/20.
//  Copyright © 2020 TennisBot. All rights reserved.
//

import UIKit

class JoystickViewController: UIViewController {
    
    private var bluetoothConnection: Bluetooth!

    @IBOutlet var MoveSlider: UISlider! {
        didSet {
            MoveSlider.transform = CGAffineTransform(rotationAngle: CGFloat(-Double.pi / 2))
        }
    }
    
    
    @IBAction func MoveSlider(_ sender: UISlider) {
        var value = Int(sender.value)
        if (value >= -30  && value <= 30) {
            bluetoothConnection.sendCommand(command: Move.Stop, power: 0)
        }
        else if (value < -30){
            value = value * -1
            bluetoothConnection.sendCommand(command: Move.Reverse, power: UInt8(value))
        }
        else {
            bluetoothConnection.sendCommand(command: Move.Forward, power: UInt8(value))
        }
    }
    
    @IBAction func TurnSlider(_ sender: UISlider) {
        var value = Int(sender.value)
        if (value >= -30  && value <= 30) {
            bluetoothConnection.sendCommand(command: Move.Center, power: 0)
        }
        else if (value < -30){
            value = value * -1
            bluetoothConnection.sendCommand(command: Move.Left, power: UInt8(value))
        }
        else {
            bluetoothConnection.sendCommand(command: Move.Right, power: UInt8(value))
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        bluetoothConnection = Bluetooth()
        // Do any additional setup after loading the view.
    }
}

