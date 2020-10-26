"""
WIP: A Python wrapper for Brandons RemoteInput/Reflection for OSRS 

Resources:
    Definitions of functions from headers: https://gist.github.com/Brandon-T/530ffc8780920dc12919af8d15ebac3f
    Hex code constants: https://gist.github.com/kkusch/245bb80ec4e7ab4d8cdc6b7eeb3f330f#file-hex_keycodes-py
    ctypes: https://docs.python.org/3/library/ctypes.html

Working: (tested with vanilla client)
    [x] EIOS_GainFocus
    [x] EIOS_GetClientPID
    [x] EIOS_GetClients
    [x] EIOS_GetMousePosition
    [x] EIOS_GetRealMousePosition
    [x] EIOS_GetTargetDimensions
    [x] EIOS_HasFocus
    [x] EIOS_HoldKey
    [x] EIOS_HoldMouse
    [x] EIOS_Inject
    [x] EIOS_LoseFocus
    [x] EIOS_MoveMouse
    [x] EIOS_PairClient
    [x] EIOS_ReleaseKey
    [x] EIOS_ReleaseMouse
    [x] EIOS_ReleaseTarget
    [x] EIOS_SendString

TODO:
    [ ] ask brandon if theres a better around the "ValueError: Procedure probably called with too many arguments (4 bytes in excess)"  
            exception when calling EIOS_Inject, other than loading the dll with CDLL('./libremoteinput.dll') for that one call.

    [ ] Functions that still need tested:
        [ ] EIOS_GetImageBuffer 
        [ ] EIOS_GetDebugImageBuffer 
        [ ] EIOS_SetGraphicsDebugging 
        [ ] EIOS_UpdateImageBuffer 
        [ ] EIOS_ScrollMouse 
        [ ] EIOS_IsMouseButtonHeld 
        [ ] EIOS_IsKeyHeld
        [ ] EIOS_GetKeyboardSpeed
        [ ] EIOS_SetKeyboardSpeed
        [ ] EIOS_GetKeyboardRepeatDelay
        [ ] EIOS_SetKeyboardRepeatDelay
        [ ] EIOS_KillClientPID
        [ ] EIOS_KillClient
        [ ] EIOS_KillZombieClients
        [ ] Reflect_GetEIOS
    
    [ ] Functions that still need written:
        [ ] Reflect_Object
        [ ] Reflect_IsSame_Object
        [ ] Reflect_InstanceOf
        [ ] Reflect_Release_Object
        [ ] Reflect_Release_Objects
        [ ] Reflect_Bool
        [ ] Reflect_Char
        [ ] Reflect_Byte
        [ ] Reflect_Short
        [ ] Reflect_Int
        [ ] Reflect_Long
        [ ] Reflect_Float
        [ ] Reflect_Double
        [ ] Reflect_String
        [ ] Reflect_Array
        [ ] Reflect_Array_With_Size
        [ ] Reflect_Array_Size
        [ ] Reflect_Array_Index
        [ ] Reflect_Array_Index2D
        [ ] Reflect_Array_Index3D
        [ ] Reflect_Array_Index4D
        [ ] Reflect_Array_Indices

    [x] EIOS_MoveMouse seems broken, after calling it once, the next call to EIOS_GetMousePosition is really high
        RESOLVED: was using pointer, for something that shouldn't be a pointer :/

    [x] not sure how to properly capture the bool from EIOS_HasFocus. always getting c_bool(True)
        RESOLVED: had to set `.restype` to a bool
"""
from ctypes import *
import getpass
import platform
import time
from typing import Tuple

from hex_keycodes import *


