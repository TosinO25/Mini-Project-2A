"""
Micro:bit Accelerometer Data Logger
Collects accelerometer data from micro:bit via serial connection and saves to CSV.

Usage:
1. Flash the micro:bit with the MakeCode or Python script
2. Connect micro:bit to PC via USB
3. Run this script: python microbit_data_logger.py
4. Follow the prompts to record your data
"""

import serial
import csv
import time
from datetime import datetime
import os


class MicrobitDataLogger:
    """Collect and log accelerometer data from micro:bit"""
    
    def __init__(self, port=None, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.data = []
        
    def find_port(self):
        """Auto-detect micro:bit serial port"""
        import serial.tools.list_ports
        
        ports = serial.tools.list_ports.comports()
        microbit_ports = [p.device for p in ports if 'microbit' in p.description.lower()]
        
        if microbit_ports:
            return microbit_ports[0]
        
        # Fall back to common ports
        for port in ['COM3', 'COM4', 'COM5', '/dev/ttyUSB0', '/dev/ttyACM0']:
            try:
                ser = serial.Serial(port, self.baudrate, timeout=0.5)
                ser.close()
                return port
            except:
                pass
        
        return None
    
    def connect(self):
        """Establish serial connection to micro:bit"""
        if not self.port:
            self.port = self.find_port()
        
        if not self.port:
            print("Error: Could not find micro:bit")
            print("Make sure it's connected and drivers are installed")
            return False
        
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for connection
            print(f"Connected to micro:bit on {self.port}")
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False
    
    def read_data(self, duration=20, label='unlabeled'):
        """Read accelerometer data for a specified duration
        
        Parameters:
        - duration: seconds to record
        - label: data label (e.g., 'steady', 'shaking')
        """
        if not self.serial_connection:
            print("Not connected to micro:bit")
            return False
        
        print(f"\nRecording {label} for {duration} seconds...")
        print("Make sure data is being sent from micro:bit")
        
        start_time = time.time()
        sample_count = 0
        
        try:
            while time.time() - start_time < duration:
                if self.serial_connection.in_waiting:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    if line:
                        try:
                            # Parse data - adjust based on your micro:bit format
                            # Expected: "x,y,z" or "time,x,y,z"
                            values = [float(v) for v in line.split(',')]
                            
                            if len(values) == 3:
                                x, y, z = values
                                timestamp = time.time() - start_time
                            elif len(values) == 4:
                                timestamp, x, y, z = values
                            else:
                                continue
                            
                            self.data.append({
                                'timestamp': timestamp,
                                'accel_x': x,
                                'accel_y': y,
                                'accel_z': z,
                                'label': label
                            })
                            
                            sample_count += 1
                            if sample_count % 10 == 0:
                                print(f"  Samples collected: {sample_count}")
                        
                        except ValueError:
                            # Skip malformed lines
                            pass
                
                time.sleep(0.01)  # Small delay to avoid consuming all CPU
        
        except KeyboardInterrupt:
            print("\nRecording interrupted")
        
        print(f"Collected {sample_count} samples for {label}")
        return sample_count > 0
    
    def save_to_csv(self, filename=None):
        """Save collected data to CSV file"""
        if not self.data:
            print("No data to save")
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"accelerometer_data_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'accel_x', 'accel_y', 'accel_z', 'label'])
                writer.writeheader()
                writer.writerows(self.data)
            
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def close(self):
        """Close serial connection"""
        if self.serial_connection:
            self.serial_connection.close()
            print("Connection closed")


def main():
    """Main function for data collection workflow"""
    
    print("="*60)
    print("Micro:bit Accelerometer Data Logger")
    print("="*60)
    
    logger = MicrobitDataLogger()
    
    # Connect to micro:bit
    if not logger.connect():
        print("Failed to connect to micro:bit")
        print("Troubleshooting:")
        print("1. Check micro:bit is connected via USB")
        print("2. Install drivers: https://support.microbit.org/support/solutions/articles/19000013863")
        print("3. Check serial port settings")
        return
    
    # Recording sequence
    print("\n" + "="*60)
    print("Recording Sequence:")
    print("="*60)
    print("You will record: Steady (5s) -> Shake (5s) -> Steady (5s) -> Shake (5s)")
    print("Total: ~20 seconds")
    
    input("\nPress ENTER when ready to start recording...")
    
    # Sequence 1: Steady
    input("\nHold micro:bit steady. Press ENTER to start (5 seconds)...")
    logger.read_data(duration=5, label='steady')
    
    # Sequence 2: Shaking
    input("Shake micro:bit. Press ENTER to start (5 seconds)...")
    logger.read_data(duration=5, label='shaking')
    
    # Sequence 3: Steady
    input("Hold micro:bit steady. Press ENTER to start (5 seconds)...")
    logger.read_data(duration=5, label='steady')
    
    # Sequence 4: Shaking
    input("Shake micro:bit. Press ENTER to start (5 seconds)...")
    logger.read_data(duration=5, label='shaking')
    
    # Save data
    print("\n" + "="*60)
    logger.close()
    
    filename = input("Enter filename for saving (or press ENTER for auto): ").strip()
    logger.save_to_csv(filename if filename else None)
    
    print(f"\nTotal samples collected: {len(logger.data)}")
    print("Data ready for analysis!")


if __name__ == "__main__":
    main()
