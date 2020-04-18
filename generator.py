import random
import yaml
import subprocess


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
        \\end{enumerate}mat
        \\end{document}
        '''

with open('config.yaml') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    print(config)
    for i in range(0, config["student_number"]):

        # LaTeX file construction ---------------------------------------

        TexFileName = '%s/examen-%d.tex' % (config["output_folder"], i)
        TexFile = open(TexFileName, 'w')

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
        TexFile.close()

        # PDF creation ---------------------------------------

        proc = subprocess.Popen(['pdflatex', '-output-directory', config["output_folder"], TexFileName], shell=False)
        proc.communicate()