#!/bin/bash

RED='\033[0;31m'
BLUE='\033[0;34m'
YEL='\033[0;33m'
GRN='\033[0;32m'
RESET='\033[0m'

echo -e " 🔔  ${YEL}ARE YOU IN VIRTUAL ENVIRONMENT?${RESET}"
read -p "     [Y|N|?]: " response

if [[ "$response" == "y" || "$response" == "Y" ]]; then

  echo -e " 🗿  ${BLUE}Upgrading pip...${RESET}"
  python3 -m pip install --upgrade pip

  echo -e " 🗿  ${BLUE}Installing Django...${RESET}"
  python3 -m pip install django==4.0
#  python3 -m pip install --upgrade django


  python3 -m pip install channels==4.0.0
#  python3 -m pip install --upgrade channels

  python3 -m pip install daphne==4.0.0
#  python3 -m pip install --upgrade daphne

  python3 -m pip install channels_redis
#  python3 -m pip install --upgrade channels_redis

  echo -e " 🗿  ${BLUE}Applying migrations...${RESET}"
  python3 backend/manage.py makemigrations
  python3 backend/manage.py migrate


  echo -e " 🗿  ${BLUE}Starting Django server...${RESET}"
  python3 backend/manage.py runserver 6969


  echo -e " 🗿  ${RED}Server exit${RESET}"

elif [[ "$response" == "?" ]]; then
  echo -e "\n 💡  ${RESET}Your Terminal should look like this:"
  echo -e "       (${YEL}virtualEnvironment${RESET}) user@lol69 TRANSCENDENCE %"
  echo -e "\n     To create virtual Environment:"
  echo -e "       ${YEL}python3 -m venv <venv_name>${RESET}"
  echo -e "\n     To activate virtual Environment run:"
  echo -e "       ${YEL}source <venv_name>/bin/activate${RESET}"
  echo -e "\n     For more Information's go to:"
  echo -e "       https://docs.python.org/3/library/venv.html\n"
else
  echo -e "\n ${RED}❌   ACTIVATE VIRTUAL ENVIRONMENT!\n${BLUE} 💡  RUN:  source virtualEnvironment/bin/activate${RESET}"
fi
