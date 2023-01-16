#!/usr/bin/env python

import binascii
# a='45222e'
# s=binascii.unhexlify(a)
# b=[ord(x) for x in s]

# import can
import time
import serial

from bluetooth import *

ECU_ADDR_H = "7E2"  # HVECU address (Hybrid contol module)
ECU_R_ADDR_H = "7EA"  # Responses sent by HVECU (Hybrid contol module) 7E2/7EA
ECU_ADDR_E = "7E0"  # Engine ECU address
ECU_R_ADDR_E = "7E8"  # Responses sent by Engine ECU - ECM (engine control module) 7E0/7E8
ECU_ADDR_T = "7E1"  # Transmission ECU address (transmission control module)
ECU_R_ADDR_T = "7E9"  # Responses sent by Transmission ECU - TCM (transmission control module) 7E1/7E9
ECU_ADDR_I = "7C0"  # ICE ECU address
ECU_R_ADDR_I = "7C8"  # Responses sent by ICE ECU address 7C0/7C8
ECU_ADDR_B = "7E3"  # Traction Battery ECU address
ECU_R_ADDR_B = "7EB"  # Responses sent by Traction Battery ECU - 7E3/7EB
ECU_ADDR_P = "7C4"  # Air Conditioning
ECU_R_ADDR_P = "7CC"  # Responses sent by Air Conditioning ECU - 7C4/7CC
ECU_ADDR_S = "7B0"  # Skid Control address ECU
ECU_R_ADDR_S = "7B8"  # Responses sent by 7B0 Skid Control ECU 7B0/7B8

ELM_R_OK = "OK\r"
ELM_MAX_RESP = '[0123456]?$'

responce = dict()
responce['ATZ'] = "ELM327 v1.5\n"
responce['ATE0'] = "OK"
responce['ATM0'] = "OK"
responce['ATL0'] = "OK"
responce['ATST62'] = "OK"
responce['ATS0'] = "OK"
responce['AT@1'] = "OBDII to RS232 Interpreter"
responce['ATI'] = "ELM327/ELM-USB v1.0 (c) SECONS Ltd.\n"
responce['ATH0'] = "OK"
responce['ATH1'] = "OK"
responce['ATAT1'] = "OK"
responce['ATAT2'] = "OK"
responce['ATDPN'] = "A0"

responce['ATSP0'] = "NO DATA"
responce['ATSP1'] = "NO DATA"
responce['ATSP2'] = "NO DATA"
responce['ATSP3'] = "NO DATA"
responce['ATSP4'] = "NO DATA"
responce['ATSP5'] = "NO DATA"
responce['ATSP6'] = "OK"
responce['ATSP7'] = "NO DATA"
responce['ATSP8'] = "NO DATA"


responce['0100'] = '41 00 FF FF FF FF\r' # list pids
responce['0120'] = '41 20 FF FF FF FF\r' # list pids
responce['0140'] = '41 40 FF FF FF FF\r' # list pids
responce['0160'] = '41 60 FF FF FF FF\r' # list pids

responce['01781'] = '41 78 10 11\r' # EGT 1
responce['01791'] = '41 79 00 00\r' # EGT 2

responce['01701'] = '41 70 00 00 00 00 17\r' # boost

# responce['0178'] = '41 78 10 11 \r' # EGT 1
# responce['0179'] = '41 79 08 55 \r' # EGT 2
# responce['0170'] = '41 70 00 FF \r' # boost

responce['015C'] = '41 5C 30\r' # oil temp
responce['015C1'] = '41 5C 30\r' # oil temp

responce['0114'] = '41 14 FF' # afr custom (A*(0.06)) + 7.35

responce['010D1'] = '41 0D 30\r' # speed
responce['010C1'] = '41 0C 11 00\r' # rpm

responce['010C'] = '41 0C 11 00\r' # rpm
responce['010D'] = '41 0D 30\r' # speed
responce['0105'] = '41 05 64\r' # coolant



