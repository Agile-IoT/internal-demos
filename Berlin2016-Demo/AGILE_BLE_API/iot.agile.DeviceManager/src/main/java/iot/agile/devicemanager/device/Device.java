/*
 * Copyright 2016 Dagmawi Neway Mekuria <d.mekuria@create-net.org>.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package iot.agile.devicemanager.device;

import org.freedesktop.dbus.DBusInterface;

/**
 * @author dagi
 * 
 *         Agile Device Interface
 *
 */
public interface Device extends DBusInterface {

	/**
	 * 
	 * @return The unique device id on the gateway
	 */
	@org.freedesktop.DBus.Description("Unique device ID in the gateway")
	public String Id();

	/**
	 * 
	 * @return The device name
	 */
	@org.freedesktop.DBus.Description("Name of the device")
	public String Name();

	/**
	 * 
	 * @return Current Device status
	 */
	@org.freedesktop.DBus.Description("Current Device status")
	public String Status();

	/**
	 * 
	 * @return return User configuration storage (in terms of KeyValue)
	 */
	@org.freedesktop.DBus.Description("returns User configuration storage (in terms of KeyValue)")
	public String Configuration();

	/**
	 * 
	 * @return Profile is protocol specific information of the device
	 * 
	 */
	@org.freedesktop.DBus.Description("returns the profile of the device")
	public String Profile();

	/**
	 * 
	 * @return A UNIX time stamp to indicate the last data update received by
	 *         the device
	 */
	@org.freedesktop.DBus.Description("returns the last data update received by the device")
	public int LastUpdate();

	/**
	 * 
	 * @return the most recent update of a sensor or data stream Received
	 *         asynchronously from subscribe all
	 */
	@org.freedesktop.DBus.Description("returns the most recent update of a sensor")
	public String Data();

	/**
	 * 
	 * @return Device specific communication protocol instance Available to
	 *         access protocol specific methods and properties
	 */
	@org.freedesktop.DBus.Description("returns Device specific communication  protocol instance")
	public String Protocol();

	// Methods

	/**
	 * Setup connection and initialize BLE connection for the given device
	 * 
	 * TODO: Instead of deviceAddress this method should receive device profile,
	 * and retrieve the id and other properties from it
	 */
	@org.freedesktop.DBus.Description("Setup connection and initialize BLE connection for the given device")
	public boolean Connect();

	/**
	 * 
	 * Disconnect the BLE device
	 *
	 * TODO: Use device profile to disconnect the device
	 * 
	 * @param deviceAddress
	 */
	@org.freedesktop.DBus.Description("Safely disconnect the device from the BLE adapter")
	public boolean Disconnect();

	/**
	 * Execute an operation on the device
	 */
	@org.freedesktop.DBus.Description("Execute an operation on the device")
	public void Execute(String command);

	/**
	 * Read data from the device
	 */
	@org.freedesktop.DBus.Description("Read data from the device")
	public String Read(String sensorName);

	/**
	 * Write data on the device
	 */
	@org.freedesktop.DBus.Description("Write data on the device")
	public void Write();

	/**
	 * Enable subscription
	 */
	@org.freedesktop.DBus.Description("Enable subscription")
	public void Subscribe();

	public void DropBus();
}
