import os
import subprocess
import shutil

def compile_latex_files(source_directory, temp_directory, output_directory):
    # Certificar-se de que os diretórios de saída existem
    os.makedirs(temp_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    # Listar todos os arquivos no diretório de origem
    for filename in os.listdir(source_directory):
        # Verificar se o arquivo tem extensão .tex
        if filename.endswith(".tex"):
            filepath = os.path.join(source_directory, filename)
            # Compilar o arquivo .tex usando pdflatex para o diretório temporário
            subprocess.run(["pdflatex", "-output-directory", temp_directory, filepath])
            
            # Nome do arquivo PDF gerado
            pdf_filename = filename.replace(".tex", ".pdf")
            pdf_filepath = os.path.join(temp_directory, pdf_filename)
            
            # Mover o arquivo PDF para o diretório de saída
            if os.path.exists(pdf_filepath):
                shutil.move(pdf_filepath, os.path.join(output_directory, pdf_filename))

if __name__ == "__main__":
    # Diretório onde os arquivos .tex estão localizados
    source_directory = ["output/latex/medicoes", "output/latex/grandezas", "output/latex/"]
    # Diretório temporário para os arquivos compilados
    temp_directory = ["output/mock/medicoes", "output/mock/grandezas", "output/mock/total/"]
    # Diretório final para os arquivos PDF
    output_directory = ["output/pdf/medicoes", "output/pdf/grandezas", "output/pdf/"]
    
    for i in range(len(source_directory)):
        compile_latex_files(source_directory[i], temp_directory[i], output_directory[i])
        print(f"Files compiled and moved to {output_directory[i]}")