# pids = {
#         'FUEL_STATUS': {
#             'Request': '^0103' + ELM_MAX_RESP,
#             'Descr': 'Fuel System Status',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 03 00 00 \r'
#         },
#         'ENGINE_LOAD': {
#             'Request': '^0104' + ELM_MAX_RESP,
#             'Descr': 'Calculated Engine Load',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 04 00 \r'
#         },
#         'COOLANT_TEMP': {
#             'Request': '^0105' + ELM_MAX_RESP,
#             'Descr': 'Engine Coolant Temperature',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 05 41 05 7B \r'
#         },
#         'INTAKE_PRESSURE': {
#             'Request': '^010B' + ELM_MAX_RESP,
#             'Descr': 'Intake Manifold Pressure',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 0B 73 \r'
#         },
#         'RPM': {
#             'Request': '^010C' + ELM_MAX_RESP,
#             'Descr': 'Engine RPM',
#             'Header': ECU_ADDR_E,
#             'Response': '',
#             'ResponseFooter': \
#             lambda self, cmd, pid, val: \
#                 ECU_R_ADDR_E + ' 04 41 0C ' \
#                 + self.Sequence(pid, base=2400, max=200, factor=80, n_bytes=2) \
#                 + ' \r' + ECU_R_ADDR_H + ' 04 41 0C ' \
#                 + self.Sequence(pid, base=2400, max=200, factor=80, n_bytes=2) \
#                 + ' \r'
#         },
#         'SPEED': {
#             'Request': '^010D' + ELM_MAX_RESP,
#             'Descr': 'Vehicle Speed',
#             'Header': ECU_ADDR_E,
#             'Response': '',
#             'ResponseFooter': \
#             lambda self, cmd, pid, val: \
#                 ECU_R_ADDR_E + ' 03 41 0D ' \
#                 + self.Sequence(pid, base=0, max=30, factor=4, n_bytes=1) \
#                 + ' \r' + ECU_R_ADDR_H + ' 03 41 0D ' \
#                 + self.Sequence(pid, base=0, max=30, factor=4, n_bytes=1) \
#                 + ' \r'
#         },
#         'INTAKE_TEMP': {
#             'Request': '^010F' + ELM_MAX_RESP,
#             'Descr': 'Intake Air Temp',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 0F 44 \r'
#         },
#         'MAF': {
#             'Request': '^0110' + ELM_MAX_RESP,
#             'Descr': 'Air Flow Rate (MAF)',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 10 05 1F \r'
#         },
#         'THROTTLE_POS': {
#             'Request': '^0111' + ELM_MAX_RESP,
#             'Descr': 'Throttle Position',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 11 FF \r'
#         },
#         'OBD_COMPLIANCE': {
#             'Request': '^011C' + ELM_MAX_RESP,
#             'Descr': 'OBD Standards Compliance',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 1C 06 \r'
#         },
#         'RUN_TIME': {
#             'Request': '^011F' + ELM_MAX_RESP,
#             'Descr': 'Engine Run Time',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 1F 00 8C \r'
#         },
#         'DISTANCE_W_MIL': {
#             'Request': '^0121' + ELM_MAX_RESP,
#             'Descr': 'Distance Traveled with MIL on',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 21 00 00 \r00 \r'
#         },
#         'FUEL_RAIL_PRESSURE_DIRECT': {
#             'Request': '^0123' + ELM_MAX_RESP,
#             'Descr': 'Fuel Rail Pressure (direct inject)',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 23 1A 0E \r'
#         },
#         'COMMANDED_EGR': {
#             'Request': '^012C' + ELM_MAX_RESP,
#             'Descr': 'Commanded EGR',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 2C 0D \r'
#         },
#         'EGR_ERROR': {
#             'Request': '^012D' + ELM_MAX_RESP,
#             'Descr': 'EGR Error',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 2D 80 \r'
#         },
#         'DISTANCE_SINCE_DTC_CLEAR': {
#             'Request': '^0131' + ELM_MAX_RESP,
#             'Descr': 'Distance traveled since codes cleared',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 31 C8 1F \r'
#         },
#         'BAROMETRIC_PRESSURE': {
#             'Request': '^0133' + ELM_MAX_RESP,
#             'Descr': 'Barometric Pressure',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 33 65 \r'
#         },
#         'CATALYST_TEMP_B1S1': {
#             'Request': '^013C' + ELM_MAX_RESP,
#             'Descr': 'Catalyst Temperature: Bank 1 - Sensor 1',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 3C 04 44 \r'
#         },
#         'CONTROL_MODULE_VOLTAGE': {
#             'Request': '^0142' + ELM_MAX_RESP,
#             'Descr': 'Control module voltage',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 42 39 D6 \r00 \r'
#         },
#         'AMBIANT_AIR_TEMP': {
#             'Request': '^0146' + ELM_MAX_RESP,
#             'Descr': 'Ambient air temperature',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 46 43 \r'
#         },
#         'ACCELERATOR_POS_D': {
#             'Request': '^0149' + ELM_MAX_RESP,
#             'Descr': 'Accelerator pedal position D',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 49 00 \r'
#         },
#         'ACCELERATOR_POS_E': {
#             'Request': '^014A' + ELM_MAX_RESP,
#             'Descr': 'Accelerator pedal position E',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 4A 45 \r'
#         },
#         'THROTTLE_ACTUATOR': {
#             'Request': '^014C' + ELM_MAX_RESP,
#             'Descr': 'Commanded throttle actuator',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 4C 00 \r'
#         },
#         'RUN_TIME_MIL': {
#             'Request': '^014D' + ELM_MAX_RESP,
#             'Descr': 'Time run with MIL on',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 4D 00 00 \r00 \r'
#         },
#         'TIME_SINCE_DTC_CLEARED': {
#             'Request': '^014E' + ELM_MAX_RESP,
#             'Descr': 'Time since trouble codes cleared',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 4E 4C 69 \r00 \r'
#         },
#         'FUEL_TYPE': {
#             'Request': '^0151' + ELM_MAX_RESP,
#             'Descr': 'Fuel Type',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 03 41 51 01 \r'
#         },
#         'FUEL_INJECT_TIMING': {
#             'Request': '^015D' + ELM_MAX_RESP,
#             'Descr': 'Fuel injection timing',
#             'Header': ECU_ADDR_E,
#             'Response': ECU_R_ADDR_E + ' 04 41 5D 66 00 \r'
#         },
#         # Supported PIDs for protocols
#         'ELM_PIDS_A': {
#             'Request': '^0100' + ELM_MAX_RESP,
#             'Descr': 'PIDS_A',
#             'ResponseHeader': \
#             lambda self, cmd, pid, val: \
#                 'SEARCHING...\0 time.sleep(3) \0\r' if self.counters[pid] == 1 else "",
#             'Response':
#             ECU_R_ADDR_H + ' 06 41 00 98 3A 80 13 \r' +
#             ECU_R_ADDR_E + ' 06 41 00 BE 3F A8 13 \r'
#         },
#         'ELM_PIDS_B': {
#             'Request': '^0120' + ELM_MAX_RESP,
#             'Descr': 'PIDS_B',
#             'Response':
#             ECU_R_ADDR_H + ' 06 41 20 80 01 A0 01 \r' +
#             ECU_R_ADDR_E + ' 06 41 20 90 15 B0 15 \r'
#         },
#         'ELM_PIDS_C': {
#             'Request': '^0140' + ELM_MAX_RESP,
#             'Descr': 'PIDS_C',
#             'Response':
#             ECU_R_ADDR_H + ' 06 41 40 44 CC 00 21 \r' +
#             ECU_R_ADDR_E + ' 06 41 40 7A 1C 80 00 \r'
#         },
#         'ELM_MIDS_A': {
#             'Request': '^0600' + ELM_MAX_RESP,
#             'Descr': 'MIDS_A',
#             'Response': ECU_R_ADDR_E + ' 06 46 00 C0 00 00 01 \r'
#         },
#         'ELM_MIDS_B': {
#             'Request': '^0620' + ELM_MAX_RESP,
#             'Descr': 'MIDS_B',
#             'Response': ECU_R_ADDR_E + ' 06 46 20 80 00 80 01 \r'
#         },
#         'ELM_MIDS_C': {
#             'Request': '^0640' + ELM_MAX_RESP,
#             'Descr': 'MIDS_C',
#             'Response': ECU_R_ADDR_E + ' 06 46 40 00 00 00 01 \r'
#         },
#         'ELM_MIDS_D': {
#             'Request': '^0660' + ELM_MAX_RESP,
#             'Descr': 'MIDS_D',
#             'Response': ECU_R_ADDR_E + ' 06 46 60 00 00 00 01 \r'
#         },
#         'ELM_MIDS_E': {
#             'Request': '^0680' + ELM_MAX_RESP,
#             'Descr': 'MIDS_E',
#             'Response': ECU_R_ADDR_E + ' 06 46 80 00 00 00 01 \r'
#         },
#         'ELM_MIDS_F': {
#             'Request': '^06A0' + ELM_MAX_RESP,
#             'Descr': 'MIDS_F',
#             'Response': ECU_R_ADDR_E + ' 06 46 A0 F8 00 00 00 \r'
#         },
#         'ELM_PIDS_9A': {
#             'Request': '^0900' + ELM_MAX_RESP,
#             'Descr': 'PIDS_9A',
#             'Response': ECU_R_ADDR_E + ' 06 49 00 FF FF FF FF \r'
#         },
#         'VIN_MESSAGE_COUNT': {
#             'Request': '^0901' + ELM_MAX_RESP,
#             'Descr': 'VIN Message Count',
#             'Response': ECU_R_ADDR_E + ' 03 49 01 01 \r'
#         },
#         'VIN': { # Check this also: https://stackoverflow.com/a/26752855/10598800, https://www.autocheck.com/vehiclehistory/autocheck/en/vinbasics
#             'Request': '^0902' + ELM_MAX_RESP,
#             'Descr': 'Get Vehicle Identification Number',
#             'Response': [
#                         ECU_R_ADDR_E + ' 10 14 49 02 01 57 50 30 \r' +
#                         ECU_R_ADDR_E + ' 21 5A 5A 5A 39 39 5A 54 \r' +
#                         ECU_R_ADDR_E + ' 22 53 33 39 30 30 30 30 \r', # https://www.autodna.com/vin/WP0ZZZ99ZTS390000, https://it.vin-info.com/libro-denuncia/WP0ZZZ99ZTS390000
#                         ECU_R_ADDR_E + ' 10 14 49 02 01 4D 41 54 \r' + # https://community.carloop.io/t/how-to-request-vin/153/11
#                         ECU_R_ADDR_E + ' 21 34 30 33 30 39 36 42 \r' +
#                         ECU_R_ADDR_E + ' 22 4E 4C 30 30 30 30 30 \r'
#                         ]
#         },
#         'CALIBRATION_ID_MESSAGE_COUNT': {
#             'Request': '^0903' + ELM_MAX_RESP,
#             'Descr': 'Calibration ID message count for PID 04',
#             'Response': ECU_R_ADDR_E + ' 03 49 03 01 \r'
#         }
#     }