class RemoteInput:
    """
    This class allows for python to access RemoteInput
    """

    def __init__(self):
        if platform.system() == "Windows":
            self.ri = WinDLL("./libremoteinput.dll")
            self.cri = CDLL(
                "./libremoteinput.dll"
            )  # needed for EIOS_Inject, otherwise get
        elif platform.system() == "Dawrin":
            self.cri = self.ri = CDLL("./libremoteinput.dylib")
        else:
            self.cri = self.ri = CDLL(".libremoteinput.so")

    ## EIOS
    def EIOS_RequestTarget(self, initstr: str) -> c_void_p:
        """
        EIOS* EIOS_RequestTarget(const char* initargs) noexcept;
        """
        self.ri.EIOS_RequestTarget.argtypes = [c_char_p]
        self.ri.EIOS_RequestTarget.restype = c_void_p
        return self.EIOS_RequestTarget(bytes(initstr, encoding="utf8"))

    def EIOS_ReleaseTarget(self, target: c_void_p) -> None:
        """
        void EIOS_ReleaseTarget(EIOS* eios) noexcept;
        """
        self.ri.EIOS_ReleaseTarget.argtypes = [c_void_p]
        self.ri.EIOS_ReleaseTarget.restype = None
        self.ri.EIOS_ReleaseTarget(target)

    def EIOS_GetTargetDimensions(self, target: c_void_p):
        """
        void EIOS_GetTargetDimensions(EIOS* eios, std::int32_t* width, std::int32_t* height) noexcept;
        :return: width, height
        """
        width = c_int32()
        height = c_int32()
        self.ri.EIOS_GetTargetDimensions.argtypes = [
            c_void_p,
            POINTER(c_int32),
            POINTER(c_int32),
        ]
        self.ri.EIOS_GetTargetDimensions.restype = None
        self.ri.EIOS_GetTargetDimensions(target, byref(width), byref(height))
        return [width.value, height.value]

    def EIOS_GetImageBuffer(self, target: c_void_p):
        """
        std::uint8_t* EIOS_GetImageBuffer(EIOS* eios) noexcept;
        """
        self.ri.EIOS_GetImageBuffer.argtypes = [c_void_p]
        self.ri.EIOS_GetImageBuffer.restype = POINTER(c_uint8)
        buffer = self.ri.EIOS_GetImageBuffer(target)
        return buffer.contents
        # return cast(buffer, POINTER(c_uint8)).contents

    def EIOS_GetDebugImageBuffer(self, target: c_void_p):
        """
        std::uint8_t* EIOS_GetDebugImageBuffer(EIOS* eios) noexcept;
        """
        self.ri.EIOS_GetDebugImageBuffer.argtypes = [c_void_p]
        self.ri.EIOS_GetDebugImageBuffer.restype = POINTER(c_uint8)
        buffer = self.ri.EIOS_GetDebugImageBuffer(target)
        return buffer.contents
        # return cast(buffer, POINTER(c_uint8)).contents

    def EIOS_SetGraphicsDebugging(self, target: c_void_p, enabled: bool):
        """
        void EIOS_SetGraphicsDebugging(EIOS* eios, bool enabled) noexcept;
        """
        self.ri.EIOS_SetGraphicsDebugging.argtypes = [c_void_p, c_bool]
        self.ri.EIOS_SetGraphicsDebugging.restype = None
        self.ri.EIOS_SetGraphicsDebugging(target, enabled)

    def EIOS_UpdateImageBuffer(self, target: c_void_p) -> None:
        """
        void EIOS_UpdateImageBuffer(EIOS* eios) noexcept;
        """
        self.ri.EIOS_UpdateImageBuffer.argtypes = [c_void_p]
        self.ri.EIOS_UpdateImageBuffer.restype = None
        self.ri.EIOS_UpdateImageBuffer(target)

    def EIOS_HasFocus(self, target: c_void_p) -> bool:
        """
        bool EIOS_HasFocus(EIOS* eios) noexcept;
        """
        self.ri.EIOS_HasFocus.argtypes = [c_void_p]
        self.ri.EIOS_HasFocus.restype = c_bool
        return self.ri.EIOS_HasFocus(target)

    def EIOS_GainFocus(self, target: c_void_p) -> None:
        """
        void EIOS_GainFocus(EIOS* eios) noexcept;
        """
        self.ri.EIOS_GainFocus.argtypes = [c_void_p]
        self.ri.EIOS_GainFocus.restype = None
        self.ri.EIOS_GainFocus(target)

    def EIOS_LoseFocus(self, target: c_void_p) -> None:
        """
        void EIOS_LoseFocus(EIOS* eios) noexcept;
        """
        self.ri.EIOS_LoseFocus.argtypes = [c_void_p]
        self.ri.EIOS_LoseFocus.restype = None
        self.ri.EIOS_LoseFocus(target)

    def EIOS_IsInputEnabled(self, target: c_void_p) -> bool:
        """
        bool EIOS_IsInputEnabled(EIOS* eios) noexcept;
        """
        self.ri.EIOS_IsInputEnabled.argtypes = [c_void_p]
        self.ri.EIOS_IsInputEnabled.restype = c_bool
        return self.ri.EIOS_IsInputEnabled(target)

    def EIOS_SetInputEnabled(self, target: c_void_p, enabled: bool) -> None:
        """
        void EIOS_SetInputEnabled(EIOS* eios, bool enabled) noexcept;
        """
        self.ri.EIOS_SetInputEnabled.argtypes = [c_void_p, c_bool]
        self.ri.EIOS_SetInputEnabled.restype = None
        self.ri.EIOS_SetInputEnabled(target, enabled)

    def EIOS_GetMousePosition(self, target: c_void_p) -> Tuple[int, int]:
        """
        void EIOS_GetMousePosition(EIOS* eios, std::int32_t* x, std::int32_t* y) noexcept;

        :param target: The EIOS target
        type target: EIOS

        :return: x, y
        """
        x = c_int32()
        y = c_int32()
        self.ri.EIOS_GetMousePosition.argtypes = [
            c_void_p,
            POINTER(c_int32),
            POINTER(c_int32),
        ]
        self.ri.EIOS_GetMousePosition.restype = None
        self.ri.EIOS_GetMousePosition(target, byref(x), byref(y))
        return (x.value, y.value)

    def EIOS_GetRealMousePosition(self, target: c_void_p) -> Tuple[int, int]:
        """
        void EIOS_GetRealMousePosition(EIOS* eios, std::int32_t* x, std::int32_t* y) noexcept;

        :param target: The EIOS target
        type target: EIOS

        :return: x, y
        """
        x = c_int32()
        y = c_int32()
        self.ri.EIOS_GetRealMousePosition.argtypes = [
            c_void_p,
            POINTER(c_int32),
            POINTER(c_int32),
        ]
        self.ri.EIOS_GetRealMousePosition.restype = None
        self.ri.EIOS_GetRealMousePosition(target, byref(x), byref(y))
        return (x.value, y.value)

    def EIOS_MoveMouse(self, target: c_void_p, x: int, y: int) -> None:
        """
        void EIOS_MoveMouse(EIOS* eios, std::int32_t x, std::int32_t y) noexcept;
        """
        self.ri.EIOS_MoveMouse.argtypes = [c_void_p, c_int32, c_int32]
        self.ri.EIOS_MoveMouse.restype = None
        self.ri.EIOS_MoveMouse(target, x, y)

    def EIOS_HoldMouse(self, target: c_void_p, x: int, y: int, button: int) -> None:
        """
        void EIOS_HoldMouse(EIOS* eios, std::int32_t x, std::int32_t y, std::int32_t button) noexcept;
        """
        self.ri.EIOS_HoldMouse.argtypes = [c_void_p, c_int32, c_int32, c_int32]
        self.ri.EIOS_HoldMouse.restype = None
        self.ri.EIOS_HoldMouse(target, x, y, button)

    def EIOS_ReleaseMouse(self, target: c_void_p, x: int, y: int, button: int) -> None:
        """
        void EIOS_ReleaseMouse(EIOS* eios, std::int32_t x, std::int32_t y, std::int32_t button) noexcept;
        """
        self.ri.EIOS_ReleaseMouse.argtypes = [c_void_p, c_int32, c_int32, c_int32]
        self.ri.EIOS_ReleaseMouse.restype = None
        self.ri.EIOS_ReleaseMouse(target, x, y, button)

    def EIOS_ScrollMouse(self, target: c_void_p, x: int, y: int, lines: int) -> None:
        """
        void EIOS_ScrollMouse(EIOS* eios, std::int32_t x, std::int32_t y, std::int32_t lines) noexcept;
        """
        self.ri.EIOS_ScrollMouse.argtypes = [c_void_p, c_int32, c_int32, c_int32]
        self.ri.EIOS_ScrollMouse.restype = None
        self.ri.EIOS_ScrollMouse(target, x, y, lines)

    def EIOS_IsMouseButtonHeld(self, target: c_void_p, button: int) -> bool:
        """
        bool EIOS_IsMouseButtonHeld(EIOS* eios, std::int32_t button) noexcept;
        """
        self.ri.EIOS_IsMouseButtonHeld.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_IsMouseButtonHeld.restype = c_bool
        return self.ri.EIOS_IsMouseButtonHeld(target, button)

    def EIOS_SendString(
        self, target: c_void_p, text: str, keywait: int, keymodwait: int
    ) -> None:
        """
        void EIOS_SendString(EIOS* eios, const char* string, std::int32_t keywait, std::int32_t keymodwait) noexcept;
        """
        _text = bytes(text, encoding="utf8")
        self.ri.EIOS_SendString.argtypes = [c_void_p, c_char_p, c_int32, c_int32]
        self.ri.EIOS_SendString.restype = None
        self.ri.EIOS_SendString(target, _text, keywait, keymodwait)

    def EIOS_HoldKey(self, target: c_void_p, key: int) -> None:
        """
        void EIOS_HoldKey(EIOS* eios, std::int32_t key) noexcept;
        """
        self.ri.EIOS_HoldKey.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_HoldKey.restype = None
        self.ri.EIOS_HoldKey(target, key)

    def EIOS_ReleaseKey(self, target: c_void_p, key: int) -> None:
        """
        void EIOS_ReleaseKey(EIOS* eios, std::int32_t key) noexcept;
        """
        self.ri.EIOS_ReleaseKey.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_ReleaseKey.restype = None
        self.ri.EIOS_ReleaseKey(target, key)

    def EIOS_IsKeyHeld(self, target: c_void_p, key: int) -> bool:
        """
        bool EIOS_IsKeyHeld(EIOS* eios, std::int32_t key) noexcept;
        """
        self.ri.EIOS_IsKeyHeld.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_IsKeyHeld.restype = c_bool
        return self.ri.EIOS_IsKeyHeld(target, key)

    def EIOS_GetKeyboardSpeed(self, target: c_void_p) -> int:
        """
        std::int32_t EIOS_GetKeyboardSpeed(EIOS* eios) noexcept;
        """
        self.ri.EIOS_GetKeyboardSpeed.argtypes = [c_void_p]
        self.ri.EIOS_GetKeyboardSpeed.restype = c_int32
        return self.ri.EIOS_GetKeyboardSpeed(target)

    def EIOS_SetKeyboardSpeed(self, target: c_void_p, speed: int) -> None:
        """
        void EIOS_SetKeyboardSpeed(EIOS* eios, std::int32_t speed) noexcept;
        """
        self.ri.EIOS_SetKeyboardSpeed.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_SetKeyboardSpeed.restype = None
        self.ri.EIOS_SetKeyboardSpeed(target, speed)

    def EIOS_GetKeyboardRepeatDelay(self, target: c_void_p) -> int:
        """
        std::int32_t EIOS_GetKeyboardRepeatDelay(EIOS* eios) noexcept;
        """
        self.ri.EIOS_GetKeyboardRepeatDelay.argtypes = [c_void_p]
        self.ri.EIOS_GetKeyboardRepeatDelay.restype = c_int32
        return self.ri.EIOS_GetKeyboardRepeatDelay(target)

    def EIOS_SetKeyboardRepeatDelay(self, target: c_void_p, delay: int) -> None:
        """
        void EIOS_SetKeyboardRepeatDelay(EIOS* eios, std::int32_t delay) noexcept;
        """
        self.ri.EIOS_SetKeyboardRepeatDelay.argtypes = [c_void_p, c_int32]
        self.ri.EIOS_SetKeyboardRepeatDelay.restype = None
        self.ri.EIOS_SetKeyboardRepeatDelay(target, delay)

    def EIOS_PairClient(self, pid: int) -> c_void_p:
        """
        EIOS* EIOS_PairClient(pid_t pid) noexcept;
        """
        self.ri.EIOS_PairClient.argtypes = [c_int32]
        self.ri.EIOS_PairClient.restype = c_void_p
        return self.ri.EIOS_PairClient(pid)

    def EIOS_KillClientPID(self, pid: int) -> None:
        """
        void EIOS_KillClientPID(pid_t pid) noexcept;
        """
        pass

    def EIOS_KillClient(self, target: c_void_p) -> None:
        """
        void EIOS_KillClient(EIOS* eios) noexcept;
        """
        pass

    def EIOS_KillZombieClients(self) -> None:
        """
        void EIOS_KillZombieClients() noexcept;
        """
        pass

    def EIOS_GetClients(self, unpaired_only: bool = False) -> int:
        """
        std::size_t EIOS_GetClients(bool unpaired_only) noexcept;

        :param unpaired_only: Should return only unparied clients or all clients
        :type unpaired_only: bool

        :return: injectedtargets
        :rtype: Int
        """
        self.ri.EIOS_GetClients.argtypes = [c_bool]
        self.ri.EIOS_GetClients.restype = int
        return self.ri.EIOS_GetClients(unpaired_only)

    def EIOS_GetClientPID(self, index: int) -> int:
        """
        pid_t EIOS_GetClientPID(std::size_t index) noexcept;
        """
        self.ri.EIOS_GetClientPID.argtypes = [c_int]
        self.ri.EIOS_GetClientPID.restype = int
        return self.ri.EIOS_GetClientPID(index)

    ## Reflection

    def EIOS_Inject(self, process_name: str = "JagexLauncher.exe") -> None:
        """
        void EIOS_Inject(const char* process_name) noexcept;

        TODO: ask brandon if theres a better around the "ValueError:" exception when calling EIOS_Inject, other than loading the dll with CDLL('./libremoteinput.dll') for that one call.
              ERROR is...."ValueError: Procedure probably called with too many arguments (4 bytes in excess)"
        """
        self.cri.EIOS_Inject.argtypes = [c_char_p]
        self.cri.EIOS_Inject.restype = None
        self.cri.EIOS_Inject(process_name.encode("utf-8"))

    def EIOS_Inject_PID(self, pid: int) -> None:
        """
        void EIOS_Inject_PID(std::int32_t pid) noexcept;
        """
        self.cri.EIOS_Inject_PID.argtypes = [c_int]
        self.cri.EIOS_Inject_PID.restype = None
        self.cri.EIOS_Inject_PID(pid)

    def Reflect_GetEIOS(self, pid: int) -> c_void_p:
        """
        EIOS* Reflect_GetEIOS(std::int32_t pid) noexcept;
        """
        self.cri.Reflect_GetEIOS.argtypes = [c_int]
        self.ri.Reflect_GetEIOS.restype = c_void_p
        return self.ri.Reflect_GetEIOS(pid)

    # def Reflect_Object(self, ):
    #     """
    #     jobject Reflect_Object(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_IsSame_Object(self, ):
    #     """
    #     jboolean Reflect_IsSame_Object(EIOS* eios, jobject first, jobject second) noexcept;
    #     """
    #     pass

    # def Reflect_InstanceOf(self, ):
    #     """
    #     jboolean Reflect_InstanceOf(EIOS* eios, jobject object, const char* cls) noexcept;
    #     """
    #     pass

    # def Reflect_Release_Object(self, ):
    #     """
    #     void Reflect_Release_Object(EIOS* eios, jobject object) noexcept;
    #     """
    #     pass

    # def Reflect_Release_Objects(self, ):
    #     """
    #     void Reflect_Release_Objects(EIOS* eios, jobject* objects, std::size_t amount) noexcept;
    #     """
    #     pass

    # def Reflect_Bool(self, ):
    #     """
    #     bool Reflect_Bool(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Char(self, ):
    #     """
    #     char Reflect_Char(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Byte(self, ):
    #     """
    #     std::uint8_t Reflect_Byte(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Short(self, ):
    #     """
    #     std::int16_t Reflect_Short(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Int(self, ):
    #     """
    #     std::int32_t Reflect_Int(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Long(self, ):
    #     """
    #     std::int64_t Reflect_Long(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Float(self, ):
    #     """
    #     float Reflect_Float(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Double(self, ):
    #     """
    #     double Reflect_Double(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_String(self, ):
    #     """
    #     void Reflect_String(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc, char* output, std::size_t output_size) noexcept;
    #     """
    #     pass

    # def Reflect_Array(self, ):
    #     """
    #     jarray Reflect_Array(EIOS* eios, jobject object, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Array_With_Size(self, ):
    #     """
    #     jarray Reflect_Array_With_Size(EIOS* eios, jobject object, std::size_t* output_size, const char* cls, const char* field, const char* desc) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Size(self, ):
    #     """
    #     std::size_t Reflect_Array_Size(EIOS* eios, jarray array) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Index(self, ):
    #     """
    #     void* Reflect_Array_Index(EIOS* eios, jarray array, ReflectionArrayType type, std::size_t index, std::size_t length) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Index2D(self, ):
    #     """
    #     void* Reflect_Array_Index2D(EIOS* eios, jarray array, ReflectionArrayType type, std::size_t length, std::int32_t x, std::int32_t y) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Index3D(self, ):
    #     """
    #     void* Reflect_Array_Index3D(EIOS* eios, jarray array, ReflectionArrayType type, std::size_t length, std::int32_t x, std::int32_t y, std::int32_t z) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Index4D(self, ):
    #     """
    #     void* Reflect_Array_Index4D(EIOS* eios, jarray array, ReflectionArrayType type, std::size_t length, std::int32_t x, std::int32_t y, std::int32_t z, std::int32_t w) noexcept;
    #     """
    #     pass

    # def Reflect_Array_Indices(self, ):
    #     """
    #     void* Reflect_Array_Indices(EIOS* eios, jarray array, ReflectionArrayType type, std::int32_t* indices, std::size_t length) noexcept;
    #     """
    #     pass


