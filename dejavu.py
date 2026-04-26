import os
import subprocess
import hashlib
import shutil
from time import time
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image

def abrir_guia():
    os.system('xdg-open "Guia passo a passo sobre como executar a ferramenta Dejavu com a interface gráfica.txt"')

def selecionar_imagem_dispositivo():
    caminho_imagem = filedialog.askopenfilename(
        title="Selecione a imagem do dispositivo ou o dispositivo",
        filetypes=(("Imagens de disco", "*.img;*.dd"), ("Todos os arquivos", "*.*"))
    )
    if caminho_imagem:
        caminho_dispositivo_var.set(caminho_imagem)

def selecionar_diretorio_saida():
    pasta_selecionada = filedialog.askdirectory()
    diretorio_saida_var.set(pasta_selecionada)

def calcular_hash_md5(caminho_arquivo):
    hash_md5 = hashlib.md5()
    with open(caminho_arquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verificar_integridade_imagem(caminho_arquivo):
    try:
        img = Image.open(caminho_arquivo)
        img.verify()  
        return True
    except Exception as e:
        print(f"Erro ao abrir a imagem {caminho_arquivo}: {e}")
        return False

def renomear_e_mover_arquivos(diretorio_saida, file_type):
    hashes = {}
    total_arquivos = 0
    total_duplicados = 0
    total_falso_positivo = 0

    os.makedirs(os.path.join(diretorio_saida, "Duplicados"), exist_ok=True)
    os.makedirs(os.path.join(diretorio_saida, "Falso_Positivo"), exist_ok=True)

    for arquivo in os.listdir(diretorio_saida):
        caminho_completo = os.path.join(diretorio_saida, arquivo)
        if os.path.isfile(caminho_completo) and arquivo.lower().endswith(('jpeg', 'jpg', 'png')):
            total_arquivos += 1
            hash_arquivo = calcular_hash_md5(caminho_completo)
            novo_nome_arquivo = hash_arquivo + os.path.splitext(arquivo)[1]

            if hash_arquivo in hashes:
                shutil.move(caminho_completo, os.path.join(diretorio_saida, "Duplicados", novo_nome_arquivo))
                total_duplicados += 1
            else:
                hashes[hash_arquivo] = {'caminho': caminho_completo, 'tamanho': os.path.getsize(caminho_completo)}
                os.rename(caminho_completo, os.path.join(diretorio_saida, novo_nome_arquivo))

    for hash_arquivo, arquivo_info in hashes.items():
        caminho_arquivo = arquivo_info['caminho']
        tamanho_arquivo = arquivo_info['tamanho']
        
        if not os.path.exists(caminho_arquivo):
            continue

        if tamanho_arquivo != os.path.getsize(caminho_arquivo):
            shutil.move(caminho_arquivo, os.path.join(diretorio_saida, "Falso_Positivo", os.path.basename(caminho_arquivo)))
            total_falso_positivo += 1

    return total_arquivos, total_duplicados, total_falso_positivo

def executar_dejavu():
    base_command = "./dejavu"
    file_type = tipo_arquivo_var.get()
    
    if file_type == "JPEG":
        dejavu_folder = "dejavu-JPEG"
    elif file_type == "PNG":
        dejavu_folder = "dejavu-PNG"
    else:
        print("Tipo de arquivo não suportado!")
        return
    
    command = [base_command, "-vv", "-o", diretorio_saida_var.get(), "-oneclass"]
    
    if sem_rodape_var.get():
        command.append("-nofooter")
    
    command.extend(["-fex", metodo_extracao_var.get(), caminho_dispositivo_var.get()])
    
    start_time = time()
    try:
        process = subprocess.Popen(command, cwd=dejavu_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        end_time = time()
        elapsed_time = end_time - start_time

        if stdout:
            stdout_str = stdout.decode().replace("deca_detector_tst_jpeg_svm_histo", "Dejavu Forensics").replace("deca_detector_tst_jpeg_svm_raw", "Dejavu Forensics")
            print(stdout_str)
        if stderr:
            stderr_str = stderr.decode().replace("deca_detector_tst_jpeg_svm_histo", "Dejavu Forensics").replace("deca_detector_tst_jpeg_svm_raw", "Dejavu Forensics")
            print(stderr_str)
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")

    total_arquivos, total_duplicados, total_falso_positivo = renomear_e_mover_arquivos(diretorio_saida_var.get(), file_type)
    
    print(f"Dejavu recuperou {total_arquivos} arquivos ({file_type}), {total_duplicados} foram duplicados, {total_falso_positivo} falso positivo(s).")
    print(f"Tempo de execução: {elapsed_time:.2f} segundos.")

root = tk.Tk()
root.title("Dejavu Forensics 1.0")
root.geometry("1030x890")

background_image = tk.PhotoImage(file='ICON DEJAVU FORENSICS.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
root.iconphoto(False, background_image)

tipo_arquivo_var = tk.StringVar(value="JPEG")
metodo_extracao_var = tk.StringVar(value="raw")
sem_rodape_var = tk.BooleanVar(value=False)
caminho_dispositivo_var = tk.StringVar()
diretorio_saida_var = tk.StringVar()

ttk.Label(root, text="Tipo de Arquivo:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Combobox(root, textvariable=tipo_arquivo_var, values=("JPEG", "PNG")).grid(row=0, column=1, padx=10, pady=5)
ttk.Label(root, text="Método de Extração:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ttk.Combobox(root, textvariable=metodo_extracao_var, values=("raw", "histo")).grid(row=1, column=1, padx=10, pady=5)
ttk.Checkbutton(root, text="NoFooter", variable=sem_rodape_var).grid(row=2, column=0, columnspan=2, padx=10, pady=5)
ttk.Label(root, text="Caminho do Dispositivo:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
ttk.Entry(root, textvariable=caminho_dispositivo_var).grid(row=3, column=1, padx=10, pady=5)
ttk.Button(root, text="Procurar Dispositivo", command=selecionar_imagem_dispositivo).grid(row=3, column=2, padx=10, pady=5)
ttk.Label(root, text="Diretório de Saída:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
ttk.Entry(root, textvariable=diretorio_saida_var).grid(row=4, column=1, padx=10, pady=5)
ttk.Button(root, text="Procurar Saída", command=selecionar_diretorio_saida).grid(row=4, column=2, padx=10, pady=5)
executar_button = ttk.Button(root, text="Executar Dejavu Forensics", command=executar_dejavu)
executar_button.place(x=800, y=780)

contato_frame = tk.Frame(root)
contato_frame.grid(row=0, column=4, sticky="W", padx=10)

contato_label1 = ttk.Label(contato_frame, text="Contato: iab@ecomp.poli.br")
contato_label1.pack(anchor="w")  

contato_label2 = ttk.Label(contato_frame, text="             smll@ecomp.poli.br")
contato_label2.pack(anchor="w")  

ajuda_button = ttk.Button(root, text="Ajuda", command=abrir_guia)
ajuda_button.grid(row=0, column=3, padx=10, pady=5)

root.mainloop()
