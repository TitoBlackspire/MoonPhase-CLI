# Moon Phase Tracker

## Get an update on the current moon phase all in your terminal!

## 📌 Features
This project uses the [Usno.navy Complete Sun and Moon Data for One Day](https://aa.usno.navy.mil/data/RS_OneDay) API to pull moon data and provide the following:

   - Moon Phase
   - Fracillum/Ilumination
   - Moon Rise & Set Time
 
Using the results provided via the API it then gets parsed and made look "pretty". Also ascii art is used to give the users a visual representation all in the terminal.

## 📋 Installation (Arch Linux)
```bash 
# Clone the repository
git clone https://github.com/TitoBlackspire/Moon-Phase-Tracker.git

# Navigate into the directory
cd Moon-Phase-Tracker

# Build the package
makepkg -si

# Set up config file
mkdir -p ~/.config/moonphase
cp /etc/skel/.config/moonphase/.env.example ~/.config/moonphase/.env
```

## 🎯 Usage
To use the program in your terminal run:
```bash
moonphase
```

## 🗑️ Uninstalling

```bash
sudo pacman -R moonphase
```

## 🛠️ Requirements
- Arch Linux (or Arch-based distro)
- Python 3
- Dependencies installed automatically via makepkg (requests, geopy, python-dotenv)

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
