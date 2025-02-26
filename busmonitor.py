import PySimpleGUI as sg
import struct
import matplotlib.pyplot as plt
import numpy as np


def hex_to_value(hex_value, bits=16):
    value = int(hex_value, 16)
    if bits == 16:
        return handle_16bit(value)
    elif bits == 32:
        return handle_32bit(value)
    else:
        raise ValueError("Unsupported bit length: Only 16 or 32 bits are supported.")

def handle_16bit(value):
    if value & 0x8000:
        return value - 0x10000
    else:
        return value

def handle_32bit(value):
    if value & 0x80000000:
        return value - 0x100000000
    else:
        return value

def hex_to_twos_complement(hex_value, bits=16):
    value = int(hex_value, 16)
    if bits == 16:
        if value & 0x8000:
            return value - 0x10000
        else:
            return value
    elif bits == 32:
        if value & 0x80000000:
            return value - 0x100000000
        else:
            return value
    else:
        raise ValueError("Unsupported bit length for two's complement. Only 16 or 32 bits supported.")

def hex_to_float(hex_value, is_double=False):
    if is_double:
        return struct.unpack('!d', bytes.fromhex(hex_value))[0]
    else:
        return struct.unpack('!f', bytes.fromhex(hex_value))[0]


def process_conversion(hex_value, conversion_type, bits=16):
    if conversion_type == "16-bit Unsigned/Signed":
        return hex_to_value(hex_value, bits=16)
    elif conversion_type == "32-bit Unsigned/Signed":
        return hex_to_value(hex_value, bits=32)
    elif conversion_type == "16-bit Two's Complement":
        return hex_to_twos_complement(hex_value, bits=16)
    elif conversion_type == "32-bit Two's Complement":
        return hex_to_twos_complement(hex_value, bits=32)
    elif conversion_type == "32-bit Float":
        return hex_to_float(hex_value)
    elif conversion_type == "64-bit Float":
        return hex_to_float(hex_value, is_double=True)
    else:
        return "Invalid Conversion Type"


def plot_graph(x_values, m, c):
    y_values = m * np.array(x_values) + c
    plt.plot(x_values, y_values, label=f'y = {m}x + {c}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph of y = mx + c')
    plt.legend()
    plt.grid(True)
    plt.show()


layout = [
    [sg.Text('Hexadecimal to Bit Conversion', font=('Helvetica', 16))],
    [sg.Text('Enter hexadecimal values below, one per line:', size=(30, 1))],
    [sg.Multiline('', size=(50, 10), key='-INPUT-', disabled=False)],
    [sg.Text('Select Conversion Type:', size=(20, 1))],
    [sg.Combo(['16-bit Unsigned/Signed', '32-bit Unsigned/Signed', '16-bit Two\'s Complement',
               '32-bit Two\'s Complement', '32-bit Float', '64-bit Float'],
              default_value='16-bit Unsigned/Signed', key='-CONVERSION_TYPE-', size=(30, 1))],
    [sg.Button('Convert'), sg.Button('Clear')],
    [sg.Text('Results:', size=(30, 1))],
    [sg.Multiline('', size=(50, 10), key='-OUTPUT-', disabled=True)],
    [sg.Text('Enter m (slope) and c (intercept) for y = mx + c', size=(30, 1))],
    [sg.Text('m (slope):'), sg.InputText('', key='-M-', size=(10, 1))],
    [sg.Text('c (intercept):'), sg.InputText('', key='-C-', size=(10, 1))],
    [sg.Button('Plot Graph')]
]


window = sg.Window('Hexadecimal Converter', layout, finalize=True)


x_values = []


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'Convert':

        hex_values = values['-INPUT-'].splitlines()
        conversion_type = values['-CONVERSION_TYPE-']

        if hex_values:

            try:
                output = []
                x_values.clear()

                for hex_value in hex_values:
                    hex_value = hex_value.strip()
                    if hex_value:
                        result = process_conversion(hex_value, conversion_type)
                        x_values.append(result)
                        output.append(f"Hex: {hex_value} => {conversion_type}: {result}")

                window['-OUTPUT-'].update('\n'.join(output))
                window['-M-'].update('')
                window['-C-'].update('')
            except Exception as e:
                window['-OUTPUT-'].update(f"Error during conversion: {str(e)}")
        else:
            window['-OUTPUT-'].update("Please enter hexadecimal values to convert.")

    elif event == 'Plot Graph':

        if not x_values:
            sg.popup("Error", "Please first convert hexadecimal values to x-values before plotting.")
            continue


        try:
            m = float(values['-M-'])
            c = float(values['-C-'])


            plot_graph(x_values, m, c)

        except ValueError:
            sg.popup("Error", "Please enter valid numerical values for m and c.")

    elif event == 'Clear':
        window['-INPUT-'].update('')
        window['-CONVERSION_TYPE-'].update('16-bit Unsigned/Signed')
        window['-OUTPUT-'].update('')
        window['-M-'].update('')
        window['-C-'].update('')
        x_values.clear()

window.close()