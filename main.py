import os
import pyperclip

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.realpath(__file__))
    pathname = os.path.join(root_path, "src")

    latex_output = "    \\subsection{Code} \label{code}\n\n"

    for root, dirs, files in os.walk(pathname, topdown=True):
        for filename in files:
            if filename.split(".")[1] in ["png", "svg", "puml", "gitignore", "properties"]:
                continue

            filepath = os.path.join(root, filename)

            # If it's a png or smthn, we can't read it, so read it first.
            file_code = ""
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    file_code = file.read()
            except Exception as e:
                continue

            latex_output = latex_output + "        \\subsubsection{"+(filepath.replace(root_path+"\\src\\", "")).replace("\\", "/")+"} \label{"+filename.lower().replace(".", "_")+"}\n" \
                                          "\n" \
                                          "        \\begin{longlisting}\n" \
                                          "            \\centering\n" \
                                          "            \\begin{minted}[\n" \
                                          "                framesep=4mm,\n" \
                                          "                baselinestretch=1,\n" \
                                          "                breaklines,\n" \
                                          "                breakanywhere\n" \
                                          "            ]{"+str(filename.split(".")[1])+"}\n" \


            latex_output = latex_output + file_code

            latex_output = latex_output + "            \\end{minted}\n" \
                                          "            \\caption{"+filename+"}\n" \
                                          "            \\label{lst:"+filename.lower().replace(".", "_")+"}\n" \
                                          "        \\end{longlisting}\n" \
                                          "\n"
    pyperclip.copy(latex_output)
    print("Output copied to clipboard!")
