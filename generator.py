import random
import yaml
import subprocess
import os
import errno

# Futuros cambios:
# - pasar aparte esta plantilla
# - Hacerla menos dependiente de la posición
# - considerar la escala del logo
# - agregar gui (ver de usar easygui
# - manejo de excepciones
# - tamaño de letra y demás yerbas

FirstPartLatex = '''  \\documentclass[12pt]{exam}
 		\\usepackage{times}
        \\usepackage[utf8]{inputenc}
        \\usepackage{amsmath}
        \\usepackage{graphicx}
        \\usepackage{probsoln}
       
        \\pagestyle{head}
        \\headrule
        \\extraheadheight{.52in}
        \\lhead{\\includegraphics[scale=0.65]{%s}} 
        \\chead{\\textbf{\\bfseries %s\\\\%s\\\\%s\\\\ \\bigskip %s - %s \\\\ %s}}
        \\rhead{}
        \\PSNrandseed{%d}
        '''
# This part of the LaTeX will be written as many times as question files are in config question_bases
MidPartLatex = "\\loadrandomproblems{%d}{%s}"

EndPartLatex = '''
        \\begin{document}
         
         Cada respuesta deberá estar debidamente justificada. Caso contrario no se considerará.
         
        \\begin{enumerate}
        \\foreachproblem{\\item\\thisproblem}
        \\end{enumerate}
        \\end{document}
        '''

with open('config.yaml') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    print(config)
    for i in range(0, config["student_number"]):

        # LaTeX file construction ---------------------------------------

        TexFileName = '%s/examen-%d.tex' % (config["output_folder"], i)
        if not os.path.exists(os.path.dirname(TexFileName)):
            try:
                os.makedirs(os.path.dirname(TexFileName))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(TexFileName, 'w') as TexFile:

            randomseed = random.randint(0, 9999) # Random seed for question selection
            TexFile.write(FirstPartLatex % (config["logo"],
                                            config["university"],
                                            config["faculty"],
                                            config["department"],
                                            config["subject"],
                                            config["topic"],
                                            config["date"],
                                            randomseed))

            for ind, file in enumerate(config["question_bases"]):
                number = config["questions_per_file"][ind]
                TexFile.write(MidPartLatex % (number, file))

            TexFile.write(EndPartLatex)

        # PDF creation ---------------------------------------

        proc = subprocess.Popen(['pdflatex', '-output-directory', config["output_folder"], TexFileName], shell=False)
        proc.communicate()

        # remove auxiliary files
        filelist = [f for f in os.listdir(config["output_folder"]) if not f.endswith(".pdf")]
        for f in filelist:
            os.remove(os.path.join(config["output_folder"], f))