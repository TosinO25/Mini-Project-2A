// Micro:bit Accelerometer Data Logger
// This script records accelerometer data to the micro:bit file system
// Data can be downloaded via USB and analyzed

// Setup
let recording = false
let startTime = 0

input.onButtonPressed(Button.A, function () {
    if (recording) {
        recording = false
        basic.showIcon(IconNames.No)
    } else {
        recording = true
        startTime = control.millis()
        basic.showIcon(IconNames.Yes)
    }
})

basic.forever(function () {
    if (recording) {
        let timestamp = control.millis() - startTime
        let x = input.acceleration(Dimension.X)
        let y = input.acceleration(Dimension.Y)
        let z = input.acceleration(Dimension.Z)
        
        // Send data via serial
        serial.writeString(timestamp + "," + x + "," + y + "," + z + "\n")
        
        basic.showLeds(`
            # # # # #
            # . . . #
            # . # . #
            # . . . #
            # # # # #
            `)
        basic.pause(50)  // Sample every 50ms = 20Hz
    } else {
        basic.pause(100)
    }
})

// Alternative: Data logging to device
// Uncomment this section if your micro:bit supports data logging
/*
input.onButtonPressed(Button.B, function () {
    datalogger.setColumnTitles("time,x,y,z")
    for (let i = 0; i < 400; i++) {
        datalogger.log(datalogger.createCV("time", control.millis()),
                       datalogger.createCV("x", input.acceleration(Dimension.X)),
                       datalogger.createCV("y", input.acceleration(Dimension.Y)),
                       datalogger.createCV("z", input.acceleration(Dimension.Z)))
        basic.pause(50)
    }
})
*/

// Note: This is a MakeCode JavaScript example
// To use: 
// 1. Go to https://makecode.microbit.org/
// 2. Create new project
// 3. Switch to JavaScript view
// 4. Paste this code
// 5. Download to your micro:bit
// 6. Press A button to start/stop recording
// 7. Data streams to serial port (read with Python script)
