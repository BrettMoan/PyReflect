# PyReflect
Python Reflection for OSRS and Private Servers.

## About 

This is a port of https://github.com/Brandon-T/Reflection to Python.


## Current Goals

- [ ] Completely implement RemoteInput 
- [ ] Completely port Reflection include

---

## Usage/Setup

Download the correct RemoteInput dll from https://github.com/brandon-t/reflection/releases

The version of RemoteInput <u>must</u>:

* Match your operating system (Windows, Linux, Mac)
* Be the same bit version as python interpreter you will run code on (python 32-bit for 32-bit DLL)
* Match the same version of client you are trying to inject to (Default old school client is 32-bit)

You can than import RemoteInput and set up the connection to client:

```python
import RemoteInput

# Create instance of Remote Input
reflect = RemoteInput.RemoteInput()

# Inject EIOS 
reflect.EIOS_Inject()

# Get number of clients
client_count = reflect.EIOS_GetClients()

# Get first clients PID
client_pid = reflect.EIOS_GetClientPID(0)

# Pair the client and get the target or eiosptr
eios_ptr = reflect.EIOS_PairClient(client_pid)

# lose Focus
reflect.EIOS_LoseFocus(eios_ptr)

# Gain focus
reflect.EIOS_GainFocus(eios_ptr)

# get Dimensions of client
dimensions = reflect.EIOS_GetTargetDimensions(eios_ptr)

# get current mouse position
mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)

# hold down the ESC key
reflect.EIOS_HoldKey(eios_ptr, VK_ESC)

# release the ESC key
reflect.EIOS_ReleaseKey(eios_ptr, VK_ESC)

# Type `hello world` with 100 ms apart
reflect.EIOS_SendString(eios_ptr, "hello world", 100, 100)

# move mouse to x=470, y=290
reflect.EIOS_MoveMouse(eios_ptr, 470, 290)

# Instantly move move mouse to x=375 y=260 and click left mouse button
reflect.EIOS_HoldMouse(eios_ptr, 375, 260, VK_LBUTTON)

# Instantly move move mouse to x=375 y=260 and release left mouse button
reflect.EIOS_ReleaseMouse(eios_ptr, 375, 260, VK_LBUTTON)

# Release the client
reflect.EIOS_ReleaseTarget(eios_ptr)
```

