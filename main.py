import os 

def main():
    os.system('clear')
    print("""* Bienvenidos, favor infresar datos solicitados para conexion a wifi *
            1. Gestion pos particion -  Particionado J // montado de particiones // algunas instalaciones
            2. Configuraciones de hostname
            3. Instructtivo de como configurar un usuario
            4. Despliegue de servicios y instalacion de GRUB

            5. Wifi connect pos instalacion
            
            0. Para salir
    """)

    selector = input(' -> ')
    if selector == '0':
        input('Presione enter para salir')
    elif selector == '1':
        diskmanage()
    elif selector == '2':
        config()
    elif selector == '3':
        userconf()
    elif selector == '4':
        deploimentaig()
    elif selector == '5':
        wificonnect()
    else:
        print(" OPCION NO EN MENU")
        input("...")
        return main()


def diskmanage():
    os.system('clear')
    print("""
    
     || Listado de particiones ||

    """)

    os.system('lsblk')

    print("""
    
     || Ingrese datos solicitados ||

    """)
    print("    *Ingrese nombre de particion UEFI:")
    part1=input(" -> ")
    print("    *Ingrese nombre de particion RAIZ:")
    part2=input(" -> ")
    print("    *Ingrese nombre de particion SWAP:")
    part3=input(" -> ")

    os.system(f"mkfs.vfat -F 32 /dev/{part1}")
    os.system(f"mkfs.ext4 /dev/{part2}")
    os.system(f"mkswap /dev/{part3}")
    os.system("swapon")

    os.system(f"mount /dev/{part2} /mnt/")
    os.system("mkdir /mnt/boot")
    os.system(f"mount /dev/{part1} /mnt/boot")

    os.system("pacman -Sy reflector python --noconfirm")
    os.system("reflector --verbose --latest 15 --sort rate --save /etc/pacman.d/mirrorlist")
    os.system("pacstrap /mnt base base-devel nano")
    os.system("pacstrap /mnt linux-firmware linux linux-headers mkinitcpio")
    os.system("pacstrap /mnt dhcpcd networkmanager iwd net-tools ifplugd ")
    os.system("pacstrap /mnt iw wireless_tools wpa_supplicant dialog wireless-regdb")
    os.system("pacstrap /mnt xf86-input-libinput")
    os.system("pacstrap /mnt bluez bluez-utils SS-bluetooth")
    os.system("genfstab -p /mnt >> /mnt/etc/fstab")
    os.system("arch-chroot /mnt")
    


def config():
    os.system('clear')
    print("""
    N O S A R A S H I

    Inserte hostname desktop
    """)

    hostname = input(" -> ")
    os.system(f"echo {hostname} > /etc/hostname")
    os.system(f"""echo "
127.0.0.1   localhost
::1         localhost
127.0.1.1   {hostname}.localdomain {hostname}

    ">> /etc/hosts""")
    return main()




def userconf():
    os.system('clear')
    print("""*** I N S T R U C T I V O
    
Contraseña para root:

[root@archiso /]# passwd root

Creamos nuestro usuario, para entrar a nuestro sistema.

[root@archiso /]# useradd -m -g users -G wheel -s /bin/bash nombre_de_usuario

[root@archiso /]# passwd nombre_de_usuario

 Ahora con nuestro usuario si queremos hacer algo como root por lo general usamos SUDO
Sudo tendrá efecto si nuestro usuario esta en la lista de Sudoers.

[root@archiso /]# nano /etc/sudoers

Buscamos root ALL=(ALL) ALL y abajo ponemos nuestro usuario
Para que tenga permisos y mismos privilegios al ejecutar sudo.

    nombre_de_usuario ALL=(ALL) ALL

    """)
    input("Presione enter para proceder a configurar")

def deploimentaig():
    os.system('clear')
    os.system("systemctl enable dhcpcd  NetworkManager")
    os.system("systemctl enable bluetooth")
    os.system("pacman -Sy reflector")
    os.system("reflector --verbose --latest 15 --sort rate --save /etc/pacman.d/mirrorlist")
    os.system('clear')
    #GRUB UEFI - Gestor de arranque 
    os.system("pacman -S grub efibootmgr os-prober")
    os.system("grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=Arch")
    os.system("grub-install --target=x86_64-efi --efi-directory=/efi --removable")
    os.system('nano /etc/default/grup")
    os.system("grub-mkconfig -o /boot/grub/grub.cfg")
    os.system("ls /boot/")
    input("Presione enter para volver a menu...")
    return main()


def wificonnect():
    os.system('clear')
    print("-----------------------------------------")
    print(" interface network")
    tr = os.popen("ls /sys/class/net").read()
    print(str(tr))
    print("* Listado de redes")
    os.system("nmcli dev wifi list")
    print("-----------------------------------------")
    print("* Insert the SSID of network")
    ssid=input(" -> ")
    print("* Insert the password for network")
    passw=input(" -> ")
    os.system(f"nmcli dev wifi connect '{ssid}' password {passw}")
    os.system("ping 8.8.8.8")
    input('Presione enter para retornar a menu')
    return main()

main()

