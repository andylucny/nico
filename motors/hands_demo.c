/*******************************************************************************
* Copyright 2017 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* Author: Ryu Woon Jung (Leon) */

//
// *********     Read and Write Example      *********
//
//
// Available DXL model on this example : All models using Protocol 1.0
// This example is designed for using a Dynamixel MX-28, and an USB2DYNAMIXEL.
// To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below "#define"d variables yourself.
// Be sure that Dynamixel MX properties are already set as %% ID : 1 / Baudnum : 34 (Baudrate : 57600)
//

#if defined(__linux__) || defined(__APPLE__)
#include <fcntl.h>
#include <termios.h>
#define STDIN_FILENO 0
#elif defined(_WIN32) || defined(_WIN64)
#include <conio.h>
#endif

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "dynamixel_sdk.h"                                  // Uses Dynamixel SDK library

// Control table address
#define ADDR_MX_TORQUE_ENABLE           24                  // Control table address is different in Dynamixel model
#define ADDR_MX_GOAL_POSITION           30
#define ADDR_MX_PRESENT_POSITION        36

// Protocol version
#define PROTOCOL_VERSION                1.0                 // See which protocol version is used in the Dynamixel

// Default setting

#define DEMO_MOTORS			12
int DXL_ID[] =                          { 47, 37, 46, 36, 44, 34, 45, 35, 33, 43, 31, 41 };                   // Dynamixel ID: 1
#define BAUDRATE                        1000000
#define DEVICENAME                      "/dev/ttyUSB0"      // Check which port is being used on your controller
                                                            // ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

#define TORQUE_ENABLE                   1                   // Value for enabling the torque
#define TORQUE_DISABLE                  0                   // Value for disabling the torque
int DXL_ONE_POSITION_VALUE[] = { 2500, 2500, 2500, 2500, 3500, 3500, 1500, 1500, 3700, 3700, 2500, 2500 };                // Dynamixel will rotate between this value
int DXL_TWO_POSITION_VALUE[] = { 0, 0, 0, 0, 0, 0, 0, 0, 700, 700, 3900, 3900 };               // and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
#define DXL_MOVING_STATUS_THRESHOLD     20                  // Dynamixel moving status threshold

#define ESC_ASCII_VALUE                 0x1b

int getch()
{
#if defined(__linux__) || defined(__APPLE__)
  struct termios oldt, newt;
  int ch;
  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  ch = getchar();
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  return ch;
#elif defined(_WIN32) || defined(_WIN64)
  return _getch();
#endif
}

int kbhit(void)
{
#if defined(__linux__) || defined(__APPLE__)
  struct termios oldt, newt;
  int ch;
  int oldf;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

  ch = getchar();

  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);

  if (ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }

  return 0;
#elif defined(_WIN32) || defined(_WIN64)
  return _kbhit();
#endif
}

int main()
{
  // Initialize PortHandler Structs
  // Set the port path
  // Get methods and members of PortHandlerLinux or PortHandlerWindows
  int port_num = portHandler(DEVICENAME);

  // Initialize PacketHandler Structs
  packetHandler();

  int dxl_comm_result = COMM_TX_FAIL;             // Communication result
  int dxl_goal_position[DEMO_MOTORS][2];
  for (int i = 0; i < DEMO_MOTORS; i++)
  {
	 dxl_goal_position[i][0] = DXL_ONE_POSITION_VALUE[i];
         dxl_goal_position[i][1] =  DXL_TWO_POSITION_VALUE[i];  // Goal position
  }

  uint8_t dxl_error = 0;                          // Dynamixel error
  uint16_t dxl_present_position = 0;              // Present position

  // Open port
  if (openPort(port_num))
  {
    printf("Succeeded to open the port!\n");
  }
  else
  {
    printf("Failed to open the port!\n");
    printf("Press any key to terminate...\n");
    getch();
    return 0;
  }

  // Set port baudrate
  if (setBaudRate(port_num, BAUDRATE))
  {
    printf("Succeeded to change the baudrate!\n");
  }
  else
  {
    printf("Failed to change the baudrate!\n");
    printf("Press any key to terminate...\n");
    getch();
    return 0;
  }

  // Enable Dynamixel Torque
  for (int i = 0; i < DEMO_MOTORS; i++)
  {
    write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID[i], ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE);
    if ((dxl_comm_result = getLastTxRxResult(port_num, PROTOCOL_VERSION)) != COMM_SUCCESS)
    {
      printf("%s\n", getTxRxResult(PROTOCOL_VERSION, dxl_comm_result));
    }
    else if ((dxl_error = getLastRxPacketError(port_num, PROTOCOL_VERSION)) != 0)
    {
      printf("%s\n", getRxPacketError(PROTOCOL_VERSION, dxl_error));
    }
    else
    {
      printf("Dynamixel has been successfully connected \n");
    }
  }

  while (1)
  {
    printf("Press any key to continue! (or press ESC to quit!)\n");
    if (getch() == ESC_ASCII_VALUE)
      break;

    for (int i = 0; i < DEMO_MOTORS; i++)
    {
	    for (int ind = 0; ind < 4; ind++)
	    {
		int index = ind % 2;
                // Write goal position
                write2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID[i], ADDR_MX_GOAL_POSITION, dxl_goal_position[i][index]);
                if ((dxl_comm_result = getLastTxRxResult(port_num, PROTOCOL_VERSION)) != COMM_SUCCESS)
                {
                  printf("%s\n", getTxRxResult(PROTOCOL_VERSION, dxl_comm_result));
                }
                else if ((dxl_error = getLastRxPacketError(port_num, PROTOCOL_VERSION)) != 0)
                {
                  printf("%s\n", getRxPacketError(PROTOCOL_VERSION, dxl_error));
                }
            
                do
                {
                  // Read present position
                  dxl_present_position = read2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID[i], ADDR_MX_PRESENT_POSITION);
                  if ((dxl_comm_result = getLastTxRxResult(port_num, PROTOCOL_VERSION)) != COMM_SUCCESS)
                  {
                    printf("%s\n", getTxRxResult(PROTOCOL_VERSION, dxl_comm_result));
                  }
                  else if ((dxl_error = getLastRxPacketError(port_num, PROTOCOL_VERSION)) != 0)
                  {
                    printf("%s\n", getRxPacketError(PROTOCOL_VERSION, dxl_error));
                  }
            
                  printf("[ID:%03d] GoalPos:%03d  PresPos:%03d\r", DXL_ID[i], dxl_goal_position[i][index], dxl_present_position);
            
                } while ((abs(dxl_goal_position[i][index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD));
		usleep(200000);
	    }
	    sleep(1);
    }
  }

  // Disable Dynamixel Torque
  for (int i = 0; i < DEMO_MOTORS; i++)
  {
      //printf("disabling torque of %d\n", DXL_ID[i]);
      write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID[i], ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE);
      if ((dxl_comm_result = getLastTxRxResult(port_num, PROTOCOL_VERSION)) != COMM_SUCCESS)
      {
        printf("%s\n", getTxRxResult(PROTOCOL_VERSION, dxl_comm_result));
      }
      else if ((dxl_error = getLastRxPacketError(port_num, PROTOCOL_VERSION)) != 0)
      {
        printf("%s\n", getRxPacketError(PROTOCOL_VERSION, dxl_error));
      }
  }

  // Close port
  closePort(port_num);

  return 0;
}