if __name__ == "__main__":

    print("loading reflection library")
    # Create instance of Remote Input
    reflect = RemoteInput()

    # # Inject EIOS
    reflect.EIOS_Inject()

    # Get number of clients
    client_count = reflect.EIOS_GetClients()
    print(f"there are {client_count} clients")

    # Get first clients PID
    client_pid = reflect.EIOS_GetClientPID(0)

    # Pair the client and get the target or eios_ptr
    eios_ptr = reflect.EIOS_PairClient(client_pid)
    print(f"Pointer for the target for client is = {eios_ptr}")

    reflect.EIOS_LoseFocus(eios_ptr)
    have_focus1 = reflect.EIOS_HasFocus(eios_ptr)
    print(f"have_focus1 = {have_focus1}")

    reflect.EIOS_GainFocus(eios_ptr)
    have_focus2 = reflect.EIOS_HasFocus(eios_ptr)
    print(f"have_focus2 = {have_focus2}")

    dimensions = reflect.EIOS_GetTargetDimensions(eios_ptr)
    print(f"dimensions = {dimensions}")

    mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)
    print(f"mouse_position = {mouse_position}")

    real_mouse_position = reflect.EIOS_GetRealMousePosition(eios_ptr)
    print(f"real_mouse_position = {real_mouse_position}")

    print(
        "If you're at the login screen enter password to do a stupidly simple login script with fixed coordinates"
    )
    password = getpass.getpass()
    if password:
        reflect.EIOS_HoldKey(eios_ptr, VK_ESC)
        time.sleep(0.3)
        reflect.EIOS_ReleaseKey(eios_ptr, VK_ESC)
        reflect.EIOS_HoldKey(eios_ptr, VK_ESC)
        time.sleep(0.3)
        reflect.EIOS_ReleaseKey(eios_ptr, VK_ESC)
        reflect.EIOS_HoldKey(eios_ptr, VK_ESC)
        time.sleep(0.3)
        reflect.EIOS_ReleaseKey(eios_ptr, VK_ESC)

        reflect.EIOS_MoveMouse(eios_ptr, 478, 294)
        mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)
        print(f"mouse_position = {mouse_position}")

        reflect.EIOS_HoldMouse(eios_ptr, 478, 294, VK_LBUTTON)
        time.sleep(0.3)
        reflect.EIOS_ReleaseMouse(eios_ptr, 478, 294, VK_LBUTTON)
        mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)
        print(f"mouse_position = {mouse_position}")

        reflect.EIOS_HoldMouse(eios_ptr, 375, 263, VK_LBUTTON)
        time.sleep(0.3)
        reflect.EIOS_ReleaseMouse(eios_ptr, 375, 263, VK_LBUTTON)
        mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)
        print(f"mouse_position = {mouse_position}")

        reflect.EIOS_SendString(eios_ptr, password, 100, 100)

        reflect.EIOS_HoldMouse(eios_ptr, 329, 319, VK_LBUTTON)
        time.sleep(0.3)
        reflect.EIOS_ReleaseMouse(eios_ptr, 329, 319, VK_LBUTTON)
        mouse_position = reflect.EIOS_GetMousePosition(eios_ptr)
        print(f"mouse_position = {mouse_position}")

    reflect.EIOS_LoseFocus(eios_ptr)
    reflect.EIOS_ReleaseTarget(eios_ptr)
