import os
import sys
import pyperclip

inputminuted = False

if __name__ == "__main__":
    root_path = None
    # Read path from given command-line argument
    if len(sys.argv) > 0:
        arg_path = ' '.join(sys.argv[1:])
        if os.path.exists(arg_path):
            root_path = arg_path
    # If no argument was given, use base directory
    if not root_path:
        root_path = os.path.dirname(os.path.realpath(__file__))
    # pathname = os.path.join(root_path, "src")
    pathname = root_path

    latex_output = "    \\subsection{Code} \label{code}\n\n"

    for root, dirs, files in os.walk(pathname, topdown=True):
        for filename in files:
            filepath = os.path.join(root, filename)

            if "." not in filename or filename.split(".")[1] in ["png", "svg", "puml", "gitignore", "properties"] or any(x in filepath for x in ["cmake-build-debug", ".idea"]):
                continue

            # If it's a png or smthn, we can't read it, so read it first.
            file_code = ""
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    file_code = file.read()
            except Exception as e:
                continue

            minted_language = str(filename.split(".")[1])
            if minted_language == "py":
                minted_language = "python"
            elif minted_language == "h":
                minted_language = "c"
            elif minted_language == "yml":
                minted_language = "yaml"
            elif minted_language == "txt":
                minted_language = "text"
			elif minted_language in ["conf", "service", "db"]:
				minted_language = "text"

            filepath_document = (filepath.replace(pathname, "")).replace("\\", "/")
            if filepath_document.startswith("/"):
                filepath_document = filepath_document[1:]

            latex_output = str(
                f"{latex_output}"
                "        \\subsubsection{"+filepath_document+"} \label{"+filename.lower().replace(".", "_")+"}\n"
                "\n"
                "        \\begin{longlisting}\n"
                "            \\centering\n" +
                ("            \\begin{minted}[\n" if not inputminuted else "            \\inputminted[\n") +
                "                framesep=4mm,\n"
                "                baselinestretch=1,\n"
                "                breaklines,\n"
                "                breakanywhere\n"
                "            ]{"+minted_language+"}" + (("{project_files/"+(filepath.replace(root_path+"\\src\\", "")).replace("\\", "/")+"}\n") if inputminuted else f"\n{file_code}\n            \\end{'{minted}'}\n") +
                "            \\caption{"+filename+"}\n"
                "            \\label{lst:"+filename.lower().replace(".", "_")+"}\n"
                "        \\end{longlisting}\n"
                "\n"
                               )
    pyperclip.copy(latex_output)
    print("Output copied to clipboard!")
