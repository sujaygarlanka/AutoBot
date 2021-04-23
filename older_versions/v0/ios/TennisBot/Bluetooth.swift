//
//  Bluetooth.swift
//  TennisBot
//
//  Created by Sujay Garlanka on 10/15/20.
//  Copyright © 2020 TennisBot. All rights reserved.
//

import Foundation
import UIKit
import CoreBluetooth

class Bluetooth: NSObject, CBPeripheralDelegate, CBCentralManagerDelegate {
    
    // Properties
    private var centralManager: CBCentralManager!
    private var peripheral: CBPeripheral!
    /// UUID of the service to look for.
    private var serviceUUID = CBUUID(string: "FFE0")
    private var characteristicUUID = CBUUID(string: "FFE1")
    private var writeCharacteristic: CBCharacteristic?
    private var writeType: CBCharacteristicWriteType = .withoutResponse

    
    override init() {
       super.init()
       centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    
    // If we're powered on, start scanning
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        print("Central state update")
        if central.state != .poweredOn {
            print("Central is not powered on")
        } else {
            print("Central scanning for", serviceUUID);
            centralManager.scanForPeripherals(withServices: [serviceUUID],
                                              options: [CBCentralManagerScanOptionAllowDuplicatesKey : true])
        }
    }
    
    // Handles the result of the scan
     func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {

         // We've found it so stop scan
         self.centralManager.stopScan()

         // Copy the peripheral instance
         self.peripheral = peripheral
         self.peripheral.delegate = self

         // Connect!
         self.centralManager.connect(self.peripheral, options: nil)

     }
    
    // The handler if we do connect succesfully
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        if peripheral == self.peripheral {
            print("Connected to the car")
            peripheral.discoverServices([serviceUUID])
        }
    }
    
    // Handles discovery event
     func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if let services = peripheral.services{
             for service in services {
                if service.uuid == serviceUUID && peripheral.name! == "DSD TECH" {
                     print("Car found")
                     //Now kick off discovery of characteristics
                     peripheral.discoverCharacteristics([characteristicUUID], for: service)
                     return
                 }
             }
         }
     }
    
    // Handling discovery of characteristics
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        if let characteristics = service.characteristics {
            for characteristic in characteristics {
                if characteristic.uuid == characteristicUUID {
                    print("Car characteristic found")
                    writeCharacteristic = characteristic
                }
            }
        }
    }
    
    func sendCommand(command: Move, power: UInt8) {
        // Check if it has the write property
        var data = command.rawValue.data(using: .utf8)!
        data.append(power)
        sendData(withValue: data)
    }
    
    func sendData(withValue value: Data) {
        // Check if it has the write property
        if let unwrappedChar = writeCharacteristic, unwrappedChar.properties.contains(.writeWithoutResponse
            ), peripheral != nil {
            peripheral.writeValue(value, for: unwrappedChar, type: .withoutResponse)
        }
    }
    
}