def connect(full=False):

    if full:
        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )

        print "Waiting for connection on RFCOMM channel %d" % port

        client_sock, client_info = server_sock.accept()
        print "Accepted connection from ", client_info
        return client_sock

    connecting = True
    print('connecting...')
    while connecting:
        try:
            com = serial.Serial('/dev/rfcomm0', 19200, timeout=1)
            com.close()
            connecting = False
            print('connectied!')
        except:
            time.sleep(1)

    socket = serial.Serial('/dev/rfcomm0', 19200, timeout=1)
    return socket


def write(stream, resp, linefeeds = False, echo = False, echo_cmd = ''):

    n = "\r\n" if linefeeds else "\r"

    resp += n + ">"

    if echo:
        resp = echo_cmd + n + resp

    # stream.write(resp.encode())

    if 'write' in dir(stream):
        stream.write(resp)
    else:
        stream.send(resp)


def read(stream):
    buffer = ""

    while True:

        if 'read' in dir(stream):
            c = stream.read().decode()
        else:
            c = stream.recv(1).decode()
        if c == '\n':
            break

        if c == '\r':
            break  # ignore carraige returns

        buffer += c

    return buffer


def main():
    linefeeds = False
    echo = False
    headers = False

    server = connect(full=False)

    while True:
        time.sleep(0)

        command = read(server)

        if command == '':
            continue

        print("< {}".format(command))

        if command in responce:

            if command == "ATL0":
                linefeeds = False
            if command == "ATL1":
                linefeeds = True
            if command == "ATH0":
                headers = False
            if command == "ATH1":
                headers = True
            if command == "ATE0":
                echo = False
            if command == "ATE1":
                echo = True

            res = responce[command]

            write(server, res, linefeeds=linefeeds, echo=echo)

            print("> {}".format(res))
        else:

            write(server, "NO DATA")
            print("(new) > {}".format("False"))


if __name__ == "__main__":
    main()